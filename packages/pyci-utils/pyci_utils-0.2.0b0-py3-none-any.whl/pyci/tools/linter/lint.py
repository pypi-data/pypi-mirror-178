"""
Script that uses pylint to check codes and print custom
warnings and errors messages here.
"""
import os
from typing import Tuple, List, Dict, Optional, TypeAlias
from collections import defaultdict
import attr
# Pylint imports
from pylint.lint.run import _cpu_count
from pylint.lint.pylinter import PyLinter
from pylint.lint.base_options import _make_run_options
from pylint.config import find_default_config_files
from pylint.config.config_initialization import _config_initialization
from pylint.reporters.base_reporter import BaseReporter
from pylint.message import Message
# Local imports
from pyci.tools import BaseTool
from pyci.utils import find_code


class CustomReporter(BaseReporter):
    """Custom Reporter for Pylint and its errors."""

    def __init__(self) -> None:
        super().__init__()
        self.path_strip_prefix = os.getcwd() + os.sep
        self._errors: Dict[str, List[Dict[str, str]]] = defaultdict(list)

    def _display(self, layout):
        pass

    def handle_message(self, msg: Message) -> None:
        """Personal method to append the errors in a better way"""
        self._errors[msg.path].append({
            'line': msg.line,
            'col': msg.column,
            'msg': f"{msg.msg_id} {msg.msg}",
            'type': msg.msg_id[0],
            'code': find_code(msg.line, msg.end_line, msg.abspath)
        })

    @property
    def errors(self) -> Optional[Dict[str, List[Dict[str, str]]]]:
        """Method to return a better structure of errors"""
        if not self._errors:
            return None
        return self._errors

    def on_set_current_module(self, module: Optional[str] = None, filepath: Optional[str] = None) -> None:
        """Hook called when a module starts to be analyzed."""


@attr.s(slots=True)
class PylintRunner(BaseTool):
    """Class to perform a personal Pylint validation to catch all the errors or
    messages that comes from the codes."""
    # Add the options to run
    _options = attr.ib(default=(("Commands", "Commands",),), type=Tuple[str])
    # Some configuration files, as the .rcFile
    _rcFile = attr.ib(default=None, type=str)
    # The Linter and the base reporter
    _linter = attr.ib(default=None, type=PyLinter)
    _reporter = attr.ib(default=CustomReporter, type=TypeAlias)

    def __attrs_post_init__(self) -> None:
        #!TODO Add also other parameters as the possibility to add custom rc files.
        # Check if the user has passed some _rcFile. If not, then use the default one.
        if not self._rcFile:
            self._rcFile = str(next(find_default_config_files(), None))
        # Initialize the reporter
        self._reporter = self._reporter()
        # Now, initialize the linter
        self._linter = PyLinter(
            _make_run_options(self),
            option_groups=self._options,
            pylintrc=self._rcFile,
        )
        # Add some linter configurations
        self._linter.load_default_plugins()
        self._linter.disable("I")
        self._linter.enable("c-extension-no-member")
        if self._linter.config.jobs < 0:
            raise ValueError(
                f"Jobs number ({self._linter.config.jobs}) should be greater than or equal to 0")
        if self._linter.config.jobs == 0:
            self._linter.config.jobs = _cpu_count()

    def __run_tool(self, files: List[str]) -> None:
        """Private method to include how to run this tool."""
        # Once you've finished the process of selecting the arguments to review
        #!TODO Later, add the possibility here to choose between the customReporter
        #!TODO for the terminal and the custom reporter for the web app.
        _args = _config_initialization(
            self._linter, files, self._reporter, config_file=self._rcFile, verbose_mode=False
        )
        # If you can't find arguments, report that to the user
        if not _args:
            print(
                f"There are no files to review for the given path '{files}'.")
            return
        # Now, check the files with the linter
        self._linter.check(_args)

    def run(self) -> None:
        """Method to run the linter."""
        self.report(self.__run_tool, 'Pylint')


if __name__ == '__main__':
    PR = PylintRunner()
    PR.run()
