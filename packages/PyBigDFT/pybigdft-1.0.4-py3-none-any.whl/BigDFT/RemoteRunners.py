"""
This module wraps the classes and functions you will need if you want to run
PyBigDFT operations on a remote machine.
"""
import datetime
import pprint

try:
    from BigDFT.AiidaCalculator import AiidaCalculator  # noqa F401
    AIIDA_FLAG = True
    from BigDFT.RemoteRunnerUtils import RemoteAiidaFunction
except ModuleNotFoundError:
    AIIDA_FLAG = False
from BigDFT.RemoteRunnerUtils import RemoteScript, \
    RemoteJSONFunction, \
    RemoteDillFunction, \
    RemoteJSONPickleFunction, \
    CallableAttrDict
from BigDFT.Calculators import Runner
from BigDFT.Datasets import Dataset
from BigDFT.URL import URL

import logging
from BigDFT.LogUtils import format_iterable
import os


# create and link logger
module_logger = logging.getLogger(__name__)


def _ensure_url(url, verbose=False):
    """make sure the URL is an actual class

    Arguments:
        url (str, URL):
            url to be enforced to BigDFT.URL

    Returns:
        URL
    """
    if url is None:
        return URL()

    if not isinstance(url, URL):
        # now require a URL handler for remote operations
        # create one if needed
        # warnings.DeprecationWarning is ignored by default, just print
        print('Warning: Explicit url expression is to be deprecated. '
              'Create a url using BigDFT.URL.')
        module_logger.warning('creating url class from string. Explicitly '
                              'create from BigDFT.URL() to be future-proof.')
        url = URL.from_string(url)

        url.verbose = verbose

    return url


