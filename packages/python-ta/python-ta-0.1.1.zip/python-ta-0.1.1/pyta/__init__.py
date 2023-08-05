"""Python Teaching Assistant

The goal of this module is to provide automated feedback to students in our
introductory Python courses, using static analysis of their code.

To run the checker, call the check function on the name of the module to check.

> import pyta
> pyta.check_all('mymodule')
"""
import importlib.util
import os
import sys
import webbrowser

import pylint.lint as lint
from astroid import MANAGER

from pyta.reporters import ColorReporter

# Local version of website; will be updated later.
HELP_URL = 'http://www.cs.toronto.edu/~david/pyta/'


# check the python version
if sys.version_info < (3, 4, 0):
    print('You need Python 3.4 or later to run this script')


def check_errors(module_name, reporter=ColorReporter, number_of_messages=5):
    """Check a module for errors, printing a report.

    The name of the module should be the name of a module,
    or the path to a Python file.
    """
    _check(module_name, reporter, number_of_messages, level='error')


def check_all(module_name, reporter=ColorReporter, number_of_messages=5):
    """Check a module for errors and style warnings, printing a report.

    The name of the module should be passed in as a string,
    without a file extension (.py).
    """
    _check(module_name, reporter, number_of_messages, level='all')


def _check(module_name, reporter=ColorReporter, number_of_messages=5, level='all',
           local_config_file=False):
    """Check a module for problems, printing a report.

    <level> is used to specify which checks should be made.

    The name of the module should be the name of a module,
    or the path to a Python file.
    """
    # Check if `module_name` is not the type str, raise error.
    if not isinstance(module_name, str):
        print("The Module '{}' has an invalid name. Module name must be the "
              "type str.".format(module_name))
        return

    module_name = module_name.replace(os.path.sep, '.')

    # Detect if the extension .py is added, and if it is, remove it.
    if module_name.endswith('.py'):
        module_name = module_name[:-3]

    # Reset astroid cache
    MANAGER.astroid_cache.clear()

    spec = importlib.util.find_spec(module_name)
    if spec is None:
        print("The Module '{}' could not be found. ".format(module_name))
        return

    current_reporter = reporter(number_of_messages)
    linter = lint.PyLinter(reporter=current_reporter)
    linter.load_default_plugins()
    linter.load_plugin_modules(['pyta/checkers/forbidden_import_checker',
                                'pyta/checkers/global_variables_checker',
                                'pyta/checkers/dynamic_execution_checker',
                                'pyta/checkers/IO_Function_checker',
                                # TODO: Fix this test
                                #'pyta/checkers/invalid_range_index_checker',
                                'pyta/checkers/assigning_to_self_checker',
                                'pyta/checkers/always_returning_checker'])
    if local_config_file:
        linter.read_config_file()
    else:
        linter.read_config_file(os.path.join(os.path.dirname(__file__), '.pylintrc'))
    linter.load_config_file()

    # Make sure the program doesn't crash for students.
    # Could use some improvement for better logging and error reporting.
    try:
        linter.check([spec.origin])
        current_reporter.print_messages(level)
    except Exception as e:
        print('Unexpected error encountered - please report this to david@cs.toronto.edu!')
        print(e)


def doc(msg_id):
    """Open a webpage explaining the error for the given message."""
    msg_url = HELP_URL + '#' + msg_id
    print('Opening {} in a browser.'.format(msg_url))
    webbrowser.open(msg_url)
