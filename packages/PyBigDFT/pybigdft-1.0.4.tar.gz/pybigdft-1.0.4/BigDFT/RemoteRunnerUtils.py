try:
    from BigDFT.AiidaCalculator import AiidaCalculator
    AIIDA_FLAG = True
except ModuleNotFoundError:
    AIIDA_FLAG = False


import logging
from BigDFT.LogUtils import format_iterable


# create and link logger
module_logger = logging.getLogger(__name__)


def _find_in_ls(ls_return, target):
    """Parse the output of a system 'ls', searching for a target file

    ls_return: bytestring return from _system "ls" call in target folder
    target: target file (path or filename)

    Returns:
        bool: presence of target file
    """
    import os
    if '/' in target or r'\\' in target:
        target = os.path.split(target)[-1]

    files = ls_return.split('\n')
    return target in files


def _bind_closure(f, **kwargs):
    """
    Given a function and its named arguments, this routine binds that as
    a lexical context for a closure which is returned.
    """
    return lambda: f(**kwargs)


class RemoteFunction:
    """Serialize and execute remotely a python function.

    With this class we serilize and execute a python function
    on a remote filesystem. This filesystem may be a remote computer
    or a different directory of the local machine.

    Such class is useful to be employed in runners which needs to be executed
    outside of the current framework, butfor which the result is needed to
    continue the processing of the data.

    Args:
        name (str): the name of the remote function
        function (func): the python function to be serialized.
            The return value of the function should be an object for which
            a relatively light-weight serialization is possible.
        submitter (str): the interpreter to be invoked. Should be, e.g.
            `python` if the function is a python function, or `bash`.
        **kwargs:  keyword arguments of the function.
            The arguments of the function should be serializable without
            the requirement of too much disk space.
    """
    def __init__(self, submitter, name, **kwargs):
        self._logger = logging.getLogger(__name__ + '.' + 'RemoteFunction')
        self._logger.error('baseclass RemoteFunction has been called')
        self.name = name
        self.submitter = submitter
        self.appended_functions = []
        self.arguments = kwargs
        self.output_files = []
        raise NotImplementedError

    def _set_arguments(self):
        pass

    def _serialize(self, run_dir):
        return []

    def _make_run(self, run_dir):
        self.resultfile = None
        self.runfile = None
        raise NotImplementedError

    def _read_results(self, run_dir):
        return None

    def files_sent(self, yes):
        """
        Mark the relevant files as sent.

        Args:
            yes (bool): True if the files have been already sent to the
                remote directory
        """
        self.files_have_been_sent = yes

    def files_received(self, yes):
        """
        Mark the relevant files as received.

        Args:
            yes (bool): True if the files have been already received in the
                remote directory
        """
        self.files_have_been_received = yes

    def directories_created(self, yes):
        """
        Mark the relevant directories as created.

        Args:
            yes (bool): True if the directories have been tested as present.
        """
        self.directories_ensured = yes

    def _write_main_runfile(self, pscript, run_dir):
        from os.path import join
        runfile = join(run_dir, self.runfile)
        with open(runfile, "w") as ofile:
            ofile.write(pscript + '\n' + self._append_further_lines())
        return self.runfile

    def _append_further_lines(self):
        pscript = ''
        for func in self.appended_functions:
            pscript += func.call(remotely=False, remote_cwd=True) + '\n'
        return pscript

    def _append_further_files_to_send(self):
        initials = []
        for func in self.appended_functions:
            initials += func.setup(src=self.local_directory)
            self.resultfile = func.resultfile  # override resultfile
        return initials

    def _append_further_files_to_receive(self):
        initials = []
        for func in self.appended_functions:
            initials.append(func.resultfile)  # add the result for info
            initials += func.output_files
        return initials

    def prepare_files_to_send(self):
        """List of files that will have to be sent.

        This function defines the files which requires to be sent over
        in order to execute remotely the python function.
        Also set the main file to be called and the resultfile.

        Returns:
            dict: files which will be sent
        """
        run_dir = self.local_directory
        self._set_arguments()
        initials = self._serialize(run_dir)
        pscript = self._make_run(run_dir)
        dependencies = self._append_further_files_to_send()
        self.main_runfile = self._write_main_runfile(pscript, run_dir)
        initials.append(self.main_runfile)
        self.files_sent(False)
        return initials + dependencies

    def prepare_files_to_receive(self):
        """List of files that will have to be received.

        This function defines the files which requires to be get from the url
        in order to execute remotely the python function.

        Returns:
            dict: files which will be received
        """
        initials = self.output_files
        dependencies = self._append_further_files_to_receive()
        initials.append(self.resultfile)
        self.files_received(False)
        return initials + dependencies

    def setup(self, dest='.', src='/tmp/'):
        """Create and list the files which have to be sent remotely.

        Args:
            dest (str): remote_directory of the destination filesystem.
                The directory should exist and write permission should
                be granted.
            src (str): local directory to prepare the IO files to send.
                The directory should exist and write permission should
                be granted.

        Returns:
            list: list files
        """
        self.local_directory = src
        self.remote_directory = dest
        files_to_send = [f for f in self.prepare_files_to_send()]
        self.files_to_send = files_to_send
        files_to_receive = [f for f in self.prepare_files_to_receive()]
        self.resultfiles = files_to_receive
        return files_to_send

    def send_files(self, files):
        """Send files to the remote filesystem to which the class should run.

        With this function, the relevant serialized files should be sent,
        via the rsync protocol (or equivalent) into the remote directory
        which will then be employed to run the function.

        Args:
            files(dict): source and destination files to be sent,
                organized as items of a dictionary.
        """
        if hasattr(self, 'files_have_been_sent') and self.files_have_been_sent:
            self._logger.debug('files are marked as already sent')
            pass
        else:
            self.url.rsync(files,
                           self.local_directory,
                           self.remote_directory)
        self.files_sent(True)

    def append_function(self, extra_function):
        """Include the call to another function in the main runfile.

        With this method another remote function can be called in the same
        context of the remote call.
        Such remote function will be called from within the same remote
        directory of the overall function.
        The result of the remote function will then be the result provided
        from the last of the appended functions.

        Args:
            extra_function (RemoteFunction): the remote function to append.
        """
        assert extra_function.name != self.name, \
            'Name of the remote function should be different'
        for func in self.appended_functions:
            assert extra_function.name != func.name, \
                'Cannot append functions with the same name'
        self.appended_functions.append(extra_function)

    def send_to(self, dest='.', src='/tmp/'):
        """Assign the remote filesystem to which the class should run.

        With this function, the relevant serialized files should be sent,
        via the rsync protocol (or equivalent) into the remote directory
        which will then be employed to run the function.

        Args:
            dest (str): remote_directory of the destination filesystem.
                The directory should exist and write permission should
                be granted.
            src (str): local directory to prepare the IO files to send.
                The directory should exist and write permission should
                be granted.
        """
        files = self.setup(dest=dest, src=src)
        self.send_files(files)

    def call(self, remotely=True, remote_cwd=False):
        """Provides the command to execute the function.

        Args:
            remotely (bool): invoke the function from local machine.
                employ ssh protocol to perform the call.
            remote_cwd (bool): True if our CWD is already the remote_dir to
                which the function has been sent. False otherwise.
                Always assumed as False if remotely is True.

        Returns:
            str: the string command to be executed.
        """
        # touch the file to ensure that the run (modification) time is accurate
        command = f'touch {self.main_runfile} && {self.submitter} ' \
                  f'{self.main_runfile}'
        if remotely or not remote_cwd:
            command = f'cd {self.remote_directory} && {command}'
        return command

    def is_finished(self, remotely=True, anyfile=True,
                    timeout=-1, verbose=None):
        """
        Check if the function has been executed.

        This is controlled by the presence of the resultfile. This runfile has
        a set name that is generated at initalisation.

        Args:
            remotely (bool): control the presence of the result on the remote
                filesystem
            anyfile (bool): determine if any run is finished. Useful if the run
                in question is asyncronous
            timeout (int): maximum number of times is_finished can be called
                before the check times out, prevents infinite loops.
                Set to -1 to disable check
                Set to integer to limit to `timeout` calls.
            verbose (bool):
                local verbosity for this check
        Return:
            bool: True if ready, False otherwise.

        ``is_finished`` will return the status of the run it is called for.
        Checks can be made remotely for checking if a remote run has finished,
        or locally, to check whether the files from a remote run have been
        transferred back to the local system, or to check if a local run has
        completed.

        Advanced arguments such as ``anyfile`` and ``timeout`` can greatly
        enhance the capabilities of these checks.

        Anyfile

        The ``anyfile`` argument states whether ``is_finished()`` cares about
        *any* file that matches the resultfile name for the run, or should
        check that the file has been created after the run file was created.

        Simply put, add ``anyfile=True`` to a call to ensure that the results
        that get returned from the remote are due to a recent run, and not one
        that has been run previously and the files have not been cleaned up.

        Timeout

        The ``timeout`` argument will allow is_finished to fail ``timeout``
        times before returning false. This can be useful for ensuring that
        a ``while not run.is_finished`` loop does not run forever, but still
        has allowance for waiting for a run to start.

        Final Notes

        Verbosity can be explicity set for each call, allowing a run where
        the global verbosity is False to provide info on the run states, or
        vice versa.

        Remotely can also be given, to force a run to check only locally (or
        remotely)
        """
        logstr = ['### New call: Checking for finished run:',
                  f'remote: {remotely},',
                  f'anyfile: {anyfile},',
                  f'timeout: {timeout}']
        self._logger.debug(' '.join(logstr))
        from os.path import join, getmtime
        if verbose is None:
            verbose = getattr(self, 'verbose', True)
        if verbose:
            print('Checking for finished run... ', end='')
        remotefile = self.resultfile

        if timeout >= 0:
            self._is_finished_timeout = timeout

        if remotely:
            # better to ask forgiveness...
            try:
                root = self.remote_directory
            except AttributeError:
                if verbose:
                    print('No (No files found)')
                self._logger.info('not finished, nothing found')
                return False
        else:
            root = self.local_directory

        self._logger.debug(f'checking for {remotefile} in {root}')
        remotefile = join(root, remotefile)

        # check that a remote results file exists
        # check_output will return a CalledProcessError
        # in the event that none are present
        if not remotely or self.url.local:
            if verbose:
                print('locally... ', end='')
            ret = self.url.cmd('ls ' + root, local=True)
        else:
            if verbose:
                print('remotely... ', end='')
            ret = self.url.cmd('ls ' + root)
        self._logger.debug(f'ls return from search: \n{str(ret)}')

        file_present = _find_in_ls(ret, remotefile)

        if not file_present:
            if verbose:
                print('No (No result file)')
            self._logger.info('not finished, no results file')
            return self._is_finished_finalise(False)  # no file

        # we have a results file, check modification times if we care about
        # the _current_ run
        if not anyfile:
            runfile = join(root, self.runfile)

            # file modification times (unix) of results, and runner
            if not remotely or self.url.local:
                res_mtime = getmtime(remotefile)
                run_mtime = getmtime(runfile)
            else:
                # Get the modified time using stat
                res_mtime = self.url.cmd('stat -c %Y ' + remotefile)
                run_mtime = self.url.cmd('stat -c %Y ' + runfile)

                res_mtime = int(res_mtime)
                run_mtime = int(run_mtime)

            self._logger.debug('found file with stats:\n'
                               f'\tresult time {res_mtime}\n'
                               f'\trun time:   {run_mtime}')

            # if the results file was modified after the current run file
            # there is likely a run still in progress, so return false
            if res_mtime < run_mtime:
                if verbose:
                    print('No (Outdated resultsfile)')
                self._logger.info('not finished, file is outdated')
                # there's a file, but from before this run
                return self._is_finished_finalise(False)

            if verbose:
                print('Yes (And recent run)')
            self._logger.info('finished, found a file (and is recent)')
            # res file, and from after the last run
            return self._is_finished_finalise(True)

        if verbose:
            print('Yes (Found a results file)')
        self._logger.info('finished, found a file (any valid filename)')
        # file, and we care about any run
        return self._is_finished_finalise(True)

    def _is_finished_finalise(self, fin):
        """
        called by is_finished before a return to ensure that the `timeout`
        argument is respected
        """
        # set up or retrieve the timeout limit
        if hasattr(self, '_is_finished_timeout'):
            lim = self._is_finished_timeout
            self._logger.debug(f'_is_finished_timeout is set to {lim}')
        else:
            self._logger.debug('creating new timeout attribute with val -1')
            lim = -1

        # set up or increment the calls counter
        if not hasattr(self, '_is_finished_calls'):
            self._logger.debug('creating new calls attribute with val 1')
            self._is_finished_calls = 1
        else:
            self._is_finished_calls += 1
            self._logger.debug('_is_finished_calls is now '
                               f'{self._is_finished_calls}')

        # raise an error if needed
        if lim >= 0:
            if self._is_finished_calls >= lim:
                self._logger.warning('is_finished timed out with calls '
                                     f'{self._is_finished_calls}')
                raise ValueError('is_finished timed out')

        # reset if we're exiting
        if fin:
            # disable timeout after a successful run
            self._is_finished_timeout = -1
            self._is_finished_calls = 0

        return fin

    def receive_files(self, files):
        """
        Fetch files back from the run directory as needed.
        Mark them as received once done.
        """
        # cut down the list to unique filenames
        files = [f for f in set(files)]
        self._logger.debug('requesting file retreival for files:')
        self._logger.debug(f'{format_iterable(files)}')
        if hasattr(self, 'files_have_been_received') and \
                self.files_have_been_received:
            self._logger.debug('files have already been received, skipping...')
            pass
        else:
            self._logger.debug('files not already local, retreiving...')
            self.url.rsync(files,
                           self.local_directory,
                           self.remote_directory,
                           push=False)
        self._logger.debug('marking files as received')
        self.files_received(True)

    def fetch_result(self, remotely=True):
        """Get the results of a calculation locally.

        Args:
            remotely (bool): control the presence of the result on the remote
                filesystem

        Returns:
            The object returned by the original function
        """
        self._logger.info(f'fetching results, remotely: {remotely}')
        if hasattr(self, 'protocol') and self.protocol == 'aiida':
            # is_finished does not work for an aiida run
            print('retrieving stored aiida run')
            return self._read_results('')

        elif not self.is_finished(remotely=remotely):
            self._logger.warning('Calculation not completed yet')
            raise ValueError("Calculation not completed yet")

        files = self.resultfiles
        self.receive_files(files)

        if len(self.appended_functions) > 0:
            func = self.appended_functions[-1]
        else:
            func = self
        # Read results, with dependencies or not
        return func._read_results(self.local_directory)


