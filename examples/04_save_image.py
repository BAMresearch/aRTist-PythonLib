from artistlib import SAVEMODES, API
from pathlib import Path

def main():
    # Initialize the api.
    artist_api = API()

    # Save Folder
    save_folder = Path('./workspace')
    save_folder.mkdir(exist_ok=True)

    # Save image / Save images and load them is fastern than to send the images via the rc connection.
    artist_api.save_image(save_folder / 'projection.tif', SAVEMODES.UINT16, save_projection_geometry=True)

if __name__ == '__main__':
    main()