
from __future__ import annotations

from typing import Any
import collections.abc
import pathlib
import json

import conditor
import conditor.__config__

PathLike = pathlib.Path|str
"""Path like type."""


class ConfigManager :
    """Project configuration manager

    Stores and manages project configuration entries.
    """

    def __init__(self, project:conditor.Project) :
        """Initialize configuration manager.

        Parameters:
            project:
                Reference to related project instance.
        """

        self.project:conditor.Project = project
        """Reference to related project instance."""

        self.entries = []
        """List of configuration entries."""

        self.default_map_interface:DefaultMapInterface = DefaultMapInterface(self)
        """Interface instance for configuration access as map."""

        self.string_map_interface:StringMapInterface = StringMapInterface(self)
        """Interface instance for configuration access as map casting strings."""

        self.locals_map_interface:LocalsMapInterface = LocalsMapInterface(self)
        """Interface to set persistent local configuration entry values."""

        # Load initial configuration.
        self.load_init()

        return

    def __str__(self) -> str:
        return self.__repr__()
    def __repr__(self) -> str:
        return f'ConfigManager({str(self.project)})'

    def load_init(self) :
        """Load initial conditor configuration."""
        init_config = conditor.__config__.INIT_CONFIG.copy()
        self.set_nvp_dict(init_config)
        _c = self.default_map_interface
        _c['path'] = self.project.path
        _c['path.cpm'] =        _c['path'].joinpath(f'./{_c["conditor.cpm.filename"]}').resolve()
        return

    def load_defaults(self) :
        """Load conditor default configuration."""
        _c = self.default_map_interface
        _c['path.source'] =     _c['path'].joinpath(f'./src').resolve()
        _c['path.docsrc'] =     _c['path'].joinpath(f'./docs').resolve()
        _c['path.build'] =      _c['path'].joinpath(f'./build').resolve()
        _c['path.distribute'] = _c['path'].joinpath(f'./dist').resolve()
        _c['path.loccfg'] =     _c['path'].joinpath(f'./.locals.json').resolve()
        return

    def load_locals(self) :
        """Load locals configuration entries."""
        locals_path = self.default_map_interface['path.loccfg']
        if not locals_path.exists() :
            return
        locals_dict = json.loads(locals_path.read_text())
        for entry_name in locals_dict :
            self.add_entry(LocalsEntry(self.project, entry_name))
            pass
        return

    def get_value(self, name:str, fallback:Any=None) -> Any :
        """Get config entry value.

        Get a configuration entry value by name.

        Parameters:
            name:
                Name of configuration entry to return.
            fallback:
                Value to return, if no configuration entry of this name exists.

        Returns:
            Value of requested configuration entry or fallback.
        """
        entry = self.get_entry(name)
        if entry is None :
            return fallback
        return entry.value

    def set_value(self, name:str, value:Any) :
        """Set config entry value.

        Set a configuration entry value by name.

        Parameters:
            name:
                Name of the configuration entry.
            value:
                New value of configuration entry.
        """
        entry = self.get_entry(name)
        if entry is None :
            entry = Entry(self.project, name)
            self.add_entry(entry)
            pass
        entry.value = value
        return

    def has_entry(self, name:str) -> bool :
        """If entry exists.

        Check existence of a configuration entry by given name.

        Patameters:
            name:
                Name of the configuration entry to check.
        """
        if name in self.entry_names :
            return True
        return False

    @property
    def entries_dict(self) -> dict[str, Entry] :
        """Composes list of all entries as dictionary indexed by name containing entry instance."""
        entries_dict = {}
        for entry in self.entries :
            entries_dict[entry.name] = entry
            pass
        return entries_dict

    @property
    def entry_names(self) -> list[str] :
        """List all configuration entry names."""
        names = []
        for entry in self.entries :
            names.append(entry.name)
            pass
        return names


    def get_entry(self, name:str) -> Entry :
        """Get entry object by name.

        Parameters:
            name:
                Name of configuration entry to get.

        Returns:
            Configuration entry matching name or `None` if not found.
        """
        for entry in self.entries :
            if entry.name == name :
                return entry
            pass
        return None

    def add_entry(self, entry:Entry, replace:bool=True) :
        """Add or replace configuration entry.

        Parameters:
            entry:
                New entry to add.
            replace:
                If a matching entry exists, replace it.
        """
        if entry.name in self.entry_names :
            if not replace :
                return
            self.entries.remove(self.get_entry(entry.name))
            return
        self.entries.append(entry)
        return

    def set_nvp_dict(self, entries_dict:dict) :
        """Set configuration by name value pair dictionary.

        Parameters:
            entries_dict:
                Dictionary of `{name: value}` configuration to set.
        """
        for entry_name in entries_dict :
            self.add_entry(Entry(self.project, entry_name, entries_dict[entry_name]))
            pass
        return

    def set_json_file(self, json_path:PathLike) :
        """Set configuration by given json file.

        Parameters:
            json_path:
                Path of json file to load entries from.
        """
        json_path = pathlib.Path(json_path).resolve()
        json_dict = json.loads(json_path.read_text())
        for entry_name in json_dict :
            self.add_entry(JsonFileEntry(self.project, entry_name, json_path))
            pass
        return

    pass


