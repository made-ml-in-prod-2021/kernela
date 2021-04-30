from importlib import import_module
import pickle


def dump_pickle(obj, path_to_file: str):
    with open(path_to_file, "wb") as dump_file:
        pickle.dump(obj, dump_file)


def load_dump(path_to_file: str):
    with open(path_to_file, "rb") as dump_file:
        return pickle.load(dump_file)


def get_class_type(fully_qualified_name: str):
    try:
        module_path, class_name = fully_qualified_name.rsplit(".", 1)
        module = import_module(module_path)
        return getattr(module, class_name)
    except (ImportError, AttributeError) as e:
        raise ImportError(fully_qualified_name)