class RemoteJSONPickleFunction(RemoteFunction):
    """Serialize and execute remotely a python function, serialized with
    json pickle.

    With this class we serialize and execute a python function
    on a remote filesystem. This filesystem may be a remote computer
    or a different directory of the local machine.

    Such class is useful to be employed in runners which needs to be executed
    outside of the current framework, but for which the result is needed to
    continue the processing of the data.

    Args:
        name (str): the name of the remote function
        function (func): the python function to be serialized.
            The return value of the function should be an object for which
            a relatively light-weight serialization is possible.
        submitter (str): the interpreter to be invoked. Should be, e.g.
            `python` if the function is a python function, or `bash`.
        required_files (list): list of extra files that may be required for
            the good running of the function.
        output_files (list): list of the files that the function will produce
            that are supposed to be retrieved to the host computer.
        **kwargs:  keyword arguments of the function.
            The arguments of the function should be serializable without
            the requirement of too much disk space.
    """
    def __init__(self, submitter, name, function, required_files=None,
                 output_files=None, **kwargs):

        if output_files is None:
            output_files = []
        if required_files is None:
            required_files = []

        self._logger = logging.getLogger(__name__ + '.' + 
                                         'RemoteJSONPickleFunction')
        self._logger.debug(f'{self.__class__.__name__} created with locals:')
        self._logger.debug(f'{format_iterable(locals())}')
        self.name = name
        self.submitter = submitter
        self.appended_functions = []
        self.required_files = required_files
        self.arguments = kwargs
        self.raw_function = function
        self.output_files = output_files

    def _set_arguments(self):
        from inspect import getsource
        self.encoded = {}
        self.encoded["fun"] = getsource(self.raw_function)
        self.encoded["fname"] = self.raw_function.__name__
        self.encoded["args"] = self.arguments

    def _serialize(self, run_dir):
        self._logger.debug('serialising a new JSONPickle run')
        from os.path import join
        from jsonpickle import encode
        self.serialized_file = self.name + "-serialize.json"
        serializedfile = join(run_dir, self.serialized_file)
        with open(serializedfile, "w") as ofile:
            ofile.write(encode(self.encoded))
        return [self.serialized_file] + self.required_files

    def _make_run(self, run_dir, dry_run=False):
        """
        Build the setup script for this run

        Arguments:
            run_dir (str):
                run directory
            dry_run (bool):
                create attributes only

        Returns:
            str:
                setup script to produce the correct files on the remote.
                resultfile name if dry_run
        """
        self.resultfile = self.name + '-result.json'
        self.runfile = self.name + "-run.py"
        self._logger.debug('making a new jsonpickle run. '
                           f'resultfile: {self.resultfile}, '
                           f'runfile: {self.runfile}')
        if dry_run:
            return self.resultfile
        pscript = ["# Run the serialized script\n"]
        pscript.append("from jsonpickle import decode, encode\n")
        pscript.append("with open(\""+self.serialized_file+"\" , \"r\")")
        pscript.append(" as ifile:\n")
        pscript.append("    dec = decode(ifile.read())\n")
        pscript.append("exec(dec['fun'])\n")
        pscript.append("result = locals()[dec['fname']](**dec['args'])\n")
        pscript.append("with open(\""+self.resultfile+"\" , "
                                                      "\"w\") as ofile:\n")
        pscript.append("    ofile.write(encode(result))\n")
        return ''.join(pscript)

    def _read_results(self, run_dir):
        from jsonpickle import decode
        from os.path import join
        rfile = join(run_dir, self.resultfile)
        self._logger.debug(f'reading results from file {rfile}')
        with open(rfile, "r") as ifile:
            res = decode(ifile.read())
        return res

    def append_function(self, extra_function):
        """!skip"""
        raise NotImplementedError('Cannot append a function.' +
                                  ' Use a RemoteScript to concatenate')


