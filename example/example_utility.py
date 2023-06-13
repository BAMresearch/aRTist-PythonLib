import sartist
import numpy as np
from scipy.spatial.transform import Rotation


def main():
    initial_transform = np.eye(4)
    initial_transform[0, 3] = 0
    initial_transform[:3, :3] = Rotation.from_euler("X", 0, degrees=True).as_matrix()

    sartist.utility.circular_trajectory("data/projections/smart_ct", number_of_projections=12, initial_transform=initial_transform, fdd=1800, fod=750)


if __name__ == '__main__':
    main()
