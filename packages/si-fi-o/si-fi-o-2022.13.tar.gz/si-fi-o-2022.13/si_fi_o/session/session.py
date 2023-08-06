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

from configparser import ConfigParser as ini_config_t
from pathlib import Path as path_t
from typing import Any, Callable, Sequence

from flask_wtf import FlaskForm as flask_form_t

from si_fi_o.path.server import file_t


class session_t(dict):
    """
    To be stored in a Flask session
    """

    form_file_fields: tuple[str, ...] = None
    outputs: Any = None
    outputs_path: path_t | None = None

    def UpdateInputs(
        self, inputs: dict[str, Any], file_fields: Sequence[str], /
    ) -> None:
        """"""
        if not set(file_fields).issubset(inputs.keys()):
            raise ValueError(
                f"{file_fields}: Form file fields not a subset of form fields {tuple(inputs.keys())}"
            )

        for field, value in inputs.items():
            # Only file field values can be None (see si_fi_o.session.form.form_t.Data). In order to preserve session
            # values, None inputs are disregarded. This means that when deleting input files in DeleteInputFiles,
            # self[field] might not exist.
            if value is not None:
                if isinstance(value, file_t):
                    _DeleteInputFile(self, field)
                self[field] = value

        self.form_file_fields = tuple(file_fields)

    def InputFilesContents(
        self, LoadInput: Callable[[path_t], Any], /
    ) -> dict[str, Any]:
        """
        Example:
            inputs = session.InputFilesContents(skimage.io.imread)
        """
        return {_inp: LoadInput(self[_inp][1]) for _inp in self.form_file_fields}

    def DeleteInputFiles(self) -> None:
        """"""
        if self.form_file_fields is not None:
            for field in self.form_file_fields:
                _DeleteInputFile(self, field)

    def UpdateOutputs(self, outputs: Any, outputs_path: path_t | None, /) -> None:
        """"""
        _DeleteFile(self.outputs_path)
        self.outputs = outputs
        self.outputs_path = outputs_path

    def DeleteOutputsFile(self) -> None:
        """"""
        self.UpdateOutputs(None, None)

    def AsDictionary(self) -> dict[str, Any]:
        """"""
        return dict(self)

    def AsINI(self, section: str, /) -> ini_config_t:
        """
        Does include form file fields but filenames only since paths of input files cannot be stored in a session as
        they are only known by the client.
        """
        output = ini_config_t()

        output[section] = {
            _fld: _val.name if isinstance(_val, file_t) else _val
            for _fld, _val in self.items()
        }

        return output

    @property
    def is_empty(self) -> bool:
        """"""
        return self.__len__() == 0

    def IsComplete(self, *, form: flask_form_t = None) -> bool:
        """
        form: Useful when the form has several submission buttons, and thus different completeness definitions
        """
        # Do not use self[_key] below since reference and/or detection files are missing if the form has been submitted
        # without these files (they are not required fields since the session can supply them) and the session has not
        # received these files yet, e.g. on the first run if not selecting these files.
        return (
            (not self.is_empty)
            and all(_val is not None for _val in self.values())
            and (self.form_file_fields is not None)
            and all(
                isinstance(self.get(_key), file_t) for _key in self.form_file_fields
            )
        )


def _DeleteFile(path: path_t | None, /) -> None:
    """"""
    if (path is not None) and path.is_file():
        path.unlink()


def _DeleteInputFile(session: session_t, field: str, /) -> None:
    """"""
    if (file := session.get(field)) is not None:
        _DeleteFile(file.path)
