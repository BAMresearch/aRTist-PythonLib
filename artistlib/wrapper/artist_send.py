from pathlib import Path
import numbers
import logging
from ..junction import Junction

logger = logging.getLogger(__name__)


class ArtistSend:
    """This class validates user input and sends the resulting Tcl commands to aRTist."""

    _jct = None  # gemeinsame Instanz
    _global_batch = False
    _batch_list = []

    def __init__(
        self,
        batch: bool = None,
        host="localhost",
        port=3658,
        bufferSize=1024,
        timeout=5,
    ):
        if ArtistSend._jct is None:
            ArtistSend._jct = Junction(host, port, bufferSize, timeout)
        self.jct = ArtistSend._jct

        self.batch_flag = batch if batch is not None else self.__class__._global_batch

    @classmethod
    def set_global_batch(cls, value: bool):
        """Enables batching mode when set to `True`. Function calls are stored and sent together.
        **Note:** Batching can improve performance, but some functions may behave differently. Use the `apply()` function to send the accumulated commands."""
        cls._global_batch = value

    def apply(self) -> str:
        """Sends the batched command list to aRTist in chunks."""
        a = ""
        chunk_size = 300
        list_chunk = [
            ArtistSend._batch_list[i : i + chunk_size]
            for i in range(0, len(ArtistSend._batch_list), chunk_size)
        ]
        for elements in list_chunk:
            cmd = "".join(elements)
            a += self.jct.send(cmd)
        ArtistSend._batch_list.clear()
        return a

    def send(self, cmd: str) -> str:
        """Sends Tcl commands directly to aRTist or stores them in the batch queue if batching is enabled."""
        if self.batch_flag is True:
            cmd_fin = cmd.strip("\n") + " ; "
            ArtistSend._batch_list.append(cmd_fin)
            return cmd_fin

        response = self.jct.send(cmd)
        return response

    def _isnumber(self, val) -> bool:
        if isinstance(val, numbers.Number) or val is None:
            return True
        else:
            raise TypeError("Only numbers are allowed", val)

    def _is_str_safe(self, string) -> None:
        if string is None:
            return
        if isinstance(string, str):
            if "[" in string or ";" in string or "\n" in string or "{" in string:
                raise Exception(
                    r"Risk of TCL injection, do not use '[' , ';' , '\n','{' in your string",
                    string,
                )
        else:
            raise Exception("Input is not a string", string)
        return

    def _replace_slashes(self, path: str) -> str:
        path = str(path)
        return path.replace("\\", "/")

    def _is_path_safe(self, path) -> str:
        path = str(path)
        path = path.replace("\\", "/")
        # not the best solution, because TCL path is solved in Artist
        if "$" in path:
            return path
            # if os.path.exists(path) or "$" in path:
        path = Path(path).expanduser()  # ~ auflösen
        path = path.resolve()  # absolut + sauber
        path = path.as_posix()  # "/" statt "\"
        return path

    def _control_str(self, *args) -> None:
        for a in args:
            self._is_str_safe(a)

    def _control_number(self, *args) -> None:
        for a in args:
            self._isnumber(a)

    def _control_path(self, *args) -> str:
        paths = [None] * len(args)
        i = 0
        for a in args:
            paths[i] = self._is_path_safe(a)
            i = i + 1

        return paths

    def _path_exist(self, *args) -> None:
        for a in args:
            if "$" in a:
                continue
            p = Path(a)
            if not p.exists():
                raise Exception("path does not exist", p)

    def load_file(self, path: str) -> str:
        """Loads a file into aRTist from the specified path."""
        path_s = str(path)
        self._control_str(path_s)
        path_s = self._control_path(path_s)[0]
        self._path_exist(path_s)
        a = self.send(f'::FileIO::OpenAny "{path_s}"')
        return a