class RemoteDillFunction(RemoteFunction):
    """Serialize and execute remotely a python function, serialized with dill.

    With this class we serilize and execute a python function
    on a remote filesystem. This filesystem may be a remote computer
    or a different directory of the local machine.

    Such class is useful to be employed in runners which needs to be executed
    outside of the current framework, butfor which the result is needed to
    continue the processing of the data.

    Args:
        name (str): the name of the remote function
        function (func): the python function to be serialized.
            The return value of the function should be an object for which
            a relatively light-weight serialization is possible.
        submitter (str): the interpreter to be invoked. Should be, e.g.
            `python` if the function is a python function, or `bash`.
        required_files (list): list of extra files that may be required for
            the good running of the function.
        output_files (list): list of the files that the function will produce
            that are supposed to be retrieved to the host computer.
        **kwargs:  keyword arguments of the function.
            The arguments of the function should be serializable without
            the requirement of too much disk space.
    """
    def __init__(self, submitter, name, function, required_files=None,
                 output_files=None, **kwargs):

        if output_files is None:
            output_files = []
        if required_files is None:
            required_files = []

        self._logger = logging.getLogger(__name__ + '.' + 'RemoteDillFunction')
        self._logger.debug(f'{self.__class__.__name__} created with locals:')
        self._logger.debug(f'{format_iterable(locals())}')
        self.name = name
        self.submitter = submitter
        self.appended_functions = []
        self.required_files = required_files
        self.arguments = kwargs
        self.raw_function = function
        self.output_files = output_files

    def _set_arguments(self):
        self.function = _bind_closure(self.raw_function, **self.arguments)

    def _serialize(self, run_dir):
        self._logger.debug('serialising a new Dill run')
        from os.path import join
        from dill import dump
        self.serialized_file = self.name + "-serialize.dill"
        serializedfile = join(run_dir, self.serialized_file)
        with open(serializedfile, "wb") as ofile:
            dump(self.function, ofile, recurse=False)
        return [self.serialized_file] + self.required_files

    def _make_run(self, run_dir, dry_run=False):
        """
        Build the setup script for this run

        Arguments:
            run_dir (str):
                run directory
            dry_run (bool):
                create attributes only

        Returns:
            str:
                setup script to produce the correct files on the remote.
                resultfile name if dry_run
        """
        self.resultfile = self.name + '-result.dill'
        self.runfile = self.name + "-run.py"
        self._logger.debug('making a new dill run. '
                           f'resultfile: {self.resultfile}, '
                           f'runfile: {self.runfile}')
        if dry_run:
            return self.resultfile
        pscript = ["# Run the serialized script\n"]
        pscript.append("from dill import load, dump\n")
        pscript.append("with open(\""+self.serialized_file+"\" , \"rb\")")
        pscript.append(" as ifile:\n")
        pscript.append("    fun = load(ifile)\n")
        pscript.append("result = fun()\n")
        pscript.append("with open(\""+self.resultfile+"\" , "
                                                      "\"wb\") as ofile:\n")
        pscript.append("    dump(result, ofile)\n")
        return ''.join(pscript)

    def _read_results(self, run_dir):
        from dill import load
        from os.path import join
        rfile = join(run_dir, self.resultfile)
        self._logger.debug(f'reading results from file {rfile}')
        with open(rfile, "rb") as ifile:
            res = load(ifile)
        return res

    def append_function(self, extra_function):
        """!skip"""
        raise NotImplementedError('Cannot append a function.' +
                                  ' Use a RemoteScript to concatenate')


