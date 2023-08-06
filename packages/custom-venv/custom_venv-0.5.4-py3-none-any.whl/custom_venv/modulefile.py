"""Creates modulefile.
"""
import os
from typing import Dict, List, Tuple

from .tools import create_path_if_needed, remove_duplicates

MODULE_TEMPLATE_TCL="""#%Module -*- tcl -*-
##
## modulefile for __name__
##
#Global infos
set              category             __category__
set              name                 __name__

proc ModulesHelp { } {

  puts stderr "\tAdds $name to your environment variables,"
}

module-whatis "adds $name to your environment variables"

__log_load__

#conflicts, prereq
conflict $category
__conflicts__

# Files to source
__source_files__
# Additional modules
__module_use__
__modules__
# Additional exports
__setenv__
# Prepend variables
__prepend_path__
# Remove path
__remove_path__
# Set aliases
__set_aliases__
"""

class ModuleBuilder:  # pylint: disable=too-few-public-methods,too-many-instance-attributes
    """Class to generate the modulefile.
    """

    def __init__(self,  # pylint: disable=too-many-arguments
                 remove_paths: List[Tuple] = None,
                 prepend_paths: List[Tuple] = None,
                 setenv_vars: Dict[str, str] = None,
                 aliases: Dict[str, str] = None,
                 conflicts: List = None,
                 modules: List = None,
                 module_uses: List = None,
                 source_sh: List = None,
                 log_load: str = None) -> None:
        self.remove_paths = remove_paths
        self.prepend_paths = prepend_paths
        self.setenv_vars = setenv_vars
        self.aliases = aliases
        self.conflicts = conflicts
        self.modules = modules
        self.module_uses = module_uses
        self.source_sh = source_sh
        self.log_load = log_load

    def create(self,
               module_name: str,
               module_directory: str,
               module_category: str = None):
        """Creates a module file and optionnally installs it in a python environment.

        Parameters
        ----------
        module_name : str
            Name of the module to create
        module_directory : str, optional
            Module directory, by default None
        module_category : str, optional
            Module category, by default None

        Raises
        ------
        AssertionError
            _description_
        AssertionError
            _description_
        AssertionError
            _description_
        """

        create_path_if_needed(module_directory)

        module_file_name = os.path.join(module_directory, module_name)

        module_file = MODULE_TEMPLATE_TCL.replace("__name__", module_name)
        module_file = module_file.replace("__category__", module_category)

        to_replace = ""
        for value in remove_duplicates(self.conflicts):
            to_replace += f"conflict {value}\n"
        module_file = module_file.replace("__conflicts__", to_replace)

        to_replace = ""
        for var, value in self.setenv_vars.items():
            to_replace += f"setenv {var} {value}\n"
        module_file = module_file.replace("__setenv__", to_replace)

        to_replace = ""
        for var, value in self.aliases.items():
            to_replace += f"set-alias {var} {value}\n"
        module_file = module_file.replace("__set_aliases__", to_replace)

        to_replace = ""
        for var, value in remove_duplicates(self.prepend_paths):
            to_replace += f"prepend-path {var} {value}\n"
        module_file = module_file.replace("__prepend_path__", to_replace)

        to_replace = ""
        for var, paths in self.remove_paths:
            for path in paths:
                to_replace += f"remove-path {var} {path}\n"
        module_file = module_file.replace("__remove_path__", to_replace)

        to_replace = ""
        for value in remove_duplicates(self.module_uses):
            to_replace += f"module use {value}\n"
        module_file = module_file.replace("__module_use__", to_replace)

        to_replace = ""
        for value in remove_duplicates(self.modules):
            to_replace += f"module load {value}\n"
        module_file = module_file.replace("__modules__", to_replace)

        to_replace = ""
        for value in remove_duplicates(self.source_sh):
            to_replace += f"source-sh bash {value} >> /dev/null\n"
        module_file = module_file.replace("__source_files__", to_replace)

        to_replace = ""
        if self.log_load:
            log_load = self.log_load.replace('[', '\[').replace(']', '\]')
            to_replace = 'if [ module-info mode load ] {\n'\
                         f'    puts stderr "{log_load}"\n'\
                         '}'
        module_file = module_file.replace("__log_load__", to_replace)

        with open(module_file_name, "w") as mod_file:
            mod_file.write(module_file)
            return 0
        return 1
