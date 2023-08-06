"""
Code made to fix the links in all the .html files
to add the relative paths to each one of them.
"""
from typing import List, Dict, Optional
import pathlib
from pathlib import PosixPath
import attr
from server.logger import Logger

logger = Logger()


@attr.s(slots=True)
class FixPaths:
    """Class to read and fix the files with links
    changing an specific 'string' to a relative path."""
    # Path related attributes
    _directory_path = attr.ib(default=None, type=str)
    _paths = attr.ib(default=[], type=List[str])
    # To fix the documents once the deploy has finished
    _documents_changed = attr.ib(default=None, type=Dict[str, Dict])

    # Document related attributes
    _remote_link = attr.ib(default=None, type=str)
    _local_link = attr.ib(default=None, type=str)

    def __attrs_post_init__(self):
        def __search_in_path(item: PosixPath, extra_paths_to_check: Optional[List[PosixPath]] = None) -> None:
            """Short function to search the .html and .js files
            in a given posixPath object."""
            # Check if the item ends with .html. and .js
            if str(item).endswith((".html", ".js")):
                # if it ends with it, add it to the list
                self._paths += [str(item)]
            # If the item is a directory, then check inside the directory with a loop
            elif item.is_dir():
                # Do the same but this time with a sub item
                if extra_paths_to_check:
                    extra_paths_to_check += list(
                        new_item for new_item in item.iterdir())
                else:
                    extra_paths_to_check = list(
                        new_item for new_item in item.iterdir())
            # Return the extra_paths_to_check first
            if extra_paths_to_check:
                item_to_check = extra_paths_to_check[-1]
                # Remove the item from the list
                extra_paths_to_check.remove(item_to_check)
                __search_in_path(item_to_check, extra_paths_to_check)

        # Define the directory_path
        self._directory_path = pathlib.Path(
            __file__).resolve().parent.parent.parent
        # Now, obtain all the paths from the files from here.
        for item in self._directory_path.iterdir():
            __search_in_path(item)

    def __fix_links(self, document_path: str, base_link: str) -> Dict[int, str]:
        """Method to open the document and set it as
        the attribute of the class.

        Args:
            document_path (str): Path of the document to read.
            base_link (str): Base link to substitute.
        """
        # First, open and save the file here in Python
        with open(document_path, 'r') as doc:
            document = doc.readlines()
        doc.close()
        # Open the file that you've provided.
        # Empty dict with the index of the replaced_lines
        replaced_lines: Dict[int, str] = {}
        with open(document_path, "w") as fixed_doc:
            for line_index, line in enumerate(document):
                if "{/url_path/}" in line:
                    replaced_lines[line_index] = line  # Save the original line
                    line = line.replace("{/url_path/}", base_link)
                fixed_doc.write(line)
        fixed_doc.close()
        return replaced_lines

    def deploy_server(self, base_url: str) -> None:
        """Method to deploy the server using the __fix_links method that was seen here

        Args:
            base_url (str): URL to substitute on the links of the file paths
        """
        documents_changed: Dict[str, Dict] = {
        }  # Empty dictionary to store changes later
        # Now, use the same as the set_url but with an empty url
        for path in self._paths:
            replaced_lines = self.__fix_links(path, base_url)
            # Only if you have found replaced_lines, store that document for later.
            if replaced_lines:
                documents_changed[path] = replaced_lines
        # Now, save this changes
        self._documents_changed = documents_changed

    def repair_documents(self):
        """Method to repair those documents that had been changed"""
        if self._documents_changed:
            for doc_path, lines_to_change in self._documents_changed.items():
                # First, open and save the file here in Python
                with open(doc_path, 'r') as doc:
                    document = doc.readlines()
                doc.close()
                # Open the file that you've provided.
                with open(doc_path, "w") as original_doc:
                    for line_index, line in enumerate(document):
                        if line_index in lines_to_change:
                            line = lines_to_change[line_index]
                        original_doc.write(line)
                original_doc.close()
            logger.log('Documents returned to its original state.',
                       status='INFO')
        else:
            logger.log("There's no documents to change.", status='INFO')
