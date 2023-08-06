"""
The URL handler exists to assist connection to a remote system.

As it also wraps file transfer and command execution systems, even non-remote
runs should rely on the use of a URL class. For developers:
This allows RemoteRunners to focus on the file and job handling aspects

The following examples should give you an idea of basic usage of the URL
module. Lets assume we have a remote server we want to run on, with IP
address ``192.168.0.0``, and we have access via user ``user``


URL can be initialised empty then updated with connection details, or
produced in a number of ways:

>>> u = URL()
>>> print(u.local)
>>> True
>>> u.user = 'user'
>>> u.host = '192.168.0.0'
>>> print(u.local)
>>> False

Initialised with args from the start:

>>> u = URL(user='user', host='192.168.0.0')
>>> print(u.local)
>>> False

Or built from a "legacy" style string:

>>> u = URL.from_string('user@192.168.0.0')
>>> print(u.local)
>>> False

A URL instance can also connect to an existing SSH tunnel, simply specify
your local endpoint. (URL uses the presence of a port to detect tunnels).

>>> u = URL(user='user', host='127.0.0.10', port=1000)
>>> print(u.local)
>>> False
>>> print(u.is_tunnel)
>>> True

For support creating a tunnel connection, URL has the ability to assist
by providing the commands needed. Though you must provide the address of
the tunnel target for this

>>> u = URL.from_tunnel(user='user', host='192.168.0.0')

You will then be given two commands to enter on the remote:

- command 1 sets up the tunnel
- command 2 tests the tunnel

Once this is done, confirm to the tunnel constructor that the tunnel is
active with "y" and URL will connect.

See URL.from_tunnel() for more details.

There is also the functionality to test the connection with the remote:

``URL.test_connection()``

This function, when called, will attempt to create folders on both local
and remote systems, then test file transfer functionality between them.

Further details of attributes and methods are below:
"""

import subprocess
import os

from warnings import warn
from datetime import datetime

import logging
from BigDFT.LogUtils import format_iterable


# create and link logger
module_logger = logging.getLogger(__name__)


def _userhost(user, host, sep='@'):
    """!skip"""
    if user is None:
        return host
    else:
        return sep.join((user, host))