class RemoteJSONFunction(RemoteFunction):
    """Serialize and execute remotely a python function, serialized with JSON.

    With this class we serilize and execute a python function
    on a remote filesystem. This filesystem may be a remote computer
    or a different directory of the local machine.

    Such class is useful to be employed in runners which needs to be executed
    outside of the current framework, for which the result is needed locally to
    continue data processing.

    Args:
        name (str): the name of the remote function
        function (func): the python function to be serialized.
            The return value of the function should be an object for which
            a relatively light-weight serialization is possible.
        submitter (str): the interpreter to be invoked. Should be, e.g.
            `python` if the function is a python function, or `bash`.
        extra_encoder_functions (list)): list of dictionaries of the format
            {'cls': Class, 'func': function} which is employed to serialize
            non-instrinsic objects as well as non-numpy objects.
        required_files (list): list of extra files that may be required for
            the good running of the function.
        output_files (list): list of the files that the function will produce
            that are supposed to be retrieved to the host computer.
        **kwargs:  keyword arguments of the function.
            The arguments of the function should be serializable without
            the requirement of too much disk space.
    """
    def __init__(self, submitter, name, function, extra_encoder_functions=None,
                 required_files=None, output_files=None, **kwargs):

        if required_files is None:
            required_files = []
        if output_files is None:
            output_files = []
        if extra_encoder_functions is None:
            extra_encoder_functions = []

        self._logger = logging.getLogger(__name__ + '.' + 'RemoteJSONFunction')
        self._logger.debug(f'{self.__class__.__name__} created with locals:')
        self._logger.debug(f'{format_iterable(locals())}')
        from inspect import getsource
        self.name = name
        self.function = getsource(function)
        self.function_name = function.__name__
        self.extra_encoder_functions = extra_encoder_functions
        self.encoder_functions_serialization = {s['cls'].__name__:
                                                {'name': s['func'].__name__,
                                                 'source':
                                                 getsource(s['func'])}
                                                for s in
                                                extra_encoder_functions}
        self.required_files = required_files
        self.submitter = submitter
        self.appended_functions = []
        self.arguments = kwargs
        self.output_files = output_files

    def _set_arguments(self):
        from futile.Utils import serialize_objects
        self.arguments_serialization = serialize_objects(
            self.arguments, self.extra_encoder_functions)

    def _serialize(self, run_dir):
        self._logger.debug('serialising a new JSON run')
        from os.path import join
        from futile.Utils import create_tarball
        if len(self.required_files) + len(self.arguments_serialization) == 0:
            self.serialized_file = ''
            return []
        self.serialized_file = self.name + "-files.tar.gz"
        serializedfile = join(run_dir, self.serialized_file)
        create_tarball(serializedfile, [],
                       {k+'.json': v
                        for k, v in self.arguments_serialization.items()})
        return [self.serialized_file] + self.required_files

    def _make_run(self, run_dir, dry_run=False):
        """
        Build the setup script for this run

        Arguments:
            run_dir (str):
                run directory
            dry_run (bool):
                create attributes only

        Returns:
            str:
                setup script to produce the correct files on the remote.
                 resultfile name if dry_run
        """
        self.resultfile = self.name + '-result.json'
        self.runfile = self.name + "-run.py"
        self._logger.debug('making a new JSON run. '
                           f'resultfile: {self.resultfile}, '
                           f'runfile: {self.runfile}')
        pscript = ["kwargs = {}\n"]
        pscript.append("import json\n")
        if dry_run:
            return self.resultfile
        if self.serialized_file != '':
            pscript.append("# Unpack the argument tarfile if present\n")
            pscript.append("import tarfile\n")
            pscript.append("# extract the archive\n")
            pscript.append("arch = tarfile.open('" + self.serialized_file +
                           "')\n")
            pscript.append("#arch.extractall(path='.')\n")
            # pscript.append("files = arch.getnames()\n")
            for arg in self.arguments_serialization.keys():
                pscript.append("#with open('" + arg + ".json', 'r') as f:\n")
                pscript.append("with arch.extractfile('" + arg + ".json') as "
                                                                 "f:\n")
                pscript.append("    kwargs['" + arg + "'] = json.load(f)\n")
            pscript.append("arch.close()\n")
        pscript.append("extra_encoder_functions = []\n")
        for name, func in self.encoder_functions_serialization.items():
            pscript.append(func['source'])
            pscript.append("extra_encoder_functions.append({'cls'" + name +
                           ", 'func:'" + func['name'] + "})\n")
        pscript.append("class CustomEncoder(json.JSONEncoder):\n")
        pscript.append("    def default(self, obj):\n")
        pscript.append("        try:\n")
        pscript.append("            import numpy as np\n")
        pscript.append("            nonumpy = False\n")
        pscript.append("        except ImportError:\n")
        pscript.append("            nonumpy = True\n")
        pscript.append("        if not nonumpy:\n")
        pscript.append("            if isinstance(obj, (np.int_, np.intc,\n")
        pscript.append("                                np.intp, np.int8,\n")
        pscript.append("                                np.int16, np.int32,\n")
        pscript.append("                                np.int64, np.uint8,\n")
        pscript.append("                                np.uint16, "
                       "np.uint32,\n")
        pscript.append("                                np.uint64)):\n")
        pscript.append("                return int(obj)\n")
        pscript.append("            elif isinstance(obj, (np.float_, "
                       "np.float16,\n")
        pscript.append("                                  np.float32,\n")
        pscript.append("                                  np.float64)):\n")
        pscript.append("                return float(obj)\n")
        pscript.append("            elif isinstance(obj, (np.ndarray,)):\n")
        pscript.append("                return obj.tolist()\n")
        pscript.append("        if isinstance(obj, (set,)):\n")
        pscript.append("            return list(obj)\n")
        pscript.append("        else:\n")
        pscript.append("            for spec in extra_encoder_functions:\n")
        pscript.append("                if isinstance(obj, (spec['cls'],)):\n")
        pscript.append("                    return spec['func'](obj)\n")
        pscript.append("        return json.JSONEncoder.default(self, obj)\n")
        pscript.append(self.function)
        pscript.append("result = "+self.function_name+"(**kwargs)\n")
        pscript.append("with open(\""+self.resultfile+"\" , \"w\") as "
                                                      "ofile:\n")
        pscript.append("    json.dump(result, ofile, cls=CustomEncoder)\n")
        return ''.join(pscript)

    def _read_results(self, run_dir):
        from json import load
        from os.path import join
        rfile = join(run_dir, self.resultfile)
        self._logger.debug(f'reading results from file {rfile}')
        with open(rfile, "r") as ifile:
            res = load(ifile)
        return res

    def append_function(self, extra_function):
        """!skip"""
        raise NotImplementedError('Cannot append a function.' +
                                  ' Use a RemoteScript to concatenate')


