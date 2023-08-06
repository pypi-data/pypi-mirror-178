#!/usr/bin/env python3
'''
    Run code tests.

    To do:
        Prospector
        Test coverage

    Copyright 2019-2022 DeNova
    Last modified: 2022-11-19
'''

import os
import os.path
import re
import sys
from time import sleep
from glob import glob


from denova.os.command import run, run_verbose, background
from denova.os.fs import cd
from denova.os.process import wait_any_child
from denova.python.elapsed_time import ElapsedTime
from denova.python.log import default_log_dir, Log
from denova.python.times import now, timedelta_to_human_readable
from denova.python.internals import dynamically_import_module

class RunTests():

    '''
        There are many steps to set up and run a full test. This module
        reduces errors by automating them. It also tries to run tests
        in parallel when possible.

        Deletes all user logs. Optionally runs static tests, unit tests,
        doctests, and functional tests. The doctests and functional tests
        are run as special cases of unit tests.

        Args:
            'test_group': name of top level module for tests
            'test': name of module, class, or function to test
            'project_dir': full path of the top level module
            'instances': number of test copies to run at the same time

        Returns:
            Nothing.
            Output to the screen reports where the full results can be seen.
    '''

    OUTPUT_DIR = default_log_dir()
    VERBOSITY = 2 # 1 is normal


    def __init__(self, test_group, test, project_dir, instances=None):

        self.test_group = test_group
        self.project_dir = project_dir
        self.instances = instances

        if test is None:
            self.test = self.test_group
        elif test.startswith(f'{self.test_group}.'):
            self.test = test
        else:
            self.test = f'{self.test_group}.{test}'

        self.stdout_path = os.path.join(self.OUTPUT_DIR, f'{self.test_group}.tests.stdout')
        self.stderr_path = os.path.join(self.OUTPUT_DIR, f'{self.test_group}.tests.stderr')
        self.log = Log()

    def start(self):
        '''
            Start the tests.

            >>> CURRENT_DIR = os.path.abspath(os.path.dirname(__file__))
            >>> PROJECT_PATH = os.path.join(CURRENT_DIR, '..', '..', 'denova.com', 'src')
            >>> TEST = 'denova.python.tests.test_doctests'
            >>> run_tests = RunTests('denova', TEST, PROJECT_PATH)
            >>> run_tests.start()
            start...Ran...
        '''

        try:
            self.delete_user_logs()

            # sys.exit(f'test: {test}') # DEBUG
            programs = {}

            with ElapsedTime() as et:
                if self.instances:
                    self.verbose(f'start {self.instances} test instances')

                    for i in range(self.instances):
                        program = self.run_test()
                        self.verbose(f'started instance {program.pid} of {self.test}')
                        programs[program.pid] = (program, now())

                    self.verbose(f'started {self.instances} instances of {self.test}')

                else:
                    if self.test_group == self.test:
                        running_tests = 'all tests'
                    else:
                        running_tests = self.test
                    self.verbose(f'start {running_tests}')
                    program = self.run_test()
                    programs[program.pid] = (program, now())

                self.wait_for_instances(programs)
                self.verbose(f'total time for all tests: {et}')

        except:
            self.log.exception()
            raise

        finally:

            self.show_output()
            self.more_logs()

            """
            # run('killmatch', self.test)
            if os.path.exists(self.stderr_path):
                run('more', self.stderr_path, stdout=sys.stdout, stderr=sys.stderr)
            """

    def run_test(self):

        try:
            program = self.dynamic_tests()
            # ... = self.dynamic_tests() and self.static_tests()

        except:
            self.log.exception()
            raise

        return program

    def static_tests(self):
        run_verbose(f'prospector {self.project_dir}')

    def dynamic_tests(self):

        program = None
        stdout = stderr = stdout_process = None

        if self.test is None or self.test == self.test_group:
            test = self.test_group
        elif not self.test.startswith(self.test_group):
            test = f'{self.test_group}.{self.test}'

        try:
            # log output to a file
            # if we don't, an output flood can overrun the console buffer
            if not os.path.exists(self.OUTPUT_DIR):
                os.makedirs(self.OUTPUT_DIR)
            stdout = open(self.stdout_path, 'a')
            stderr = open(self.stderr_path, 'a')

            """ huh?
            if not self.instances:
                # watch test updates as they happen
                stdout_process = background('tail', '--follow', self.stdout_path, stdout=sys.stdout)
                stderr_process = background('tail', '--follow', self.stderr_path, stdout=sys.stdout)
            """

            os.chdir(self.project_dir)

            # doctests
            # get path
            if os.path.exists(self.test):
                path = self.test
            else:
                module = dynamically_import_module(self.test)
                path = module.__file__
            doctest_command = ['python', '-m', 'doctest', '-v', path]

            # unittests
            unittest_command = ['python', '-m', 'unittest', '-v', self.test]

            for test_command in [doctest_command, unittest_command]:
                # sys.exit(f'test_command: {test_command}') # DEBUG
                program = background(*test_command,
                                     stdout=stdout, stderr=stderr)
                self.log(f'pid={program.pid} start test')

            # As of 2012-11 django's "manage.py test ..." is very unreliable.
            # In earlier years it would lockuprequiring Ctrl-C.
            # Now it just doesn't run some tests. Reporting is near useless.
            # So we don't use it.

        except KeyboardInterrupt:
            # "manage.py test" often locks up after running
            pass

        except Exception as exc:
            raise # DEBUG
            try:
                why = str(exc)
                sys.exit(exc) # DEBUG
                # manage.py always returns non-zero status if test failed
                # in that case error is already in stderr
                if 'returned non-zero exit status' not in why:
                    stderr.write(why)
            except:
                raise exc

        finally:
            if stdout:
                stdout.close()
            if stderr:
                stderr.close()
            if stdout_process:
                stdout_process.kill()
                stderr_process.kill()

        assert program # DEBUG
        return program


    def wait_for_children(self):
        ''' Wait for all children processes to finish.

            >>> CURRENT_DIR = os.path.abspath(os.path.dirname(__file__))
            >>> PROJECT_PATH = os.path.join(CURRENT_DIR, '..', '..', 'denova.com', 'src')
            >>> TEST = None
            >>> for secs in range(3):
            ...     process = background('sleep', secs)
            >>> run_tests = RunTests('denova', TEST, PROJECT_PATH)
            >>> run_tests.wait_for_children()
        '''

    def wait_for_instances(self, programs):
        ''' Wait for test instances. '''

        self.log('wait for test instances to finish')
        child = wait_any_child()
        while child:

            pid, signal, exit_code = child
            if pid in programs:
                __, start = programs[pid]
                elapsed_time = now() - start
                if signal:
                    self.log.error(f'instance {pid} killed by signal {signal}')
                elif exit_code:
                    self.log.error(f'instance {pid} exited with error code {exit_code}')
                self.log(f'instance {pid} exited, time={elapsed_time}')

            else:
                self.log(f'unexpected child {pid}')

            sleep(0.1)
            child = wait_any_child()

        self.log('instances done')

    def delete_user_logs(self):
        ''' Delete all logs for user '''

        if os.path.exists(default_log_dir()):
            run_verbose('rm', '--force', '--recursive', os.path.join(default_log_dir(), '*'))

    def show_output(self):
        ''' Avoid very long results overflowing bash outout buffer.
            Send stderr and stdout to tmp file and to screen.
        '''

        def output_text(path):

            if os.path.exists(path):
                with open(path) as outfile:
                    text = outfile.read()
                if type(text) != str:
                    text = text.decode(errors='replace')

                # remove noise
                # it would be nice to remove noise while the command is running,
                # but that doesn't work well, at least in python 2
                # you have to test for noise in stderr and stdout as separate regexes
                for noise in [r'Destroying test database.*\n',
                              r"\['./manage.py', 'test', .*Synchronize unmigrated.*?\n",
                              r'Apply all migrations.*Applying.*?\n']:
                    text = re.sub(noise, '', text, flags=re.DOTALL)
                with open(path, 'a') as outfile:
                    outfile.write(text)

                # print text line by line to avoid overflowing bash outout buffer
                for line in text.split('\n'):
                    print(line)

        output_text(self.stderr_path)
        output_text(self.stdout_path)

    def more_logs(self):

        def strip_log_dir(path):
            if path.startswith(log_dir):
                path = path[len(log_dir):]
            return path

        log_dir = default_log_dir() + '/'

        self.verbose('Details')
        self.verbose(f'    Log dir: {default_log_dir()}')
        self.verbose(f'    Full stdout: {strip_log_dir(self.stdout_path)}')
        self.verbose(f'    Full stderr: {strip_log_dir(self.stderr_path)}')

    def verbose(self, msg):
        print(msg)
        self.log(msg)


def arg_parser():
    parser = argparse.ArgumentParser(description='Test denova website.')

    parser.add_argument('--instances', nargs='?', type=int, const=3,
                        help='number of test copies to run at the same time')
    parser.add_argument('--static',  action='store_true',
                        help="run static tests")
    parser.add_argument('--doctest',  action='store_true',
                        help="run run_test.py's own doctests")
    parser.add_argument('test', nargs='?',
                        help='package, module, or file to test')

    return parser

def parse_args():
    ''' Parse command line. '''

    args = arg_parser().parse_args()

    return args

if __name__ == "__main__":
    args = parse_args()

    if args.doctests:
        import doctest
        doctest.testmod(optionflags=doctest.ELLIPSIS)

    else:
        main(args)

    sys.exit(0)