class Entry :
    """Configuration entry superclass."""

    def __init__(self, project:conditor.Project, name:str, value:Any=None) :
        """Initialize new configuration entry.

        Parameters:
            project:
                Instance of related conditor project.
            name:
                Name of this configuration entry.
            value:
                Initial value of this configuration entry.

        Warning:
            Entry has to be apended to config manager entries.
            Use set functions from config manager is recommended.
        """

        self.project:conditor.Project = project
        """Reference to related project."""

        self.name:str = name
        """Name of this configuration entry."""

        self._value:Any = value
        """Initial value of this configuration entry."""

        return

    def __str__(self) :
        return self.__repr__()
    def __repr__(self):
        return f'{type(self).__name__}({self.name})'

    @property
    def value(self) :
        """Get and set value of this configuration entry."""
        return self._value
    @value.setter
    def value(self, value) :
        self._value = value
        return

    pass

class JsonFileEntry (Entry) :
    """Configuration entry from JSON file."""

    def __init__(self, project, name, json_path) :
        """Initialze JSON file configuration entry.

        Parameters:
            project:
                Instance of related conditor project.
            name:
                Name of this configuration entry.
            json_path:
                Path to JSON file containing this entry.
        """
        super().__init__(project, name)

        self.path = pathlib.Path(json_path).resolve()
        """Path of JSON file storing this entry."""

        return

    def get_json(self) -> dict :
        """Get dictionary of file contents.

        Returns:
            Dictionary of json file or empty dict if not existing.
        """
        if not self.path.exists() :
            return {}
        json_str = self.path.read_text()
        json_dict = json.loads(json_str)
        return json_dict

    def set_json(self, json_dict:dict) :
        """Set dictionary in JSON file.

        Parameters:
            json_dict:
                Dictionary of JSON contents to write to file.
        """
        json_str = json.dumps(json_dict)
        if not self.path.parent.exists() :
            self.path.parent.mkdir(parents=True)
            pass
        self.path.write_text(json_str)
        return

    @property
    def value(self) :
        json_dict = self.get_json()
        return json_dict[self.name]
    @value.setter
    def value(self, value) :
        json_dict = self.get_json()
        json_dict[self.name] = value
        self.set_json(json_dict)
        return

    pass


class LocalsEntry (JsonFileEntry) :
    """Persistent local configuration entry."""

    @classmethod
    def convert(cls, entry:Entry) -> LocalsEntry :
        """Convert any existing configuration entry to a local configuration entry.

        Parameters:
            entry:
                Entry to convert.

        Returns:
            Converted locals entry.
        """
        loc_entry = cls(entry.project, entry.name)
        loc_entry.value = entry.value
        return loc_entry

    def __init__(self, project, name) :
        super().__init__(project, name, project.config['path.loccfg'])
        return

    pass


class DefaultMapInterface (collections.abc.MutableMapping):
    """Default configuration manager map interface.

    Interface to access configuration entries as mutable map.
    """

    def __init__(self, config_manager:ConfigManager) :

        self.config_manager:ConfigManager = config_manager
        """Reference to related configuration manager."""

        return

    def __str__(self) -> str :
        return self.__repr__()
    def __repr__(self) -> str :
        return f'DefaultMapInterface({str(self.config_manager)})'

    def __contains__(self, name:str) -> bool :
        return self.config_manager.has_entry(name)

    def __getitem__(self, name:str) -> Any :
        return self.config_manager.get_value(name)

    def __setitem__(self, name:str, value:Any) :
        return self.config_manager.set_value(name, value)

    def __delitem__(self, name:str) :
        return self.config_manager.del_entry(name)

    def __iter__(self) :
        return self.config_manager.entries_dict.__iter__()

    def __len__(self) :
        return self.config_manager.entries_dict.__len__()

        return


class StringMapInterface (collections.abc.Mapping):
    """String configuration map interface
    
    Interface to access configuration entries, casting return values as strings.
    """

    def __init__(self, config_manager:ConfigManager) :

        self.config_manager:ConfigManager = config_manager
        """Reference to related configuration manager."""

        return

    def __str__(self) -> str :
        return self.__repr__()
    def __repr__(self) -> str :
        return f'StringMapInterface({str(self.config_manager)})'

    def __contains__(self, name:str) -> bool :
        return self.config_manager.has_entry(name)

    def __getitem__(self, name:str) -> Any :
        return str(self.config_manager.get_value(name))

    def __iter__(self) :
        return self.config_manager.entries_dict.__iter__()

    def __len__(self) :
        return self.config_manager.entries_dict.__len__()

        return

    pass


class LocalsMapInterface (collections.abc.MutableMapping):
    """Map interface to set persistent local configuration entry values."""

    def __init__(self, config_manager:ConfigManager) :

        self.config_manager:ConfigManager = config_manager
        """Reference to related configuration manager."""

        return

    def __str__(self) -> str :
        return self.__repr__()
    def __repr__(self) -> str :
        return f'LocalsMapInterface({str(self.config_manager)})'

    def __contains__(self, name:str) -> bool :
        return self.config_manager.has_entry(name)

    def __getitem__(self, name:str) -> Any :
        entry = self.config_manager.get_entry(name)
        if entry is not None and type(entry) != LocalsEntry :
            LocalsEntry.convert(entry)
            pass
        return self.config_manager.get_value(name)

    def __setitem__(self, name:str, value:Any) :
        entry = self.config_manager.get_entry(name)
        if entry is None :
            entry = LocalsEntry(self.config_manager.project, name)
            pass
        elif type(entry) != LocalsEntry :
            entry = LocalsEntry.convert(entry)
            pass
        return self.config_manager.set_value(name, value)

    def __delitem__(self, name:str) :
        return self.config_manager.del_entry(name)

    def __iter__(self) :
        return self.config_manager.entries_dict.__iter__()

    def __len__(self) :
        return self.config_manager.entries_dict.__len__()

        return

