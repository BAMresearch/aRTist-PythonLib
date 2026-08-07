from .artist_send import ArtistSend
import os
from pathlib import Path


class ArtistProject(ArtistSend):
    """This class manages a project, including loading, running, and saving project images."""

    def load_save_project(
        self, project_path: str, save_img_to: str, img_name: str
    ) -> str:
        """Loads a project from a specified path, runs aRTist, saves the resulting image to the specified location, and returns the aRTist response."""
        self._control_str(img_name)
        project_path, save_img_to = self._control_path(project_path, save_img_to)
        self._path_exist(project_path, save_img_to)

        command_load_project = f'FileIO::OpenAny "{project_path}"'

        save_place_name = self._replace_slashes(os.path.join(save_img_to, img_name))

        self.send(command_load_project)
        self.send("Engine::GoCmd")
        ans = "Saved as: "

        cmd_save = (
            "Modules::Invoke ImageViewer SaveFile [file join $env(HOME) "
            + save_place_name
            + "] true"
        )
        ans += self.send(cmd_save)
        return ans

    def load_project(self, path_to_project: str) -> str:
        """Loads a project into aRTist."""
        # self._control_str(path_to_project)
        path_to_project = self._control_path(path_to_project)[0]
        self._path_exist(path_to_project)
        command_load_project = f'FileIO::OpenAny "{path_to_project}"'
        return self.send(command_load_project)

    def run_project(self) -> str:
        """Runs aRTist using the current project state."""
        a = self.send("Engine::GoCmd")
        return a

    def save_img_project(self, path_save_img: str, img_name: str) -> str:
        """Saves the calculated image to a specified directory."""
        self._control_str(img_name)
        path_save_img = self._control_path(path_save_img)[0]
        self._path_exist(path_save_img)
        save_place_name = self._replace_slashes(os.path.join(path_save_img, img_name))

        ans = "Saved as: "

        cmd_save = (
            "Modules::Invoke ImageViewer SaveFile [file join $env(HOME) "
            + save_place_name
            + "] true"
        )
        ans += self.send(cmd_save)
        return ans

    def clear_project(self) -> str:
        """Clears the current aRTist workspace."""
        a = ""
        path = Path(
            self.send(
                "set newPath [file join [file dirname $Xray(LibraryDir)] clear.aRDir]"
            ).strip("\n")
        )

        main_scene_file = "main.scene"
        path_main_source = "Source/850EA03A0737499F45631C73A8C036FD.xrs"
        path_file = path / main_scene_file
        path_source_file = path / path_main_source
        path_file_str = path_file.as_posix()

        a += self.load_file(path_file_str)
        path_source_file_str = path_source_file.as_posix()
        a += self.load_file((path_source_file_str))
        return a

    def save_project(self) -> str:
        """Saves the current project."""
        a = self.send("XRayProject::SaveProjectCmd")
        return a
