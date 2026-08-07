import multiprocessing
import artistlib as a
import time


def run(port):
    # time.sleep((port - 3658) * 5)
    path = "$Xray(LibraryDir)/ExampleParts/Fun/Dragon.stl"
    result_folder_pic = "$env(HOME) Pictures/"
    w = a.ArtistAll(port=port, multiple_starts=True)
    # w= a.ArtistAll(port=port)
    w.load_project(path)
    w.run_project()
    ans = w.save_img_project(result_folder_pic, f"Test_multi{port}.tiff")
    # time.sleep((port - 3658) * 5)
    a.close_artist(port)
    return ans


if __name__ == "__main__":
    with multiprocessing.Pool() as pool:
        ports = [3658, 3659, 3660, 3661, 3662, 3663, 3664]
        # ports = [3658,3659,3660]
        results = pool.map(run, ports)
        print(results)