class RemoteRunner(Runner, RemoteScript):
    """
    This class can be used to run python functions on a remote machine. This
    class combines the execution of a script with a python remote function.

    Args:

        function (callable): the python function to be serialized.
            The return value of the function should be an object for which
            a relatively light-weight serialization is possible.
        func (callable):
            alias for function
        name (str): the name of the remote function. Function name is employed
            if not provided.
        script (str): The script to be executed provided in string form.
            The result file of the script is assumed to be named
            `<name>-function-result`.
        submitter (str): the interpreter to be invoked. Should be, e.g.
            `bash` if the script is a shell script, or `qsub` if this is a
            submission script.
        url (str, URL): either a user@host string
            or URL() connection class (preferable)
        remote_dir (str): the path to the work directory on the remote machine.
           Should be associated to a writable directory.
        skip (bool): if true, we perform a lazy calculation.
        asynchronous (bool): If True, submit the calculation without waiting
           for the results.
        local_dir (str): local directory to prepare the IO files to send.
            The directory should exist and write permission should
            be granted.
        python (str): python interpreter to be invoked in the script.
        protocol (str): serialization method to be invoked for the function.
            can be 'JSON' or 'Dill' or 'JSONPickle', depending of the desired
            version.
        extra_encoder_functions (list)): list of dictionaries of the format
            {'cls': Class, 'func': function} which is employed to serialize
            non-instrinsic objects as well as non-numpy objects. Useful for
            the 'JSON' protocol.
        required_files (list): list of extra files that may be required for
            the good running of the function.
        output_files (list): list of the files that the function will produce
            that are supposed to be retrieved to the host computer.
        arguments (dict):  keyword arguments of the function.
            The arguments of the function should be serializable without
            the requirement of too much disk space. Such arguments cannot
            be named in the same way as the others.
        **kwargs (dict):  Further keyword arguments of the script,
            which will be substituted in the string representation.

    RemoteRunner exists to allow transfer of generic python functions to a
    remote system. Functions will be serialised via the user specified format
    and transferred over along with their arguments.

    Consider a simple function:

    >>> def test_func(arg):
    >>>     return arg

    This function can be run on a remote machine using RemoteRunner, as shown
    in the following example:

    Lets assume we have access to a remote machine with the ip address

    ``192.168.0.0``

    First, construct a URL connection to this machine using the URL module

    >>> from BigDFT.URL import URL
    >>> url = URL(user='user', host='192.168.0.0')

    Now give this, and the function as an argument to the RemoteRunner,
    along with any arguments required:

    >>> from BigDFT.RemoteRunners import RemoteRunner
    >>> remote_run = RemoteRunner(function = test_func,
    >>>                           url = url,
    >>>                           arguments={'arg':'This is a test argument'})

    Run your code with the ``run()`` method, then results can be retreived
    using the ``fetch_results()`` method. Whether or not a run has finished
    can be determined used the ``is_finished()`` method.

    >>> remote_run.run()
    >>> import time
    >>> # while we don't have a finished run, wait
    >>> while not remote_run.is_finished():
    >>>     time.sleep(1)
    >>> result = remote_run.fetch_result()
    >>> print(result)
    >>> 'This is a test argument'

    You now have the basic ingredients to begin running generic functions on
    remote machines. There is obviously more to these methods, but see their
    documentation for further details.
    """

    def __init__(self,
                 function=None,
                 func=None,
                 submitter='bash',
                 name=None,
                 url=None,
                 skip=False,
                 asynchronous=True,
                 remote_dir='.',
                 rsync='',
                 local_dir='.',
                 script="#!/bin/bash\n",
                 python='python',
                 arguments=None,
                 protocol='JSON',
                 extra_encoder_functions=None,
                 required_files=None,
                 output_files=None,
                 **kwargs):

        if arguments is None:
            arguments = {}
        if output_files is None:
            output_files = []
        if required_files is None:
            required_files = []
        if extra_encoder_functions is None:
            extra_encoder_functions = []
        if function is None and func is not None:
            function = func

        # create logger and log message including init arguments
        self._logger = logging.getLogger(__name__ + '.RemoteRunner')
        logstr_exclude = ['self', '__class__']
        logstr = format_iterable(locals(), logstr_exclude)
        self._logger.info('create RemoteRunner with initial args: ')
        self._logger.info(logstr)

        # un-called scripts may cause issues further down the line, make sure
        # the user calls them when passing
        try:
            if issubclass(script, CallableAttrDict):
                raise ValueError('CallableAttrDict based script has not been '
                                 'called. Try changing script = scr to '
                                 'script = scr()\nThough be aware, only the '
                                 '__str__() method will have any affect')
        except TypeError:
            pass

        if isinstance(script, CallableAttrDict):
            # this block should pull anything set within a callable script and
            # override any base arguments
            print('extracting attributes from callable script')

            script_kwargs = script.__dict__

            function = script_kwargs.pop('function', function)
            func = script_kwargs.pop('func', func)
            submitter = script_kwargs.pop('submitter', submitter)
            name = script_kwargs.pop('name', name)
            url = script_kwargs.pop('url', url)
            skip = script_kwargs.pop('skip', skip)
            asynchronous = script_kwargs.pop('asynchronous', asynchronous)
            rsync = script_kwargs.pop('rsync', rsync)
            remote_dir = script_kwargs.pop('remote_dir', remote_dir)
            local_dir = script_kwargs.pop('local_dir', local_dir)
            python = script_kwargs.pop('python', python)
            arguments = script_kwargs.pop('arguments', arguments)
            protocol = script_kwargs.pop('protocol', protocol)
            extra_encoder_functions = \
                script_kwargs.pop('extra_encoder_functions',
                                  extra_encoder_functions)
            required_files = script_kwargs.pop('required_files',
                                               required_files)
            output_files = script_kwargs.pop('output_files', output_files)

            kwargs.update(script_kwargs)

        self.protocol = protocol.lower()  # remove case sensitivity
        # get verbose from kwargs, default True
        self.verbose = kwargs.get('verbose', True)
        url = _ensure_url(url, self.verbose)

        if rsync == '':  # update rsync based on verbosity if not specified
            self._logger.debug(f'no rsync set, and verbose is {self.verbose}')
            if self.verbose:
                rsync = '-auv'
            else:
                rsync = '-auq'
        url.rsync_flags = rsync
        self.url = url
        # creation and run times
        self._times = {'ctime': datetime.datetime.now(),
                       'rtime': None}
        self._wait = None
        self._wait_args = None

        if function is None:  # function is always AiidaCalculator for aiida
            if self.protocol != 'aiida':
                raise ValueError('Function can only be '
                                 'None for AiiDA based runs')
            if name is None:  # set name if none specified
                name = 'AiiDA-calc'
        if name is None:
            name = function.__name__
        super().__init__(submitter=submitter, name=name, script=script,
                         result_file=name + '-function-result',
                         url=url, skip=skip, asynchronous=asynchronous,
                         remote_dir=remote_dir, local_dir=local_dir,
                         protocol=self.protocol, python=python,
                         extra_encoder_functions=extra_encoder_functions,
                         required_files=required_files, function=function,
                         arguments=arguments, output_files=output_files,
                         **kwargs)
        self.remote_function = self._create_remote_function(
            name, self._global_options)
        self.append_function(self.remote_function)

    def __eq__(self, other):
        """
        test if this runner is the same as other

        used for preventing a self-wait

        should use more than ctime, may not be robust
        """
        if not isinstance(self, type(other)):
            raise ValueError(f'cannot compare with {type(other)}')

        return self.ctime == other.ctime

    def _create_remote_function(self, name, options):
        # self._logger.debug(f'creating the remote function {name} w/ options:'
        #                    f' {format_iterable(options)}')
        rfargs = {'submitter': options['python'],
                  'name': name + '-function',
                  'function': options['function'],
                  'required_files': options['required_files']}
        protocol = options['protocol']

        dispatch = {'json': RemoteJSONFunction,
                    'dill': RemoteDillFunction,
                    'jsonpickle': RemoteJSONPickleFunction}
        if AIIDA_FLAG:  # if aiida is in the env, add it to the dispatch table
            dispatch['aiida'] = RemoteAiidaFunction
        if protocol not in dispatch:
            raise ValueError('protocol must be one of',
                             list(dispatch.keys()))

        cls = dispatch[protocol]
        if protocol == 'json':
            rfargs.update(options['extra_encoder_functions'])
        if protocol == 'aiida':
            update = ['NMPIVAR', 'NOMPVAR']
            for key in [k for k in update if k in options]:
                print(f'passed key {key} to remote')
                rfargs[key] = options[key]

        # all the keys of the instantiated class so far are protected.
        self.protected_arguments = list(rfargs.keys())
        reargs = self._check_protected_arguments(options['arguments'])
        rfargs.update(reargs)
        return cls(**rfargs)

    def _check_protected_arguments(self, args):
        for arg in args:
            if arg in self.protected_arguments:
                raise ValueError("Keyword argument '" + arg +
                                 "' cannot be named this way (name clashing)")
        return args

    def pre_processing(self):
        """Ensure protected arguments, and gather the files to send."""
        reargs = self._check_protected_arguments(self.run_options['arguments'])
        self.remote_function.arguments = reargs
        if hasattr(self, 'directories_ensured') and self.directories_ensured:
            pass
        else:
            self.url.ensure_dir(self.run_options['local_dir'],
                                force_local=True)
            self.url.ensure_dir(self.run_options['remote_dir'])
            self.directories_created(True)
        if hasattr(self, 'files_to_send'):
            files_to_send = self.files_to_send
        else:
            files_to_send = self.setup(dest=self.run_options['remote_dir'],
                                       src=self.run_options['local_dir'])

        if hasattr(self, 'files_have_been_received'):
            skip = self.remote_function.arguments.get('skip', None)
            force = self.remote_function.arguments.get('force', None)

            if force or (not skip):
                self._logger.debug('we are not skipping (or forcing a run), '
                                   'but files_have_been_received has been set'
                                   '. Deleting this attribute.')
                delattr(self, 'files_have_been_received')

        self._logger.debug('preprocessing completed with run_args: ')
        self._logger.debug(f'{format_iterable(self.remote_function.arguments)}'
                           )

        return {'files': files_to_send}

    def _get_opts(self, opts):
        return {key: self.run_options[key] for key in opts}

    def process_run(self, files):
        """
        Run the calculations.

        Most skip/force/async logic is evaluated here.
        """
        if self._wait is not None:
            if isinstance(self._wait, type(RemoteDataset)):
                self._logger.info('awaiting previous remotedataset')
                cont = self._wait.all_finished(**self._wait_args)
            else:
                self._logger.info('awaiting previous runner')
                cont = self._wait.is_finished(**self._wait_args)

            if not cont:
                self._logger.info('previous run is not complete, waiting')
                print('previous run is not complete! Skipping this run')
                return {'status': 'waiting'}

        # allow passing of anyfile option, default to False
        anyfile = self.run_options.get('anyfile', True)
        # if force, disable skip
        force = self.run_options.get('force', False)
        self._times['rtime'] = datetime.datetime.now()
        if self.protocol == 'aiida':
            return self.remote_function.process_run(**self.local_options)
        if self.run_options['skip'] and not force and self.url.local:
            self._logger.debug('skip command active, checking '
                               'for finished run locally')
            if self.is_finished(remotely=False,
                                anyfile=anyfile,
                                verbose=False):
                # touch the files to prevent infinite is_finished() loops
                rfile = os.path.join(self.local_directory, self.resultfile)
                self._logger.debug(f'touching file {rfile} to prevent rerun')
                self.url.cmd(f'touch {rfile}')
                return {'status': 'finished_locally'}
        self.send_files(files)
        if self.run_options['skip'] and not force:
            self._logger.debug('skip command active, checking '
                               'for finished run remotely')
            if self.is_finished(anyfile=anyfile, verbose=False):
                rfile = os.path.join(self.remote_directory, self.resultfile)
                self._logger.debug(f'touching file {rfile} to prevent rerun')
                self.url.cmd(f'touch {rfile}')
                return {'status': 'finished_remotely'}
        self._logger.debug('beginning run prep')
        command = self.call()
        run_command = not self.run_options.get('get_command', False)
        if run_command:
            asynchronous = False
            if self.run_options['asynchronous'] and self.url.local:
                asynchronous = True  # command += ' &'
            self._logger.debug(f'running calc with command "{command}" and '
                               f'asynchronous: {asynchronous}')
            self.url.cmd(command, asynchronous=asynchronous)
            return {'status': 'submitted'}
        else:
            return {'status': 'lazy='+command}

    def post_processing(self, files, status):
        """Fetch the results for finished runs if async. All runs if not."""
        if self.protocol == 'aiida':
            return self.remote_function._result
        # retrieve the command only if the run is declared as lazy
        if status.startswith('lazy='):
            return '='.join(status.split('=')[1:])
        if self.run_options['asynchronous']:
            if status == 'finished_locally':
                if self.verbose:
                    print('Data are retrieved from local directory')
                return self.fetch_result(remotely=False)
            elif status == 'finished_remotely':
                return self.fetch_result(remotely=True)
        else:
            return self.fetch_result()

    def wait(self, other, **kwargs):
        """
        set another runner to wait for prior to a run

        call this before the run, passing a runner or dataset to await

        >>> dataset = RemoteDataset(...)
        >>> runner = RemoteRunner(...)
        >>>
        >>> runner.wait(dataset)
        >>> # runner will now wait for dataset to finish

        Args:
            other (RemoteRunner, RemoteDataset):
                previous runner or dataset to wait upon
            kwargs:
                further args to be passed to the is_finished method
        """
        if self == other:
            raise ValueError('awaiting self would render the runner unable '
                             'to run!')

        self._wait = other
        self._wait_args = kwargs

        self._logger.info('wait is set for this runner')

    @property
    def ctime(self) -> datetime.datetime:
        """
        Returns (datetime.datetime):
            creation time
        """
        return self._times['ctime']

    @property
    def rtime(self) -> datetime.datetime:
        """
        Returns (datetime.datetime):
            run time
        """
        return self._times['rtime']