class URL:
    """
    Container to store the connection info for a Remote run

    Arguments:
        user (str):
            username for the remote system
        host (str):
            host address of the remote system
        port (int, str):
            port to connect to for ssh tunnels
    """

    _tunnel_port_range = (1000, 10000)

    _rsync_cp_fallback = 'cp fallback'
    _rsync_not_available_msg = 'no file transfer available'

    def __init__(self,
                 user: str = None,
                 host: str = None,
                 port: int = None,
                 rsync: str = None,
                 rsync_cmd: str = 'rsync',
                 verbose: bool = False):

        self._logger = logging.getLogger(__name__ + '.URL')

        self._logger.info('creating connection with params: '
                          f'user: {user}, host: {host}, port: {port}')

        # connection details
        self._conn = {'user': user,
                      'host': host,
                      'port': port}

        self._permissions = {}
        self._cmd_count = 0

        if rsync is None:
            rsync = 'auv'
        self._rsync_flags = Flags(rsync)

        self.set_rsync_command(cmd=rsync_cmd)

        self._verbose = verbose
        self._ssh_override = False

        self.utils = URLUtils(self)

    def __repr__(self):
        if self.local:
            return 'URL()'
        if self.is_tunnel:
            return f'URL(host={self.host}, port={self.port})'
        return f'URL(user={self.user}, host={self.host})'

    @classmethod
    def from_string(cls,
                    string: str,
                    rsync: str = None,
                    verbose: bool = False):
        """Create a connection from a `user@hostname` string

        Arguments:
            string (str):
                a `user@hostname` string to create a connection from
            rsync (str, optional):
                initial flags for rsync
            verbose (bool, optional):
                sets verbosity for connection actions

        Returns:
            URL
        """

        module_logger.debug(f'creating URL() from {string}')

        if string is None or str == '':
            module_logger.warning('attempting to create a URL instance '
                                  'from None or empty string. '
                                  'Creating localhost URL')
            return cls(verbose=verbose, rsync=rsync)

        if '@' not in string:
            module_logger.error(f'could not split string {string}')
            raise ValueError('please provide a user@host string')

        userhost = string.split('@')
        user = userhost[0] if len(userhost) == 2 else None
        host = userhost[-1]  # in case the user is not specified

        module_logger.debug(f'string split into {user} and {host}')

        return cls(user=user, host=host, verbose=verbose, rsync=rsync)

    @classmethod
    def from_tunnel(cls,
                    host: str,
                    user: str = None,
                    port: int = None,
                    endpoint: str = None,
                    rsync: str = None,
                    background: bool = False):
        """
        Create a URL instance based on an ssh tunnel, giving the needed command

        Guides the user through tunnel creation, creating the command
        corresponding to the desired connection details.

        .. note::

            It is advised to research and set up the tunnel yourself for your
            environment, as this method does not adapt per use case. Therefore
            the provided commands may set up an incorrect (or nonfunctional)
            tunnel.

        Arguments:
            user (str):
                username for remote host
            host (str):
                hostname to connect to
            port (int, optional):
                local port to connect to. Defaults to ``1800``
            endpoint (str, optional):
                local tunnel endpoint. Defaults to ``127.0.0.10``
            rsync (str, optional):
                rsync flags to be given to URL, if needed
            background (bool, optional):
                place the process in the background

                .. warning::

                    The process should be killed when not needed if placed
                    in the background

        Returns:
            URL

        When creating a tunnel connection you must specify the address of the
        remote server.

        For example, to connect to our ``192.168.0.0`` server, the connection
        details for a standard ``ssh`` are required variables. You can
        optionally specify the tunnel *endpoint*: The "local" IP address and
        port of the tunnel.

        When creating a tunnel, you will be given two commands:

        - tunnel creation command
        - tunnel test command

        The tunnel creation command will look similar to this:

        ``ssh user@192.168.0.0 -L 1000:127.0.0.10:192.168.0.0:22 -N``

        Whereas the test command will be a simple ssh "ls" command to ensure
        that the tunnel is operational and allows info transfer.

        ``ssh -p 1000 127.0.0.10 "ls"``

        Assuming everything works, enter ``y`` to continue.
        """

        # LG: user can be omitted (useful if the info is in ssh config)
        # if user is None:
        #     raise ValueError('Please provide a username')

        if host is None:
            raise ValueError('Please provide a hostname')

        if port is None:
            # port = random.randint(*URL._tunnel_port_range)
            port = 1800

        if endpoint is None:
            endpoint = '127.0.0.10'

        bg = 'f' if background else ''

        userhost = _userhost(user, host)

        tunnelstring = f'ssh {userhost} -L ' \
                       f'{endpoint}:{port}:{host}:22 -{bg}N'

        module_logger.debug('attempting tunnel creation using command '
                            f'"{tunnelstring}"')

        inputmsg = f"""Use the following command to create the tunnel:
        \n{tunnelstring}\n
        \nThen attempt the following command (in a separate terminal if needed)
        \nssh -p {port} {endpoint} "ls"\n
        \ncontinue (y/n)? """

        cont = ''
        timeout = 10
        count = 0
        while cont.lower() != 'y':
            count += 1
            if count > timeout:
                module_logger.error('tunnel creation exited after timeout')
                raise Exception('tunnel creation failed')
            cont = input(inputmsg)
            module_logger.debug(f'user entered: "{repr(cont)}"')
            if cont == 'n':
                module_logger.debug('user exited tunnel creation')
                raise Exception('tunnel creation exited')

        module_logger.debug('attempting to connect to tunnel endpoint')

        return cls(user, endpoint, port, rsync)

    def userhost(self, sep='@'):
        """Return a userhost string, allowing for user to be empty"""
        return _userhost(self.user, self.host, sep)

    @property
    def user(self):
        """Attribute for the 'user' connection parameter"""
        return self._conn['user']

    @user.setter
    def user(self, user: str):
        self._logger.debug(f'setting username to {user}')
        self._conn['user'] = user

    @property
    def host(self):
        """Attribute for the 'host' connection parameter"""
        return self._conn['host']

    @host.setter
    def host(self, host: str):
        self._logger.debug(f'setting hostname to {host}')
        self._conn['host'] = host

    @property
    def port(self):
        """
        Attribute for the 'port' connection parameter

        Used to detect presence of an SSH tunnel
        """
        return self._conn['port']

    @port.setter
    def port(self, port: int):
        self._logger.debug(f'setting port to {port}')
        self._conn['port'] = port

    @property
    def verbose(self):
        """Attribute determining the verbosity of operations"""
        return self._verbose

    @verbose.setter
    def verbose(self, verbose: bool):
        self._logger.debug(f'setting verbosity to {verbose}')
        self._verbose = verbose is True

    @property
    def local(self):
        """Returns True if this connection is local only"""
        # use the lack of a hostname to determine
        # as user and port can be either
        return self._conn['host'] is None

    @property
    def is_tunnel(self):
        """Returns True if this connection uses an SSH tunnel"""
        return self._conn['port'] is not None

    @property
    def rsync_flags(self):
        """
        Attribute determining the flags used for any rsync process

        .. note::
            These flags will be ignored if `rsync` is not available (`cp` is
            used as a fallback in this case)
        """
        return self._rsync_flags.flags

    @rsync_flags.setter
    def rsync_flags(self, flags: str):
        self._rsync_flags.flags = flags

    @property
    def permissions(self):
        """
        Displays the available permissions for this URL

        Dictates whether files can be created in root, or only in the user
        directories

        .. note::
            This property will test the connection if no permissions can be
            found

        Returns:
            dict:
                permissions
        """
        if len(self._permissions) == 0:
            self.test_connection()

        return self._permissions

    @property
    def ssh(self) -> str:

        if self._ssh_override:
            if hasattr(self, '_ssh'):
                return self._ssh

            else:
                self.ssh_override = False
                return self.ssh

        """ssh command to be used for this connection"""
        self._logger.debug('generating ssh command')
        ret = ['ssh ']
        if self.is_tunnel:
            self._logger.debug('tunnel connection, adding "-p port"')
            ret.append(f'-p {self.port} ')
        elif not self.local:
            self._logger.debug('remote connection, adding host')
            ret.append(f'{self.userhost()}')
        else:
            self._logger.warning('local connection, returning empty ssh')
            return ''
        ssh = ''.join(ret)
        self._logger.debug(f'ssh command: {ssh}')
        return ssh

    def set_rsync_command(self, cmd='rsync'):
        self._rsync = cmd

    @ssh.setter
    def ssh(self, override):
        """
        override ssh property with given value

        Args:
            override (str):
                new property
        """
        self._ssh_override = True
        self._ssh = override

    @property
    def ssh_override(self):
        """
        returns True if we are overriding the ssh value
        """
        return self._ssh_override

    @ssh_override.setter
    def ssh_override(self, flag):
        """
        enable/disable ssh
        """
        self._ssh_override = flag

    def cmd(self,
            cmd: str,
            asynchronous: bool = False,
            local: bool = None,
            verbose: bool = None,
            suppress_warn: bool = False,
            return_error: bool = False) -> str:
        """
        Execute a command

        Arguments:
            cmd (str):
                the command to be executed
            asynchronous (bool, optional):
                do not wait for stdout if async
            local (bool, optional):
                force local or remote execution
            verbose (bool, optional):
                verbosity override for this execution
            suppress_warn (bool, optional):
                suppress warnings
            return_error (bool, optional):
                prefer returning a raised error over stdout

        Returns:
            str:
                stdout if not async, None otherwise
        """
        if verbose is None:
            verbose = self.verbose

        self._logger.info(f'sending command {repr(cmd)}')
        self._logger.debug(f'async: {asynchronous}, '
                           f'local: {local}, '
                           f'verbose: {verbose}, '
                           f'suppress warns: {suppress_warn}, '
                           f'prefer error return: {return_error}')

        # ensure the command is being executed where we need
        # disable if local only, this will result in a "command", which doesn't
        # run
        if not self.local and local is not None:
            if not local and not cmd.startswith(self._rsync):
                self._logger.debug('forced remote connection and not rsync, '
                                   'generating and adding ssh')
                cmd = f"{self.ssh} '{cmd}'"

        elif not self.local and not cmd.startswith(self._rsync):
            self._logger.debug('implicit remote connection and not rsync, '
                               'generating and adding ssh')
            cmd = f'{self.ssh} "{cmd}"'
        # TODO(lbeal) add protection against "rm -r *" commands

        # {brace expansion} needs '/bin/bash' in some cases (seen with cp)
        # https://stackoverflow.com/a/22660171
        sub = subprocess.Popen(cmd,
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE,
                               shell=True,
                               text=True,
                               executable='/bin/bash')
        self._logger.debug('done')
        self._cmd_count += 1
        if not asynchronous:
            ret, err = sub.communicate()

            self._logger.debug('returned string:')
            self._logger.debug(format_iterable(ret.split('\n')))
            if err is not None and err != '':
                self._logger.warning(f'command: {repr(cmd)}')
                self._logger.warning(f'returned error: {err}')
                if return_error:
                    return err
                elif not suppress_warn:
                    warn(str(err), UserWarning)
            if verbose:
                print('cmd returned: ' + ret)
            if hasattr(ret, 'decode'):
                ret = ret.decode('utf-8')
            return str(ret)
        else:
            return None

    def ls(self,
           target: str = './',
           local: bool = False) -> list:
        """
        Perform `ls` command on target

        Arguments:
            target (str):
                target entity (folder or file)
            local (bool):
                force local or remote search

        Returns:
            list:
                newline split result
        """
        self._logger.debug(f'performing ls on {target}')
        ls_ret = self.cmd(f'ls {target}', local=local).split('\n')
        self._logger.debug(f'ls result for {target}: {ls_ret}')

        return [f for f in ls_ret if f != '']

    def rsync(self,
              files: list,
              origin: str,
              target: str = None,
              push: bool = True,
              dry_run: bool = False):
        """
        Create rsync "link" between origin and target, pull or push files

        Arguments:
            files (list):
                list of filenames to transfer
            origin (str):
                origin folder
            target (str):
                target folder
            push (bool):
                files are to be sent (or received)
            dry_run (bool):
                don't send the command if True
        Returns:
            str:
                the rsync command stdout or the command if dry_run
        """
        self._logger.debug(f'performing rsync from {origin} to {target} '
                           f'for {len(files)} files')
        # can work without a target, but use same folder name as origin
        if target is None:
            self._logger.warning(f'rsync target is None, setting target to '
                                 f'origin ({origin}')
            target = origin
        # check if we're using 'cp' as a fallback (rsync not available)
        cp_fallback = False
        if hasattr(self, '_permissions'):
            rsync = self._permissions.get('rsync', self._rsync)
            self._logger.debug('validation currently:')
            self._logger.debug(f'{format_iterable(self._permissions)}')
            if rsync == self._rsync_cp_fallback:
                self._logger.warning('rsync not available, but cp_fallback is '
                                     'set. Replacing rsync calls with cp')
                cp_fallback = True

        # initial setup with command and flags
        cmd = [self._rsync, self._rsync_flags.flags]
        if cp_fallback:  # override base command if cp_fallback
            cmd = ['cp']
        # if we're tunnelling, the port has to be specified here
        # also set up target folder connection address if needed
        if self.is_tunnel:
            cmd.append(f"'-e ssh -p {self.port}'")

            target = f'{self.host}:{target}'
        elif not self.local:
            target = f'{self.userhost()}:{target}'

        self._logger.debug(f'target updated to {target}')

        srt = origin if push else target
        end = target if push else origin
        self._logger.debug(f'as push is {push}, moving files from '
                           f'{srt} to {end}')
        if self.verbose:
            print('sending', files)
            print(f'from {srt} to {end}')
        # wrap files into a {container} where possible
        # for this syntax to be valid we must be transferring >1 files
        if len(files) <= 1:
            for file in files:
                cmd.append(os.path.join(srt, file))
        else:
            temp = [os.path.join(srt, '{')]
            for file in files:
                temp.append(file + ',')
            cmd.append(''.join(temp)[:-1] + '}')

        cmd.append(end)
        cmd = ' '.join(cmd)
        self._logger.debug(f'rsync command produced: {cmd}')
        if dry_run:
            return cmd
        return self.cmd(cmd)

    def ensure_dir(self,
                   dir: str,
                   force_local: bool = False):
        """
        Ensure a directory exists by attempting to create it

        Arguments:
            dir (str):
                directory to create
            force_local (bool):
                force a local run

        Warning: Duplicate of futile.Utils.ensure_dir
        """
        self._logger.debug(f'ensuring presence of dir {dir}')
        if force_local:
            self.cmd(f'mkdir -p {dir}', local=True)
        else:
            self.cmd(f'mkdir -p {dir}')

    def test_connection(self,
                        verbose: bool = None) -> bool:
        """
        Run a connection test suite:
        - Folder creation
            - locally
            - remotely
        - rsync files
            - push
            - pull

        Arguments:
            verbose (bool):
                verbosity for this test

        Returns:
            bool:
                True if test was successful
        """
        start_cmd_count = self._cmd_count
        # override verbosity for these tests
        # (they can produce a lot of output)
        old_verbose = self.verbose
        local_verbose = True
        if verbose is None:
            # minimal verbosity, but not off
            self.verbose = False
        elif verbose:
            # fully on
            self.verbose = True
        elif not verbose:
            # fully off
            self.verbose = False
            local_verbose = False

        self._logger.debug(f'testing connection with verbosity '
                           f'{local_verbose}')

        t_start = datetime.now()
        # test local folder creation
        local_fld = self._file_create_validation(root='/',
                                                 local=True,
                                                 verbose=local_verbose)

        # test remote folder creation
        remote_fld = self._file_create_validation(root='/',
                                                  local=False,
                                                  verbose=local_verbose)

        # test rsync
        self._logger.debug('testing rsync file sending')
        success_l = self._file_transfer_validation(push=True,
                                                   local_verbose=local_verbose)

        self._logger.debug('testing rsync file receiving')
        success_r = self._file_transfer_validation(push=False,
                                                   local_verbose=local_verbose)

        t_end = datetime.now()
        dt = (t_end - t_start).total_seconds()

        self._logger.debug('setting verbose back to old value')
        self.verbose = old_verbose

        self._logger.info('connection test completed, validation is now:')
        self._logger.info(f'{format_iterable(self._permissions)}')

        deltacmd = self._cmd_count - start_cmd_count
        t_avg = dt/deltacmd
        msg = f'used {deltacmd} cmd calls for this test, ' \
              f'taking {dt:.2f} seconds (averaging {t_avg:.2f}s per call)'
        if local_verbose:
            print(msg)
        self._logger.info(msg)

        self._permissions['latency'] = t_avg

        if all((local_fld, remote_fld, success_l, success_r)):
            return True
        return False

    def _create_unique_folder(self, name, local, verbose):
        """
        given an prospective absolute path, ensure the final leaf folder is
        unique

        Arguments:
            name (str):
                absolute path to intended folder
            local (bool):
                perform locally or not
            verbose (bool):
                verbosity for this test
        """
        self._logger.info(f'ensuring a unique name for {name}')
        root, base = os.path.split(name)
        self._logger.debug(f'running with root path {root}')
        # directory access
        prior = self.ls(root, local=local)

        uniq = base

        i = 0
        timeout = 10
        while uniq in prior:
            if i > timeout:
                raise ValueError('could not create folder, '
                                 f'try cleaning out {root}')
            i += 1
            self._logger.warning(f"can't create test folder {uniq}: "
                                 "already exists")
            if verbose:
                print(f'{uniq} already exists ({i}/{timeout})')
            uniq = f'{base}_{i}'

        return os.path.join(root, uniq)

    def _file_create_validation(self, root, local, verbose, repeat=False):
        if not local and self.local:
            self._logger.warning('system is local only, forcing local for '
                                 'remote connection test file creation')
            # can't test remote permissions if there's no remote
            local = True
        if verbose and not repeat:
            border = '#'*8
            runtype = 'local' if local else 'remote'
            print(f'\n{border} {runtype} permissions {border}')
        # generate a folder name that doesn't already exist
        test_folder = os.path.join(root, 'URL_connection_test')

        test_folder = self._create_unique_folder(test_folder,
                                                 local=local,
                                                 verbose=verbose)

        if verbose:
            print(f'creating test folder {test_folder}')
        self._logger.debug(f'test creating test folder {test_folder}')

        ret = self.cmd(f'mkdir -p {test_folder}',
                       local=local,
                       suppress_warn=True,
                       return_error=True)

        if 'cannot create directory' in ret:
            if root == '/':
                # try again in user folder
                newroot = self.cmd('echo $HOME', local=local).rstrip('\n')
                if verbose:
                    print(f'\tpermission denied, trying again in {newroot}')
                self._logger.info(f'trying again with root {newroot}')
                return self._file_create_validation(root=newroot,
                                                    local=local,
                                                    verbose=verbose,
                                                    repeat=True)
            return False
        if verbose:
            print('\tsuccess, cleaning up')

        self._logger.info(f'test successful, removing folder {test_folder}')
        self.cmd(f'rm -r {test_folder}', local=local)

        perm = 'local_root' if local else 'remote_root'

        self._permissions[perm] = root

        return True

    def _file_transfer_validation(self,
                                  push,
                                  local_verbose):

        lroot = self.permissions['local_root']
        rroot = self.permissions.get('remote_root',
                                     self.permissions['local_root'])

        local_fld = os.path.join(lroot,
                                 'rsync_test_local')
        remote_fld = os.path.join(rroot,
                                  'rsync_test_remote')

        self._logger.debug(f'file transfer validation with local {local_fld}, '
                           f'remote {remote_fld}, push = {push}')

        self.ensure_dir(local_fld, force_local=True)
        self.ensure_dir(remote_fld, force_local=False)

        dirn = 'push' if push else 'pull'
        if local_verbose:
            border = '#'*8
            print(f'\n{border} file {dirn} test {border}')

        test_file = f'testfile_{dirn}'
        start_fld = local_fld if push else remote_fld
        dest_fld = remote_fld if push else local_fld
        if local_verbose:
            print(f'test {dirn} {test_file} from {start_fld} to {local_fld}')

        self._logger.debug(f'{test_file} from {start_fld} to {dest_fld}')

        self.cmd(f'touch {start_fld}/{test_file}', local=push)
        self.rsync([test_file], local_fld, remote_fld, push=push)

        success = test_file in self.ls(f'{dest_fld}', local=not push)

        if success:
            # repeated tests will use the fallback if enabled. So make sure
            # it does not get set back to rsync here if that is the case
            # use a get on the validation dict, defaulting back to 'rsync'
            self._permissions['rsync'] = self._permissions.get('rsync',
                                                               self._rsync)
            if local_verbose:
                print('\tsuccess, cleaning up')

        elif self.local:
            if local_verbose:
                print('\trysnc failed but we are running locally, testing cp')
            # if we're local only, can use 'cp' as a fallback
            self._logger.warning('rysnc test failed, testing cp as a fallback')
            self.cmd(f'cp {start_fld}/{test_file} {dest_fld}', local=True)

            success = test_file in self.ls(f'{dest_fld}', local=True)

            if success:
                if local_verbose:
                    print('\tsuccess with cp, cleaning up'
                          '\n\tit should be investigated why rsync is not '
                          'working')
                self._logger.warning('cp succeeded. Using for now (THIS '
                                     'SHOULD BE TREATED AS AN ISSUE)')
                self._permissions['rsync'] = self._rsync_cp_fallback
            else:
                print('\tfailure, attempting to clean up')
                self._logger.warning('cp also failed, check permissions and '
                                     'commands passed')
        if not success:
            self._permissions['rsync'] = self._rsync_not_available_msg

        self.cmd(f'rm -r {local_fld}', local=True)
        self.cmd(f'rm -r {remote_fld}', local=False)

        return success


