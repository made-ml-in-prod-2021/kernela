import pickle
import pathlib

from typing import Any, Union


def load_pickle(path_to_dump: Union[str, pathlib.Path]) -> Any:
    with open(path_to_dump, "rb") as dump_file:
        return pickle.load(dump_file)
