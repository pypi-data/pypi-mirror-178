# Copyright CNRS/Inria/UCA
# Contributor(s): Eric Debreuve (since 2022)
#
# eric.debreuve@cnrs.fr
#
# This software is governed by the CeCILL  license under French law and
# abiding by the rules of distribution of free software.  You can  use,
# modify and/ or redistribute the software under the terms of the CeCILL
# license as circulated by CEA, CNRS and INRIA at the following URL
# "http://www.cecill.info".
#
# As a counterpart to the access to the source code and  rights to copy,
# modify and redistribute granted by the license, users are provided only
# with a limited warranty  and the software's author,  the holder of the
# economic rights,  and the successive licensors  have only  limited
# liability.
#
# In this respect, the user's attention is drawn to the risks associated
# with loading,  using,  modifying and/or developing or reproducing the
# software by the user in light of its specific status of free software,
# that may mean  that it is complicated to manipulate,  and  that  also
# therefore means  that it is reserved for developers  and  experienced
# professionals having in-depth computer knowledge. Users are therefore
# encouraged to load and test the software's suitability as regards their
# requirements in conditions enabling the security of their systems and/or
# data to be ensured and,  more generally, to use and operate it in the
# same conditions as regards security.
#
# The fact that you are presently reading this means that you have had
# knowledge of the CeCILL license and that you accept its terms.

import dataclasses as dtcl
import secrets as scrt
from configparser import ConfigParser as ini_config_t
from pathlib import Path as path_t
from typing import Any, Callable

import flask as flsk

from si_fi_o.html.home_page import HomePage
from si_fi_o.path.server import (
    NAME_FIELD_SEPARATOR,
    OutdatedServerFilesIterator,
    ServerFilesIterator,
    ServerVersionOfFilename,
    TIME_STAMP_SEPARATOR,
)
from si_fi_o.session.session import session_t


_SESSION_FILENAME = "session.ini"


@dtcl.dataclass(repr=False, eq=False)
class routes_t:

    home_page_details: dict[str, Any]
    form_type: type
    session_type: type
    ProcessSession: Callable[
        [session_t, str, path_t], tuple[tuple[Any, ...], path_t | None]
    ]
    ini_section: str
    session_folder: path_t = dtcl.field(init=False, default=None)  # Flask sessions
    input_folder: path_t = dtcl.field(init=False, default=None)  # Used as upload folder
    output_folder: path_t = dtcl.field(init=False, default=None)  # Also for si-fi-o sessions

    def Configure(self, app: flsk.app, /) -> None:
        """"""
        # app.static_folder is an absolute path
        relative_static_folder = path_t(path_t(app.static_folder).name)
        runtime_folder = relative_static_folder / "runtime"
        self.session_folder = runtime_folder / "session"
        self.input_folder = runtime_folder / "input"
        self.output_folder = runtime_folder / "output"
        for folder in (self.session_folder, self.input_folder, self.output_folder):
            folder.mkdir(parents=True, exist_ok=True)

        _ = app.route("/")(self.LaunchNewSession)
        _ = app.route("/<session_id>", methods=("GET", "POST"))(self.UpdateHomePage)
        _ = app.route("/load/<session_id>", methods=("POST",))(self.LoadSession)
        _ = app.route("/save/<session_id>")(self.SaveSession)
        _ = app.route("/delete/<session_id>")(self.DeleteSession)

    def LaunchNewSession(self) -> flsk.Response:
        """"""
        session_id = scrt.token_urlsafe().replace(
            NAME_FIELD_SEPARATOR, TIME_STAMP_SEPARATOR
        )
        flsk.session[session_id] = self.session_type()

        return flsk.redirect(f"/{session_id}")

    def UpdateHomePage(self, *, session_id: str = None) -> str:
        """"""
        session = flsk.session[session_id]
        form = self.form_type()  # Do not pass flask.request.form

        # Does not iterate files in self.session_folder since it contains Flask sessions with Flask-specific names
        for folder in (self.input_folder, self.output_folder):
            for path in OutdatedServerFilesIterator(folder):
                print("OUTDATED:", path)

        if flsk.request.method == "GET":
            form.Update(session.AsDictionary())
        elif form.validate_on_submit():
            form_data = form.Data(session_id, self.input_folder)
            session.UpdateInputs(form_data, form.file_fields)

            if session.IsComplete(form=form):
                outputs = self.ProcessSession(session, session_id, self.output_folder)
                session.UpdateOutputs(*outputs)

        return HomePage(
            session_id, session=session, form=form, **self.home_page_details
        )

    def LoadSession(self, *, session_id: str = None) -> flsk.Response:
        """"""
        session = flsk.session[session_id]

        session_file = tuple(flsk.request.files.values())[0]
        new_as_str = session_file.read().decode("ascii")
        new_as_ini = ini_config_t()
        new_as_ini.read_string(new_as_str)

        # Form file fields are not file_t's then, so the loaded session cannot be used as is
        for field, value in new_as_ini.items(self.ini_section):
            session[field] = value

        return flsk.redirect(f"/{session_id}")

    def SaveSession(self, *, session_id: str = None) -> flsk.Response:
        """"""
        session = flsk.session[session_id]

        name = ServerVersionOfFilename(_SESSION_FILENAME, session_id)
        path = self.output_folder / name
        with open(path, "w") as accessor:
            session.AsINI(self.ini_section).write(accessor)

        return flsk.send_file(
            path,
            mimetype="text/plain",
            as_attachment=True,
            download_name=name,
        )

    def DeleteSession(self, *, session_id: str = None) -> flsk.Response:
        """"""
        session = flsk.session[session_id]

        session.DeleteInputFiles()
        session.DeleteOutputsFile()
        # Delete downloadable session file created by SaveSession
        for path in ServerFilesIterator(
            self.output_folder, session_id, name=_SESSION_FILENAME
        ):
            if path.is_file():
                path.unlink()

        flsk.session.pop(session_id, None)

        return flsk.redirect("/")