class URLUtils:
    """
    Extra functions to go with the URL class, called via URL.utils

    As it requires a parent `URL` to function, and is instantiated with a
    `URL`, there is little to no purpose to using this class exclusively

    Arguments:
        parent (URL):
            parent class to provide utils to
    """
    def __init__(self, parent: URL):

        self._logger = logging.getLogger(__name__ + '.URLUtils')
        self._logger.info(f'creating a utils extension to parent: {parent}')

        self._parent = parent

    def search_folder(self, files: list, folder: str, local: bool = False):
        """
        Search `folder` for `files`, returning a boolean presence dict

        Arguments:
            files (list):
                list of filenames to check for. Optionally, a string for a
                single file
            folder (str):
                folder to scan
            local (bool):
                perform the scan locally (or remotely)
        Returns (dict):
            {file: present} dictionary
        """
        fpath = folder  # os.path.abspath(folder) # not locally available

        self._logger.debug(f'scanning folder {folder}. '
                           f'Convert to abspath {fpath}')
        self._logger.debug('searching for files:')
        self._logger.debug(f'{format_iterable(files)}')

        ls_return = self.ls(fpath, local=local, as_list=True)

        scan = [os.path.basename(f) for f in ls_return]

        self._logger.debug('scan sees:')
        self._logger.debug(f'{format_iterable(scan)}')

        if isinstance(files, str):
            self._logger.info('files is a string, running in singular mode')

            ret = {files: os.path.basename(files) in scan}

        else:
            ret = {}
            for file in files:
                fname = os.path.basename(file)
                ret[file] = fname in scan

        return ret

    def touch(self, file: str, local: bool = False):
        """
        perform unix `touch`, creating or updating `file`

        Arguments:
            file (str):
                filename or path to file
            local (bool):
                force local (or remote) execution
        """
        self._logger.debug(f'utils touch on file {file}')
        fname = os.path.abspath(file)
        self._parent.cmd(f'touch {fname}', local=local)

    def mkdir(self, file, local=False):
        """
        perform unix `mkdir -p`, creating a folder structure

        Arguments:
            file (str):
                name or path to folder
            local (bool):
                force local (or remote) execution
        """
        self._logger.debug(f'utils mkdir on path {file}')
        fname = os.path.abspath(file)
        print(f'making dir {fname}')
        self._parent.cmd(f'mkdir -p {fname}', local=local)

    def ls(self, file: str, as_list: bool = True, local: bool = False):
        """
        Identify the files present on the directory

        Arguments:
            file (str):
                name or path to folder.
            as_list (bool):
                convert to a list format
            local (bool):
                force local (or remote) execution
        """
        self._logger.debug(f'utils ls on path {file}')
        fname = os.path.abspath(file) if local else file

        ret = self._parent.cmd(f'ls {fname}', local=local)

        if as_list:
            ret = [f for f in ret.split('\n') if f != '']
        return ret