if AIIDA_FLAG:
    class RemoteAiidaFunction(AiidaCalculator):
        """Pass a function to a remote machine using the AiiDA infrastructure

        """

        def __init__(self, name, **kwargs):
            self._logger = logging.getLogger(__name__ + '.' +
                                             'RemoteAiidaFunction')
            self._logger.debug(f'{self.__class__.__name__} created')
            self.name = name
            self.remotely = False  # yes, but also no
            self.resultfile = AIIDA_FLAG
            self.output_files = []

            # convert kwargs into args used by AiidaCalculator
            # TODO(lbeal): find a more elegant way of doing this
            AiiDA_arg_translate = {'mpi_procs_per_machine': 'NMPIVAR',
                                   'omp': 'NOMPVAR',
                                   }
            self.AiiDA_args = {'code': 'bigdft@localhost'}
            for a, k in AiiDA_arg_translate.items():
                if k in kwargs:
                    self.AiiDA_args[a] = kwargs.get(k)

        def setup(self, **kwargs):
            """Create a remote Aiida Function by passing values to constructor
            """
            super().__init__(**self.AiiDA_args)
            # a dict containing files to send is expected, return empty dict
            return {}

        def call(self, **kwargs):
            """Usually provides the command to execute the function.

            In this case, calling is handled by AiiDA,
            so is just a placeholder.

            Args:
                kwargs: Dummy holder to accept keyword args.

            Returns:
                str: empty str, calling is handled by aiida
            """

            return ''

        def process_run(self, **kwargs):
            # don't run if we don't have to
            # TODO(lbeal): add an alternative "if run_options['skip']:"
            if hasattr(self, '_result'):
                return {'status': 'finished_remotely'}

            # because of name mangling this process_run takes priority over
            # the one in AiidaCalculator. Call that one instead if needed
            inp = kwargs.get('input', None)
            if inp is None:
                return super().process_run(**kwargs)
            # call the run method of the aiida calculator
            self._result = self.run(**kwargs)

            return {'status': 'submitted'}

        def _read_results(self):

            return self._result


