"""
Type checker that uses mypy.
"""
from typing import Tuple, List, Dict, Union, Optional, TypeAlias
from collections import defaultdict
from pathlib import Path
import attr
from mypy import api
# Local imports
from pyci.tools import BaseTool
from pyci.utils import find_code


class CustomReporter:
    """Custom reporter to catch and clean the errors
    given by mypy."""
    __slots__ = ['_errors']

    def __init__(self) -> None:
        self._errors: Dict[str, List[Dict[str, str]]] = defaultdict(list)

    def clean_result(self, result: Tuple[str, str, int]) -> None:
        """Method to clean the result of the custom reporter"""
        # First check the errors status output
        if not result[2]:
            return
        # If you've errors, then...
        mypy_errors = [('.py: error:' not in e, e)
                       for e in result[0].split('\n')[:-2] if 'note:' not in e]
        # Iterate over the mypy_errors
        for e_with_line, error in mypy_errors:
            if e_with_line:
                [path_with_line, typing_error] = error.split(': error: ')
                [path, line] = path_with_line.split(':')
            else:
                [path, typing_error] = error.split(': error: ')
                line = '0'  # It's a entire file problem
            # Now, append it to the errors dictionary
            self._errors[path].append({
                'line': line,
                'msg': typing_error,
                # 'type': #!TODO Write here the [error]
                'code': find_code(int(line), None, str(Path(path).absolute()))
            })

    @property
    def errors(self) -> Optional[Dict[str, List[Dict[str, str]]]]:
        """Method to return a better structure of errors"""
        if not self._errors:
            return None
        return self._errors


@attr.s(slots=True)
class TypeChecker(BaseTool):
    """Custom type checker that is able to uses mypy."""
    _files = attr.ib(default=None, type=Union[str, Tuple[str], List[str]])
    _folder = attr.ib(default=None, type=str)
    _reporter = attr.ib(default=CustomReporter, type=TypeAlias)

    def __attrs_post_init__(self) -> None:
        # initialize the reporter
        self._reporter = CustomReporter()

    def __run_tool(self, files: List[str]) -> None:
        """Private method to include how to run this tool."""
        result = api.run(files)
        self._reporter.clean_result(result)

    def run(self) -> None:
        """Run method that executes the static python visualization
        to find typing errors.
        """
        self.report(self.__run_tool, 'mypy')
