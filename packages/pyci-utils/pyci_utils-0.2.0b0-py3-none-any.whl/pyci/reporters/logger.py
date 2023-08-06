"""
Logger for the PyCI Tools.
This logger would be capable of handle the correct use
show of the files, the capacity of save them in an external .txt, .json or .markdown file
and it would be able to highlight some important information.
"""
from typing import Callable, Dict, List, Union
import attr
from rich.console import Console
from rich.markdown import Markdown
from rich.syntax import Syntax


@attr.s(slots=True)
class PyCILogger:
    """Logger for the PyCI Tools."""
    _console = attr.ib(default=Console(), type=Console)
    _log = attr.ib(default=None, type=Dict[str, Callable])

    @staticmethod
    def __path_format(path: str) -> str:
        """Module to be used to give format to the path of the files that
        are receiving some error.
        """
        return f"[bold black on yellow]{32*'-'} Module[/bold black on yellow]:[b][u]{path}\n"

    @staticmethod
    def __error_format(error: Dict[str, str]) -> List[Union[str, Syntax]]:
        """Module to be used to give format to the error of the codes."""
        line = f"[bold cyan]{18*'-'} [u]Line {error['line']}[/u]: {error['msg']}"
        # If you've error line...
        if error['code']:
            code = Syntax(error['code'], "python",
                          background_color='default')
            return [line, code, '']
        # If you don't, return only the line and the messages
        return [line, '']

    def no_errors(self, message: str, ci_tool: str = 'PyCILogger') -> None:
        """Method to print a 'No Error' success message."""
        log_entries = [Markdown(f"# {ci_tool}"), message]
        for entry in log_entries:
            self._console.print(entry)

    @staticmethod
    def link(url: str) -> str:
        """Static method to give format to url."""
        return f"[blue][u]{url}"

    def log(self, errors: Dict[str, List[Dict[str, str]]], ci_tool: str = 'PyCILogger') -> None:
        """Method to perform a logging event based on a report."""
        log_entries: List[Union[Markdown, str, Syntax]] = [
            Markdown(f"# {ci_tool}")]
        # Now, for each error entry, save it on the log entries
        for _file, _errors in errors.items():
            log_entries.append(self.__path_format(_file))
            for error in _errors:
                log_entries += self.__error_format(error)
            # Add an '\n' at the end of the errors
            log_entries.append('')
        # At the end, print each log entry
        for entry in log_entries[:-1]:
            self._console.print(entry)


if __name__ == "__main__":
    log = PyCILogger()
