"""
Class to set the FastAPI server
"""
# External imports
import attr
# Import all the FastAPI modules
from fastapi import FastAPI, Request, Response
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
# Setup for the FastAPI app
from server.__info__ import name, __version__, description, contact, __license__


@attr.s(slots=True)
class App:
    """FastAPI application to run the webpage."""
    _pages = attr.ib(default=None, type=Jinja2Templates)
    _app = attr.ib(default=None, type=FastAPI)

    def __attrs_post_init__(self) -> None:
        # Fix the links on the page
        self._pages = Jinja2Templates(directory="webpage")
        self._app = FastAPI(
            title=name, description=description,
            version=__version__, contact=contact,
            license_info=__license__
        )
        # Now, mount some pages, as the home page
        self._app.mount(
            "/webpage", StaticFiles(directory="webpage"), name="webpage")
        self._app.get("/")(self.home)
        self._app.get("/errors")(self.errors_index)
        self._app.get("/errors/{error_type}/{error}")(self.errors)

    @property
    def client(self) -> FastAPI:
        """Method that only returns the FastAPI object

        Returns:
            FastAPI: FastAPI object
        """
        return self._app

    # ---------------------------------------------------------------- #
    #                        THE ASYNC METHODS                         #
    # ---------------------------------------------------------------- #

    async def home(self, request: Request) -> Response:
        """Method to return the home directory using a html file
        from the webpage folder."""
        # Add this home.html as the main response object
        response = self._pages.TemplateResponse(
            "home.html", {"request": request})
        return response

    async def errors_index(self, request: Request) -> Response:
        """Method to return as a response the errors index html file."""
        return self._pages.TemplateResponse("errors/index.html", {"request": request})

    async def errors(self, request: Request, error_type: str, error: str) -> Response:
        """Method to return as a response the errors"""
        return self._pages.TemplateResponse(f"errors/{error_type}/{error}", {"request": request})
