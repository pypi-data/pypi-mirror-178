
from __future__ import annotations

import sys
import importlib.util

from .__init__ import *
from . import __config__


def import_module_path(path, load=True) :
    """Import a module by given path.

    Parameters:
        path:
            Path to module file to import.
        load:
            If the module should be loaded.

    Returns:
        Module instance.
    """
    name = f'{__config__.INIT_CONFIG["conditor.file_module_prefix"]}{str(path.resolve())}'
    if name not in sys.modules :
        spec = importlib.util.spec_from_file_location(name, path)
        sys.modules[name] = importlib.util.module_from_spec(spec)
        if load :
            spec.loader.exec_module(sys.modules[name])
        pass
    return sys.modules[name]

def find_project_root(context_path) :
    """Find project root path from given path.

    Parameters:
        context_path:
            Path withing a Conditor project to search.

    Returns:
        Root dictionary of found project.
        `None` if no Conditor project was found.
    """
    context_path = pathlib.Path(context_path).resolve()
    if context_path.is_file() :
        context_path = context_path.parent.resolve()
        pass
    while context_path != pathlib.Path(context_path.root).resolve() :
        for child in context_path.iterdir() :
            if child.is_file() and child.name == __config__.INIT_CONFIG['conditor.cpm.filename'] :
                return context_path
            pass
        context_path = context_path.parent.resolve()
        pass
    return None

