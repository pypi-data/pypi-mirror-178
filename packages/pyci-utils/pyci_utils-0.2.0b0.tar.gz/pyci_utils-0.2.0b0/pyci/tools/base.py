"""
Create a base tool class that can be inherited
from the corresponding tools to be created.
"""
from typing import Tuple, List, Union, Callable, TypeAlias
import attr
# Local imports
from pyci.utils import retrieve_current_dir
from pyci.reporters import PyCILogger


@attr.s(slots=True)
class BaseTool:
    """Base class to be used as parent class for the
    CI tools."""
    _files = attr.ib(default=None, type=Union[str, Tuple[str], List[str]])
    _folder = attr.ib(default=None, type=str)
    _reporter = attr.ib(default=None, type=TypeAlias)

    def __check_files(self, run_tool: Callable[[List[str]], None]) -> None:
        """Method to check the files and see if you can find
        some errors on them.

        Args:
        ----------------------------------------------------------
            - run_tool: Callable[[List[str]], str]: Method to call and execute the tool.

        Raises:
        ----------------------------------------------------------
            - NotImplementedError: For some not implemented options.
        """
        # Check if you have add files (or folders) to check.
        if self._files:
            raise NotImplementedError(
                "The option to review independent files it's not available at the time.")
        if self._folder:
            raise NotImplementedError(
                "The option to review an entire folder it's not available at the time.")
        # If you don't add nothing, then check whatever you can find on the repository
        _args = retrieve_current_dir()
        # Run the corresponding tool method
        run_tool(_args)

    def report(self, run_tool: Callable[[List[str]], None], ci_tool: str) -> None:
        """Run method that executes the static python visualization
        to find typing errors.

        Args:
        ----------------------------------------------------------
            - run_tool: Callable[[List[str]], str]: Method to call and execute the tool.
            - ci_tool: The name of the tool to be executed
        """
        logger = PyCILogger()  # Initialize the logger
        self.__check_files(run_tool)
        errors = self._reporter.errors
        # If you don't have any errors...
        if not errors:
            logger.no_errors(
                "[bold green]You don't have any errors![/bold green] Nice job!", ci_tool=ci_tool)
            return
        # If you've errors
        logger.log(errors, ci_tool=ci_tool)
        return
