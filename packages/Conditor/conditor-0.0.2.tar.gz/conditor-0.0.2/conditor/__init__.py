
from __future__ import annotations

import inspect
import pathlib
import importlib.util
import sys
import collections.abc

from . import __config__
from . import config
from . import action
from . import build
from . import util
from . import compose


_INSTANCES:dict = {}
"""Initialized project instances

Dictionary of already initialized project instances indexed by absolute project path.
"""


class Project :
    """Conditor Project

    Instance representing a Conditor project."""

    @classmethod
    def get(cls,
        context_path : pathlib.Path | str | None = None
    ) -> Project | None :
        """Get project

        Factory class method to get a project instance by given path.

        Parameters:
            context_path:
                Path from which the project root will be searched.
                If `None`, the file location where this function was called will be used.

        Returns:
            Initialized instance of this project or `None`, if project root path was not found.
        """
        if context_path is None :
            context_path = inspect.stack()[1].filename
            pass
        project_root = util.find_project_root(context_path)
        if project_root is None :
            return None
        if str(project_root) not in _INSTANCES :
            _INSTANCES[str(project_root)] = Project(project_root)
            _INSTANCES[str(project_root)].load()
            pass
        return _INSTANCES[str(project_root)]

    def __init__(self, path:pathlib.Path) :
        """Initialize project instance.

        Parameters:
            path:
                Path to project root.

        Danger:
            Use factory function.

        """

        self.path:pathlib.Path = path
        """Root path of this project. Used as primary identifier for projects."""

        self.config_manager:config.ConfigManager = config.ConfigManager(self)
        """Instance of project configuration manager."""

        self.action_manager:action.ActionManager = action.ActionManager(self)
        """Instance of project action manager."""

        self.recipe_manager:build.BuildManager = build.RecipeManager(self)
        """Instance of project build recipe manager."""

        self.composer = compose.Composer(self)
        """Instance of this projects composer."""

        self._cpm_module = None
        """Instance of CPM module."""

        return

    def __str__(self) -> str :
        return self.__repr__()
    def __repr__(self) -> str :
        return f'Project({str(self.path)})'

    @property
    def config(self) -> config.DefaultMapInterface :
        """Configuration map interface."""
        return self.config_manager.default_map_interface

    @property
    def strcfg(self) -> config.StringMapInterface :
        """String casted configuration map interface."""
        return self.config_manager.string_map_interface

    @property
    def loccfg(self) -> config.StringMapInterface :
        """Persistent local configuration map interface."""
        return self.config_manager.locals_map_interface

    @property
    def action(self) -> action.DefaultMapInterface :
        """Action map interface."""
        return self.action_manager.default_map_interface

    @property
    def stract(self) -> action.StringMapInterface :
        """String casted actions map interface."""
        return self.action_manager.string_map_interface

    @property
    def recipe(self) :
        """Build recipe map interface."""
        return self.recipe_manager

    def load(self) :
        """Loads all project data."""

        # Import CPM.
        self._cpm_module = util.import_module_path(self.config['path.cpm'], load=False)

        # set CPM attributes.
        setattr(self._cpm_module, self.config['conditor.cpm.project_var_name'], self)

        # Execute CPM load.
        self._cpm_module.__loader__.exec_module(self._cpm_module)

        return

    pass

