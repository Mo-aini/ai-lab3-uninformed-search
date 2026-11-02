# Lab 3 - runs all the search tasks
import platform

from src import lab3_bfs_dfs, lab3_depth_search, lab3_ucs


def main():
    print("AI Lab 3: Uninformed Search | Mohammed Emad ALaini")
    print("Python %s, standard library only" % platform.python_version())
    print()
    lab3_bfs_dfs.main()
    print()
    lab3_depth_search.main()
    print()
    lab3_ucs.main()


if __name__ == "__main__":
    main()