class RemoteDataset(Dataset):
    """
    Defines a set of remote runs, to be executed from a base script and to
    a provided url. This class is associated to a set of remote submissions,
    which may contain multiple calculations. All those calculations are
    expressed to a single url, with a single base script, but with a collection
    of multiple remote runners that may provide different arguments.

    Args:
        label (str): man label of the dataset.
        run_dir (str): local directory of preparation of the data.
        database_file (str): name of the database file to keep track of the
            submitted runs.
        force (str): force the execution of the dataset regardless of the
            database status.
        **kwargs: global arguments of the appended remote runners.
    """
    def __init__(self, label='RemoteDataset', run_dir='/tmp',
                 database_file='database.yaml', force=False,
                 **kwargs):
        Dataset.__init__(self, label=label, run_dir=run_dir, force=force,
                         **kwargs)
        self._logger = logging.getLogger(__name__ + '.RemoteDataset')
        self._logger.debug(f'creating database at {database_file}')

        self.database = RunsDatabase(database_file)
        self._logger.debug('looking for protocol in args')
        self.protocol = kwargs.get('protocol', None)
        self._logger.debug(f'{self.protocol}')

        self._logger.debug('looking for verbose in args')
        self.verbose = kwargs.get('verbose', True)
        self._logger.debug(f'{self.verbose}')

        self.url = _ensure_url(kwargs.get('url', None), self.verbose)
        self.set_postprocessing_function(submit_remote_script)

    def append_run(self, id, remote_runner=None, **kwargs):
        """Add a remote run into the dataset.

        Append to the list of runs to be performed the corresponding runner and
           the arguments which are associated to it.

        Args:
          id (dict): the id of the run, useful to identify the run in the
             dataset. It has to be a dictionary as it may contain
             different keyword. For example a run might be classified as
             ``id = {'hgrid':0.35, 'crmult': 5}``.
          remote_runner (RemoteRunner): a instance of a remote runner that will
              be employed.
          **kwargs: arguments required for the creation of the corresponding
              remote runner. If remote_runner is provided, these arguments will
              be They will be combined with the global arguments.

        Raises:
          ValueError: if the provided id is identical to another previously
             appended run.
        """
        self._logger.info(f'appending run at id {id} with kwargs ')
        self._logger.info(f'{format_iterable(kwargs)}')
        from os.path import join
        # first fill the internal database
        # 'inp' causes problems with aiida, must translate to 'input'
        if 'inp' in kwargs.get('arguments', {}) and self.protocol == 'aiida':
            vals = kwargs['arguments'].pop('inp')
            kwargs['arguments']['input'] = vals
        Dataset.append_run(self, id, Runner(), **kwargs)
        # then create the actual remote runner to be included
        self._logger.debug('creating runner for this run')
        inp = self.runs[-1]
        local_dir = inp.get('local_dir')
        if local_dir is not None:
            basedir = join(self.get_global_option('run_dir'), local_dir)
        else:
            basedir = self.get_global_option('run_dir')
        inp['local_dir'] = basedir
        # for some reason a prior RemoteRunner.run() can add it's own output
        # file here. Force it to be empty.
        # inp['output_files'] = []
        name = self.names[-1]
        # the arguments have to be substituted before the run call
        if remote_runner is not None:
            self._logger.debug('pre-specified runner given in args')
            remote_script = remote_runner
            remote_script.name = name
        else:
            remote_script = RemoteRunner(name=name, **inp)
        self._logger.info(f'added runner {remote_script} with name {name}')
        self.calculators[-1]['calc'] = remote_script

    def _get_info_from_runner(self, irun, info):
        run_inp = self.runs[irun]
        remote_runner = self.calculators[irun]['calc']
        val = run_inp.get(info, remote_runner._global_options.get(info))
        return val

    def _get_local_run_info(self, irun, info):
        return self.run_options.get(info, self._get_info_from_runner(irun,
                                                                     info))

    def pre_processing(self):
        """
        Setup datasets prior to run. Gather and send data to the runners

        For each appended runner: Register them within the database,
        collect the files to be sent then send the files to the run directory
        """
        self._logger.info('preprocessing datasets')
        from warnings import warn
        # gather all the data to be sent
        files_to_send = {}
        selection = []
        force = self.run_options['force']
        self._logger.debug(f'force is set to {force}, commencing itemisation')
        remote_dirs = set()
        local_dirs = set()
        for irun, (name, calc) in enumerate(zip(self.names, self.calculators)):
            # Check the database.
            do_it = True
            if not force:
                if self.database.exists(name):
                    run_dir = self.get_global_option('run_dir')
                    warnmsg = f'({name}, {run_dir}) already submitted'
                    self._logger.warning(warnmsg)
                    warn(warnmsg, UserWarning)
                    do_it = False
            if do_it:
                selection.append(irun)
            else:
                continue
            remote_runner = calc['calc']
            remote_dir = self._get_info_from_runner(irun, 'remote_dir')
            local_dir = self._get_info_from_runner(irun, 'local_dir')
            # ensure the remote and local_directories
            if remote_dir not in remote_dirs:
                self.url.ensure_dir(remote_dir)
            if local_dir not in local_dirs:
                self.url.ensure_dir(local_dir, force_local=True)
            remote_dirs.add(remote_dir)
            local_dirs.add(local_dir)
            if remote_dir not in files_to_send:
                files_to_send[remote_dir] = []
            files_to_send[remote_dir].extend(remote_runner.setup(
                dest=remote_dir, src=local_dir))
            remote_runner.directories_created(True)

        # then send the data and mark them as sent.
        self._logger.info('files to send before run: ')
        self._logger.info(f'{format_iterable(files_to_send)}')
        for remote, files in files_to_send.items():
            self.url.rsync(files, local_dir, remote)
        for irun, calc in enumerate(self.calculators):
            self.calculators[irun]['calc'].files_sent(True)
        self.selection = selection
        return {}

    def process_run(self):
        """Run the dataset, by performing explicit run of each of the item of
        the runs_list.
        """
        self._logger.info('running and registering calcs')
        self._run_the_calculations(selection=self.selection,
                                   extra_run_args={'get_command': True})
        # Also, update the database informing that
        # the data should run by now.
        for irun, name in enumerate(self.names):
            if irun not in self.selection:
                continue
            self.database.register(name)
        return {}

    def _get_dataset_run_status(self, retrieve_nonetheless=False):
        """Retrieve the information of which resultfiles are available."""
        results = {}
        files_list = {'local': {}, 'remote': {}}
        self._logger.debug('getting dataset run status')
        for irun, calc in enumerate(self.calculators):
            if irun in self.selection or True:
                locdir = self._get_local_run_info(irun, 'local_dir')
                remdir = self._get_local_run_info(irun, 'remote_dir')
                dirs = {'local': locdir, 'remote': remdir}
                if not hasattr(calc['calc'], 'resultfiles'):
                    self._logger.debug('calc does not have resultfiles attr')
                    calc['calc'].setup(src=locdir, dest=remdir)
                    calc['calc'].directories_created(True)
                    calc['calc'].files_sent(True)
                # get the file list if not known already
                self._logger.debug('getting file list')
                for place, dd in dirs.items():
                    self._logger.debug(f'place: {place}, dd: {dd}')
                    if dd is None:
                        continue
                    if dd not in files_list[place]:
                        files_list[place][dd] = self.url.ls(
                            dd, local=place == 'local')
                    # get the files that are present
                    resultfiles = calc['calc'].resultfiles
                    # print (irun,dd,calc['calc'].resultfile)
                    self._logger.info(f'files list for {place} in dir {dd}')
                    self._logger.info(format_iterable(files_list[place][dd]))
                    self._logger.info('resultfiles: ')
                    self._logger.info(f'{format_iterable(resultfiles)}')
                    results.setdefault(irun, {}).setdefault(
                        place, (dd, set(
                            [f for f in resultfiles
                             if place == 'remote' or f in files_list[place][dd]
                             ])))

        self._logger.info('list of resultfiles:')
        self._logger.info(f'{format_iterable(results)}')
        # organize the pool of transfers which may be required
        transfers = {}
        to_transfer = []
        for irun, res in results.items():
            if 'remote' not in res:
                continue
            remote = res['remote'][0]
            local = res['local'][0]
            flist = [f for f in res['remote'][1]
                     if f not in res['local'][1] or retrieve_nonetheless]
            self._logger.info(f'irun: {irun} flist: {flist}')
            if len(flist) > 0:
                transfers.setdefault((remote, local), []).extend(flist)
                to_transfer.append(irun)

        self.transfers = {k: set(v) for k, v in transfers.items()}
        if hasattr(self, 'to_transfer'):
            self.to_transfer.union(set(to_transfer))
        else:
            self.to_transfer = set(to_transfer)

        ready = {}
        for irun in results:
            rfile = self.calculators[irun]['calc'].resultfile
            self._logger.debug(f'checking resultfile for run {irun}: {rfile}')

            remotefld = results[irun].get('remote')[0]
            self._logger.debug(f'looking in folder {remotefld}')
            remotefiles = files_list['remote'][remotefld]

            self._logger.debug(remotefiles)

            ready[irun] = rfile in remotefiles

        self._logger.info('transfers to be issued:')
        self._logger.info(f'{format_iterable(self.transfers)}')
        return ready

    def _issue_data_transfer(self):
        self._logger.info('issuing data transfer for files')
        self._logger.info(pprint.pformat(self.transfers))
        for (remote, local), flist in self.transfers.items():
            self.url.rsync(flist, local, remote, push=False)
        self.transfers = {}
        getattr(self, 'transferred', set()).union(self.to_transfer)
        delattr(self, 'to_transfer')

    def is_finished(self, anyfile=True, verbose=False, timeout=-1):
        """Returns all() of is_finished methods of each runner present

        Args:
            anyfile (bool):
                Checks for file recency if False
            verbose (bool):
                Will not print checking status if False
            timeout (int):
                Number of times each is_finished call can fail before raising
                an error. -1 to disable (Default)

        Returns:
            dict: {irun: finished}
        """
        logstr = ['### New call: Checking for finished dataset:',
                  f'anyfile: {anyfile},',
                  f'timeout: {timeout}']
        self._logger.debug(' '.join(logstr))
        previous_verbosity = self.url.verbose

        if verbose != previous_verbosity:
            self.url.verbose = verbose

        if timeout >= 0:
            self._is_finished_timeout = timeout

        fin = self._get_dataset_run_status(retrieve_nonetheless=anyfile)
        self._logger.info(f'fin: {fin}')
        self.url.verbose = previous_verbosity
        return self._is_finished_finalise(fin)

    def _is_finished_finalise(self,
                              fin: [dict, bool]) -> [dict, bool]:
        """
        called by is_finished before a return to ensure that the `timeout`
        argument is respected

        Args:
            fin (dict, bool):
                actual is_finished result. This function just handles the
                accounting
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
        if isinstance(fin, dict) and all(fin.values()):
            # disable timeout after a successful run
            self._is_finished_timeout = -1
            self._is_finished_calls = 0
        elif isinstance(fin, bool) and fin:
            self._is_finished_timeout = -1
            self._is_finished_calls = 0

        return fin

    def all_finished(self,
                     anyfile: bool = True,
                     verbose: bool = False,
                     timeout: int = -1) -> bool:
        """
        Returns all() of is_finished methods of each runner present

        Args:
            anyfile (bool):
                Checks for file recency if False
            verbose (bool):
                Will not print checking status if False
            timeout (int):
                Number of times each is_finished call can fail before raising
                an error. -1 to disable (Default)

        Returns:
            bool: True if all runs have finished
        """
        self._logger.debug('checking if all runs have finished')

        if timeout >= 0:
            self._is_finished_timeout = timeout

        files = {}
        for run in self.calculators:
            calc = run['calc']

            remote_dir = calc.remote_directory
            resultfile = calc.resultfile

            file = os.path.join(remote_dir, resultfile)

            files[file] = calc.rtime.timestamp()

        cmd = 'ls {' + ','.join(files) + '}'
        self._logger.info('checking presence of resultfiles')
        presence = self.url.cmd(cmd).split('\n')[:-1]

        all_present = presence == list(files.keys())

        if not all_present:
            self._logger.info('files are missing, False')
            # not all the files are on the remote, return
            return self._is_finished_finalise(False)
        elif anyfile:
            self._logger.info('all the files are there, skipping time check')
            # all the files are there and we don't care about times
            return self._is_finished_finalise(True)

        cmd = 'stat -c %Y {' + ','.join(files) + '}'

        times = [int(t) for t in self.url.cmd(cmd).split('\n') if t != ""]

        total_runtime = sum([int(t) for t in files.values()])
        total_restime = sum(times)

        self._logger.info(f'total run init time is {total_runtime}')
        self._logger.info(f'total result time is {total_restime}')

        if total_runtime <= total_restime:
            self._logger.info('sum of times is above sum of run times, True')
            return self._is_finished_finalise(True)

        self._logger.info('files are outdated')
        return self._is_finished_finalise(False)

    def fetch_results(self,
                      id=None, lookup=None):
        """Retrieve some attribute from some of the results.

        Selects out of the results the objects which have in their ``id``
        at least the dictionary specified as input. May return an attribute
        of each result if needed.

        Args:
           id (dict): dictionary of the retrieved id. Helps in constructing
               a list of the runs that have the ``id`` argument inside
               the provided ``id`` in the order provided by
               :py:meth:`append_run`.
               If absent, then the entire list of runs is returned.
           lookup (list): list of the runs which will have to be retrieved
               in the order provided by :py:meth:`append_run`.
        """
        from BigDFT.Datasets import names_from_id
        self._logger.info('fetching dataset results')
        if not hasattr(self, 'transfers'):
            self._logger.info('missing transfer attribute, '
                              'running is_finished')
            finished = self.is_finished(verbose=self.verbose)
            lup = [k for k, v in finished.items() if v]
            if lookup is None:
                lookup = lup
        if lookup is not None:
            fetch_indices = lookup
        elif id is None:
            fetch_indices = list(range(len(self.names)))
            self._logger.debug('no id specified, indices are:')
            self._logger.debug(f'{format_iterable(fetch_indices)}')
        else:
            names = names_from_id(id)
            fetch_indices = []
            for irun, name in enumerate(self.names):
                # add the separator ',' to have the proper value of a key
                # (to avoid 0.3 in 0.39)
                if not all([(n in name+'__') for n in names]):
                    continue
                fetch_indices.append(irun)
            self._logger.debug(f'specified id: {format_iterable(id)}')
            self._logger.debug('indices are:')
            self._logger.debug(f'{format_iterable(fetch_indices)}')
        self._logger.debug('retreiving results...')

        # check that any local files are more recent than the previous run
        self.to_transfer = []
        self.transfers = {}
        for irun in fetch_indices:
            calc = self.calculators[irun]['calc']

            local_dir = calc.local_directory
            resultfiles = calc.resultfiles

            for resultfile in resultfiles:
                local_result = os.path.join(local_dir, resultfile)

                # if there's no runfile locally, append to transfers
                if not os.path.isfile(local_result):
                    self._logger.debug(f'result for run {irun} is not present')
                    append = True

                else:
                    # file, check if it's recent
                    rtime = calc.rtime
                    ftime = os.path.getmtime(local_result)
                    append = False
                    if rtime is None or ftime < rtime.timestamp():
                        self._logger.debug(
                            f'result for run {irun} is not recent')
                        append = True

                if append:  # if this file is marked for collection, add it
                    remote_dir = calc.remote_directory
                    key = (remote_dir, local_dir)

                    self.transfers.setdefault(key, set()).add(resultfile)
                    if irun not in self.to_transfer:
                        self.to_transfer.append(irun)
        # if len(to_transfer) != 0:
        #     self._logger.debug('joining transfer lists')
        #     self.to_transfer = self.to_transfer | set(to_transfer)
        if len([self.to_transfer]) > 0:
            self._issue_data_transfer()

        # then get the results of the indices to be fetched
        data = []
        for irun in fetch_indices:
            calc = self.calculators[irun]['calc']
            calc.files_received(True)
            data.append(calc.fetch_result(remotely=False))
        return data

    def clear_results(self,
                      selection: list = None,
                      verbose: bool = True):
        """
        delete local result files

        Args:
            selection (list):
                optional list to select results from
            verbose (bool):
                verbosity flag
        """

        if selection is None:
            self._logger.info('wiping results files with no selection')
            selection = range(len(self.calculators))
        else:
            self._logger.info('wiping results file with selection: '
                              f'{format_iterable(selection)}')

        for irun in selection:
            if verbose:
                print('removing local file', end='... ')

            calc = self.calculators[irun]['calc']

            if hasattr(calc, 'local_directory'):
                file = os.path.join(calc.local_directory, calc.resultfile)
            else:
                self._logger.info('local_directory not found in runner, have '
                                  'it been run yet?')
                if verbose:
                    print('runner has not run yet')
                continue

            self._logger.info(f'removing file {file}')
            print(file, end=' ')

            try:
                os.remove(file)
                if verbose:
                    print('success!')
            except FileNotFoundError:
                if verbose:
                    print('file not found!')


def submit_remote_script(dataset):
    _logger = logging.getLogger(__name__ + '.submit_remote_script')
    if len(dataset.selection) == 0:
        return dataset.results
    commands = '\n'.join([dataset.results[r] for r in dataset.selection])
    _logger.info(f'remote script commands are: \n{commands}')
    filename = dataset.get_global_option('label') + '-script'
    run_dir = dataset.get_global_option('run_dir')
    allcmds = RemoteScript(
        'bash',
        name=filename,
        script=commands, result_file=filename, output_files=[])
    files_to_send = allcmds.setup(dest='.', src=run_dir)
    dataset.url.rsync(files_to_send, run_dir, '.')
    callcmd = allcmds.call()
    _logger.info(f'submitting remote script with cmd: {callcmd}')
    dataset.url.cmd(callcmd, asynchronous=True)
    # nullify the results for the part which has not been submitted
    for r in dataset.selection:
        dataset.results[r] = None
    return dataset.results


class RunsDatabase():
    """Contains the list of runs which have been submitted.

    Args:
        database_file (str): name of the file used to store the data
    """
    def __init__(self, database_file):
        self._logger = logging.getLogger(__name__ + '.RunsDatabase')
        self.filename = self._ensure_name(database_file)
        self.database = self._construct_database(self.filename)

    def _ensure_name(self, name):
        """forces the database file to be a .yaml file"""
        # not a yaml file
        if not name.endswith('.yaml'):
            self._logger.debug(f'{name} does not end with .yaml: Translating')
            if '.' in name:
                self._logger.debug('replacing old extension')
                yamlfile = '.'.join(name.split('.')[:-1]) + '.yaml'
            else:
                yamlfile = name + '.yaml'
        else:
            yamlfile = name
        self._logger.info(f'ensuring name of database file {name}: '
                          f'{yamlfile}')

        return yamlfile

    def _construct_database(self, name):
        self._logger.info(f'constructing database at {name}')
        from yaml import load, Loader
        try:
            with open(name, "r") as ifile:
                return load(ifile, Loader=Loader)
        except FileNotFoundError:
            return []

    def _write_database(self):
        from yaml import dump
        # Update the file
        with open(self.filename, "w") as ofile:
            dump(self.database, ofile)

    def exists(self, name):
        """Checks if a name exists in the database."""
        self._logger.info(f'checking if {name} exists in database')
        return name in self.database

    def register(self, name):
        """Include a name in the database."""
        self._logger.info(f'adding {name} to database')
        if not self.exists(name):
            self._logger.debug('name does not exist, appending')
            self.database.append(name)
            self._write_database()
        else:
            self._logger.debug('name exists already, skipping')

    def clean(self):
        """Remove the database information."""
        self._logger.debug('wiping database...')
        for name in list(self.database):
            self._logger.debug(f'\tremoving {name}')
            self._remove_database_entry(name)

    def _remove_database_entry(self, name):
        if name in self.database:
            self.database.remove(name)
        self._write_database()


def computer_runner(func,
                    submission_script,
                    url=None,
                    validate: bool = True,
                    **kwargs):
    """Create a runner based on a computer information.

    A function is transformed into a remote runner from the specification
    of a computer.

    Args:
        func (func):
            function to be transformed
        submission_script (BigDFT.RemoteRunnerUtils.CallableAttrDict):
            specification dictionary of the computer. Should contain the
            attribute ``submitter``.
        url (BigDFT.URL.URL):
            The url of the computer
        validate (bool, optional):
            Validate input parameters if True
        **kwargs: arguments of the RemoteRunner

    Returns:
        RemoteRunner: a new remote runner ready for the computer.
    """
    _logger = logging.getLogger(__name__ + '.computer_runner')
    if hasattr(submission_script, 'valid') and validate:
        if not submission_script.valid:
            missing = submission_script.missing
            errmsg = 'submission_script is missing required ' \
                     f'arguments: {format_iterable(missing)}'
            _logger.warning(errmsg)
            raise ValueError(errmsg)
    else:
        _logger.warning('submission_script is missing a validation method!')
    if url is None:
        from BigDFT.URL import URL
        url = URL()

    return RemoteRunner(func, submitter=submission_script.submitter, url=url,
                        script=submission_script(), **kwargs)


def computer_script(commands, url, **kwargs):
    """Design a script to be executed remotely.

    This function provides a `RemoteScript` instance which can be used
    to run remotely a particular script on the machine.

    Args:
        commands (BigDFT.RemoteRunnerUtils.CallableAttrDict):
            specification dictionary of the script.
            Must contain the 'prefix' attribute.
        **kwargs: arguments of the `RemoteRunner`
            function. Default choices are made for the positional arguments
            unless otherwise specified.

    Returns:
        BigDFT.RemoteRunnerUtils.RemoteScript: the instance of the
           Remote Script.
    """
    from futile.Utils import kw_pop
    new_kw, submitter = kw_pop('submitter', 'bash', **kwargs)
    new_kw, name = kw_pop('name', 'computer_script', **new_kw)
    # new_kw, result_file = kw_pop('result_file', name, **new_kw)
    # new_kw, output_files = kw_pop('output_files ', [], **new_kw)

    return RemoteRunner(function=_function_for_script,
                        arguments={'prefix': commands.prefix},
                        submitter=submitter, name=name, url=url,
                        script=commands(**new_kw), **new_kw)


def _function_for_script(prefix):
    from os.path import isfile, join
    from os import system
    installdir = join(prefix, '..')
    stderr = join(installdir, 'stderr')
    stdout = join(installdir, 'stdout')
    # better to employ system call as the prefix may be defined with envvars
    system('mv -f '+stderr+' stderr')
    system('mv -f '+stdout+' stdout')
    return isfile('stdout')
