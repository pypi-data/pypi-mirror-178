# Significant portion of code in this file was taken from https://github.com/msm1089/ipynbname
# MIT License
#
# Copyright (c) 2020 Mark McPherson
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


import importlib
import json
import urllib.error
import urllib.request
from itertools import chain
from pathlib import Path, PurePath
from typing import Generator, Tuple, Union, Optional, Dict, Any
from traitlets.config import MultipleInstanceError

FILE_ERROR = "Can't identify the notebook {}."
CONN_ERROR = "Unable to access jupyter notebook server;\n" \
             + "notebook config requires either no security or token based security."


def get_main_notebook_path_if_run_in_one() -> Optional[Path]:
    running_in_notebook = is_run_in_jupyter_notebook()
    if running_in_notebook:
        return NotebookPath().path
    else:
        return None


# todo: return enum with environment and have ifs in other places check for specific envs if needed
# https://stackoverflow.com/questions/15411967/how-can-i-check-if-code-is-executed-in-the-ipython-notebook
def is_run_in_jupyter_notebook() -> bool:
    # get_ipython().__class__.__module__ == "google.colab._shell"
    # should be true for google collab
    try:
        shell = get_ipython().__class__.__name__  # type: ignore
        if shell == 'ZMQInteractiveShell':
            return True   # Jupyter notebook or qtconsole
        elif shell == 'TerminalInteractiveShell':
            return False  # Terminal running IPython
        else:
            return False  # Other type (?)
    except NameError:
        return False      # Probably standard Python interpreter


class NotebookPath:
    def __init__(self) -> None:
        self.ipykernel_module = importlib.import_module("ipykernel")
        self.jupyter_core_module = importlib.import_module("jupyter_core")
        self.path = self.find_path()

    def find_path(self) -> Path:
        """ Returns the absolute path of the notebook,
            or raises a FileNotFoundError exception if it cannot be determined.
        """
        srv, path = self._find_nb_path()
        if srv and path:
            root_dir = Path(srv.get('root_dir') or srv['notebook_dir'])
            return root_dir / path
        raise FileNotFoundError(FILE_ERROR.format('path'))

    def _list_maybe_running_servers(self, runtime_dir: Optional[Path] = None) -> Generator[Dict[str, Any], None, None]:
        """ Iterate over the server info files of running notebook servers.
        """
        if runtime_dir is None:
            runtime_dir = self.jupyter_core_module.paths.jupyter_runtime_dir()
        runtime_dir = Path(runtime_dir)

        if runtime_dir.is_dir():
            for file_name in chain(
                    runtime_dir.glob('nbserver-*.json'),  # jupyter notebook (or lab 2)
                    runtime_dir.glob('jpserver-*.json'),  # jupyterlab 3
            ):
                yield json.loads(file_name.read_bytes())

    def _get_kernel_id(self) -> str:
        """ Returns the kernel ID of the ipykernel.
        """
        connection_file = Path(self.ipykernel_module.get_connection_file()).stem
        kernel_id = connection_file.split('-', 1)[1]
        return kernel_id

    def _find_nb_path(self) -> Union[Tuple[Dict[str, Any], PurePath], Tuple[None, None]]:
        try:
            kernel_id = self._get_kernel_id()
        except (MultipleInstanceError, RuntimeError):
            return None, None  # Could not determine
        for srv in self._list_maybe_running_servers():
            try:
                sessions = _get_sessions(srv)
                for sess in sessions:
                    if sess['kernel']['id'] == kernel_id:
                        return srv, PurePath(sess['notebook']['path'])
            except Exception:  # noqa
                pass  # There may be stale entries in the runtime directory
        return None, None


def _get_sessions(srv: Dict[str, Any]) -> Any:
    """ Given a server, returns sessions, or HTTPError if access is denied.
        NOTE: Works only when either there is no security or there is token
        based security. An HTTPError is raised if unable to connect to a
        server.
    """
    try:
        qry_str = ""
        token = srv['token']
        if token:
            qry_str = f"?token={token}"
        url = f"{srv['url']}api/sessions{qry_str}"
        with urllib.request.urlopen(url) as req:
            return json.load(req)
    except Exception:
        raise RuntimeError("Unable to connect to Jupyter Notebook server.")


# this was in the lib, might come in handy sometime
#
# def name() -> str:
#     """ Returns the short name of the notebook w/o the .ipynb extension,
#         or raises a FileNotFoundError exception if it cannot be determined.
#     """
#     _, path = _find_nb_path()
#     if path:
#         return path.stem
#     raise FileNotFoundError(FILE_ERROR.format('name'))
