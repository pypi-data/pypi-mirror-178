"""
Summary: Models importer functions.

Allows importing modules by name.
"""

import importlib.util
import sys
from types import ModuleType
from typing import Dict, Generator, List, Optional

from loguru import logger


def import_module(name: str, package: Optional[str] = None) -> ModuleType:
    """Import module by name.

    Auxiliary function to import modules by name.

    Args:
        name (str): Module name.
        package (str, optional): Package name. Defaults to None.

    Raises:
        ModuleNotFoundError: [description]

    Returns:
        ModuleType: [description]
    """
    absolute_name = importlib.util.resolve_name(name, package)
    try:
        return sys.modules[absolute_name]
    except KeyError:
        pass

    path = None
    if "." in absolute_name:
        parent_name, _, child_name = absolute_name.rpartition(".")
        parent_module = import_module(parent_name)
        path = parent_module.__spec__.submodule_search_locations
    for finder in sys.meta_path:
        spec = finder.find_spec(absolute_name, path)
        if spec is not None:
            break
    else:
        msg = f"No module named {absolute_name!r}"
        raise ModuleNotFoundError(msg, name=absolute_name)
    module = importlib.util.module_from_spec(spec)
    sys.modules[absolute_name] = module
    spec.loader.exec_module(module)
    if path is not None:
        setattr(parent_module, child_name, module)
    return module


def import_attr_from_module(module: str, module_attrs: List[str]) -> Generator:
    """Import any attribute from module.

    Args:
        module (str): [description]
        module_attrs (List[str]): [description]

    Raises: AttributeError

    Yields:
        Generator: yields module attributes.
    """
    for attr in module_attrs:
        try:
            attr_ = getattr(module, attr)
        except AttributeError as e:
            logger.exception(e)
        yield attr_


def import_from_config_file(modules: Dict[str, str]) -> List:
    """Import modules from config dictionary.

    Args:
        modules (Dict[str, str]): Dict of attribute name and value.

    """
    pass