class RemoteScript(RemoteFunction):
    """Triggers the remote execution of a script.

    This class is useful to execute remotely a script and to retrieve.
    The results of such execution. It inherits from the `RemoteFunction`
    base class and extends some of its actions to the concept of the script.

    Args:
        name (str): the name of the remote function
        script (str, func): The script to be executed provided in string form.
            It can also be provided as a function which returns a string.
        result_file(str): the name of the file in which the script
            should redirect.
        submitter (str): the interpreter to be invoked. Should be, e.g.
            `bash` if the script is a shell script, or 'qsub' if this is a
            submission script.
        output_files (list): list of the files that the function will produce
            that are supposed to be retrieved to the host computer.
        **kwargs:  keyword arguments of the script-script function,
            which will be substituted in the string representation.
    """
    def __init__(self, submitter, name, script, result_file, output_files,
                 **kwargs):
        self._logger = logging.getLogger(__name__ + '.RemoteScript')
        self._logger.debug(f'{self.__class__.__name__} created with locals:')
        self._logger.debug(f'{format_iterable(locals())}')
        self.name = name
        self.script = script
        self.submitter = submitter
        self.resultfile = result_file
        self.arguments = kwargs
        self.appended_functions = []
        self.output_files = output_files

    def _set_arguments(self):

        if isinstance(self.script, str):
            scr = self.script
            for key, value in self.arguments.items():
                scr = scr.replace(key, str(value))
            self.script = scr
        else:
            self.script = self.script(**self.arguments)

    def _read_results(self, run_dir):
        if self.protocol == 'aiida':  # dirty deferrence
            return self.remote_function._read_results()
        from os.path import join
        with open(join(run_dir, self.resultfile), 'rb') as ifile:
            res = [line.decode('utf-8') for line in ifile.readlines()]
        return res

    def _make_run(self, run_dir):
        self.runfile = self.name + "-run.sh"
        self._logger.info(f'making run with runfile {self.runfile}, '
                          'and script:')
        yaml_script = '\n  '.join(self.script.split('\n'))
        self._logger.info(f'|\n{yaml_script}')
        return self.script


class CallableAttrDict(dict):
    """
    Dict-form structure where the contents are accessible as attributes

    Example:
        >>> d = CallableAttrDict({'a': 1})
        >>> print(d.a)
        >>> 1
        >>> print (d())
        >>> "{'a': 1}"
        >>> d.a = 2
        >>> print (d())
        >>> "{'a': 2}"
    """
    def __init__(self, *args, **kwargs):
        super(CallableAttrDict, self).__init__(*args, **kwargs)
        self.__dict__ = self

    def __call__(self, **kwargs):
        self.update(kwargs)
        return str(self)