class Flags:
    """
    Basic but flexible handler for terminal command flags

    Allows for inplace modification:

    >>> f = Flags('abcdd')
    >>> f -= 'd'
    >>> f.flags
    >>> '-abcd'

    Arguments:
        initial_flags (str):
            initial base flags to be used and modified if needed
        prefix (optional, str):
            the non-argument prefix for these flags (`-`, `--`, etc.)
    """

    _logger = logging.getLogger(__name__ + '.Flags')

    def __init__(self, initial_flags: str = '', prefix: str = None):

        self._logger.debug(f'creating Flags with initial flags '
                           f'{initial_flags} and prefix {prefix}')

        self._prefix = ''
        if prefix is None:
            if '-' in initial_flags:
                self.prefix = '-' * initial_flags.count('-')
            else:
                self.prefix = '-'
            self._logger.debug(f'prefix set to {self.prefix}')
        else:
            self.prefix = prefix

        self.flags = initial_flags

    def __repr__(self):
        return f'Flags({self.flags})'

    def __add__(self, other):
        self._flags = self._flags + other.strip('-')
        self._logger.debug(f'adding {other} to flags. '
                           f'Flags are now {self.flags}')

    def __iadd__(self, other):
        self.__add__(other)
        self._logger.debug(f'adding {other} to flags inplace. '
                           f'Flags are now {self.flags}')
        return self

    def __sub__(self, other):
        """Subtract unique flags in other once."""
        for char in ''.join(set(other)):
            self._flags = self._flags.replace(char, '', 1)
        self._logger.debug(f'subtracting {other} from flags. '
                           f'Flags are now {self.flags}')

    def __isub__(self, other):
        self.__sub__(other)
        self._logger.debug(f'subtracting {other} from flags inplace. '
                           f'Flags are now {self.flags}')
        return self

    @property
    def flags(self):
        """Returns the fully qualified flags as a string"""
        if len(self._flags) == 0:
            return ''
        return self.prefix + self._flags

    @flags.setter
    def flags(self, inp):
        """Set the flags to the new input

        Arguments:
            inp (str):
                new flags to use (will overwrite old ones)
        """
        self._logger.debug(f'setting flags to {inp}')
        for char in set(self.prefix):
            inp = inp.strip(char)
        self._logger.debug(f'after cleaning, flags are now: {inp}')
        self._flags = inp

    @property
    def prefix(self):
        """
        Attribute determining the - prefix used for these flags

        For example, a flag with a prefix of `-` will be added as `-flag`
        Change the prefix to `--` to be passed as `--flag`, and so on
        """
        return self._prefix

    @prefix.setter
    def prefix(self, prefix):
        self._prefix = prefix


if __name__ == '__main__':

    tunnel = False
    test = URL(rsync='aux')
    if tunnel:
        test.host = '127.0.0.10'
        test.port = 1800
    else:
        test.host = '192.168.0.17'
    test.user = 'pi'

    print(test)
    test.test_connection()
