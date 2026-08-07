from .launcher import launch_artist, close_artist as c_artist
from .ui import show_ui as s_ui, hide_ui as h_ui


def start_artist(
    path_specific_version=None, start_UI: bool = True, port=3658, multiple_starts=False
) -> None:
    """Starts aRTist from a Python script.
    The function searches for the default installation directory or prompts the user to start aRTist manually.
    The installation path is stored in a JSON file. After the first execution, this stored path is used automatically. Alternatively, a specific installation path can be provided.
    Set `start_UI=True` to display the aRTist user interface.
    """
    return launch_artist(
        path_specific_version=path_specific_version,
        start_UI=start_UI,
        port=port,
        multiple_starts=multiple_starts,
    )


def close_artist(port=3658) -> None:
    """Closes aRTist and resets the junction."""
    return c_artist(port)


def show_ui(name: str = "aRTist.exe") -> None:
    """Shows the aRTist user interface."""
    return s_ui(name)


def hide_ui(name: str = "aRTist.exe") -> None:
    """Hides the aRTist user interface."""
    return h_ui(name)
