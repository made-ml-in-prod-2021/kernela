from importlib import import_module


def get_class_type(fully_qualified_name: str):
    try:
        module_path, class_name = fully_qualified_name.rsplit(".", 1)
        module = import_module(module_path)
        return getattr(module, class_name)
    except (ImportError, AttributeError) as e:
        raise ImportError(fully_qualified_name)
