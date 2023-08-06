"""Module to manage python env.
"""
import importlib
import os
import shutil
from typing import Tuple

from .tools import create_path_if_needed, logger, package_name

ENV_TYPE_VENV = "venv"
ENV_TYPE_CONDA = "conda"

def test_module_import(module_name: str, verbose: bool) -> str:
    """Test module import.

    Parameters
    ----------
    module_name : str
        Name of the module to test.
    verbose : bool
        True to print result.

    Returns
    -------
    str
        Import error description if any. Else None.
    """

    error = None
    try:
        module = importlib.import_module(module_name)
    except ImportError as err:
        error = err

    if verbose:
        print(">>> import {}:".format(module_name))
        if error:
            print("  FAILED {}".format(error))
        else:
            print("  {}".format(module.__file__))
    return error


def identify_env_status(prefix: str = None, verbose: bool = False) -> Tuple[str, bool, str]:  # pylint: disable=too-many-branches
    """Identify environment type, status and prefix.

    Parameters
    ----------
    prefix : str, optional
        Path to environment, by default None.
    verbose : bool, optional
        True to print result, by default None.

    Returns
    -------
    Tuple[str, bool, str]
        ('conda'|'venv', activated|not_activated, prefix)
    """

    env_type = None
    status = False
    if "VIRTUAL_ENV" in os.environ:
        env_type = ENV_TYPE_VENV
        status = True
        if prefix:
            if os.path.realpath(prefix) != os.environ["VIRTUAL_ENV"]:
                raise AssertionError(f"prefix ({prefix}) is not coherent with "
                                     f"VIRTUAL_ENV variable ({os.environ['VIRTUAL_ENV']}).")
        prefix = os.environ["VIRTUAL_ENV"]
    elif "CONDA_PREFIX" in os.environ:
        if not os.environ["CONDA_DEFAULT_ENV"] == "base":
            env_type = ENV_TYPE_CONDA
            status = True
            if prefix:
                if os.path.realpath(prefix) != os.environ["CONDA_PREFIX"]\
                    and prefix != os.path.split(os.environ["CONDA_PREFIX"])[-1]:
                    raise AssertionError(f"prefix ({prefix}) is not coherent with "
                                        f"CONDA_PREFIX variable ({os.environ['CONDA_PREFIX']}).")
            prefix = os.environ["CONDA_PREFIX"]
    elif prefix:
        if os.path.isfile(os.path.join(os.path.realpath(prefix), "bin", "activate")):
            env_type = ENV_TYPE_VENV
            status = False
            prefix = os.path.realpath(prefix)
        else:
            try:
                import conda.cli.python_api as conda_api  # pylint: disable=import-outside-toplevel
                for env in [line.split()
                            for line in conda_api.run_command('info', '--envs')[0].splitlines()
                                if not line.strip().startswith("#") and
                                    line.split() and line.split()[0] != 'base']:
                    if os.path.realpath(prefix) in env:
                        env_type = ENV_TYPE_CONDA
                        status = False
                        prefix = env[-1]
            except ImportError:
                pass

    if verbose:
        print(f"{env_type} {status} {prefix}")

    if env_type:
        return env_type, status, prefix
    return None

USE_MODULE_TEMPLATE = """module use "__module_dir__"
"""
LOAD_MODULE_TEMPLATE = """module load '__module_name__'
"""

UNLOAD_MODULE_TEMPLATE = """    module unload '__module_name__'
"""
UNUSE_MODULE_TEMPLATE = """    module unuse "__module_dir__"
"""

def upgrade_venv(env_prefix: str, modulefile_directory: str, modulefile_name: str):  # pylint: disable=too-many-branches,too-many-locals,too-many-statements
    """Ugrade virtual env with modulefile at activate and deactivate.

    Parameters
    ----------
    env_prefix : str
        Path to environment.
    modulefile_directory : str
        Path to modulefile directory.
    modulefile_name : str
        Modulefile name.

    Raises
    ------
    AssertionError
        If the activate script is not found.
    AssertionError
        If the module is already loaded frome the script but from another modulefile directory.
    """
    bin_dir = os.path.join(env_prefix, "bin")

    activate_src = os.path.join(bin_dir, "activate")
    if not os.path.isfile(activate_src):
        raise AssertionError(f'"activate" file is expected in {bin_dir}.')

    header_line = f"# This file is generated from {package_name}"\
                " from regular venv or virtualenv file."

    unuse_module = UNUSE_MODULE_TEMPLATE.replace("__module_dir__", modulefile_directory)
    unload_module = UNLOAD_MODULE_TEMPLATE.replace("__module_name__", modulefile_name)

    load_module = LOAD_MODULE_TEMPLATE.replace("__module_name__", modulefile_name)
    use_module = USE_MODULE_TEMPLATE.replace("__module_dir__", modulefile_directory)

    use_path_present = False
    with open(activate_src, "r") as src_file:
        file_read = src_file.read()
        already_modulefile_for_env = False
        if header_line in file_read:
            already_modulefile_for_env = True
            logger.warning(
                "Existing virtual environment is already a modulefile_for_env environment.")
            if load_module in file_read:
                logger.warning("%s already loaded from this python environment.", modulefile_name)
                if not use_module in file_read:
                    raise AssertionError(f"{modulefile_name} is loaded but "
                                         f"not from {modulefile_directory} in {activate_src}.")
                return
            if use_module in file_read:
                use_path_present = True

    with open(activate_src, "r") as src_file:
        src_lines = src_file.readlines()

    tmp_path = os.path.join(env_prefix, "tmp", "modulefile_for_env")
    create_path_if_needed(tmp_path)
    activate_tmp = os.path.join(tmp_path, "activate")

    with open(activate_tmp, "w") as tmp_file:

        def _write_in_file(tmp_file, line, to_write):
            if to_write:
                if to_write[0] == -1:
                    tmp_file.write(to_write[1])
                    tmp_file.write(line)
                elif to_write[0] == 1:
                    tmp_file.write(line)
                    tmp_file.write(to_write[1])
                elif to_write[0] == 0:
                    tmp_file.write(line)

        if already_modulefile_for_env:
            append_load = append_use = 0
            for count, line in enumerate(src_lines):
                to_write = None
                if "Unload non-Python dependencies" in line:
                    to_write = (1, unload_module + "" if use_path_present else unuse_module)
                else:
                    if 'module use "' in line and not use_path_present:
                        append_use += 1
                    elif append_use:
                        to_write = [-1, use_module]
                        append_use = 0
                    if "module load '" in line :
                        append_load += 1
                    elif append_load:
                        to_write = [-1, load_module]
                        append_load = 0

                    to_write = to_write if to_write else (0, "")

                _write_in_file(tmp_file, line, to_write)
        else:
            reset_is_done = 0
            deactivate_nondestructive = 0
            for count, line in enumerate(src_lines):
                to_write = None
                if count == 2:
                    to_write = (-1, f"{header_line}\n")
                elif "reset old environment variables" in line:
                    to_write = (-1, "\n    # Unload non-Python dependencies\n"\
                        + unload_module + unuse_module + "\n")
                    reset_is_done += 1
                elif "deactivate nondestructive" in line:
                    to_write = (1, "\n# Load non-Python dependencies\n" + use_module + load_module)
                    deactivate_nondestructive += 1
                else:
                    to_write = (0, "")

                _write_in_file(tmp_file, line, to_write)

            if reset_is_done != 1:
                logger.error(
                    "'reset old environment variables' has been found %s"
                    " times in activate script. It is expectet to be 1 time.", reset_is_done)
            if deactivate_nondestructive != 1:
                logger.error(
                    "'deactivate nondestructive' has been found %s"
                    " times in activate script. It is expectet to be 1 time.",
                    deactivate_nondestructive)

    shutil.copyfile(activate_tmp, activate_src)
    shutil.rmtree(tmp_path)
    return


def upgrade_conda(env_prefix: str, modulefile_directory: str, modulefile_name: str):
    """Ugrade conda env with modulefile at activate and deactivate.

    Parameters
    ----------
    env_prefix : str
        Path to environment.
    modulefile_directory : str
        Path to modulefile directory.
    modulefile_name : str
        Modulefile name.
    """
    conda_activate_path = os.path.join(env_prefix, "etc", "conda", "activate.d")
    create_path_if_needed(conda_activate_path)
    with open(os.path.join(conda_activate_path, "modulefile.sh"), "w") as modulefile:
        modulefile.write(
            USE_MODULE_TEMPLATE.replace("__module_dir__", modulefile_directory))
        modulefile.write(
            LOAD_MODULE_TEMPLATE.replace("__module_name__", modulefile_name))

    conda_deactivate_path = os.path.join(env_prefix, "etc", "conda", "deactivate.d")
    create_path_if_needed(conda_deactivate_path)
    with open(os.path.join(conda_deactivate_path, "modulefile.sh"), "w") as modulefile:
        modulefile.write(
            UNLOAD_MODULE_TEMPLATE.replace("__module_name__", modulefile_name).strip())
        modulefile.write(
            UNUSE_MODULE_TEMPLATE.replace("__module_dir__", modulefile_directory).strip())

def upgrade_python_env(env_type: str,
                       env_prefix: str,
                       modulefile_directory: str,
                       modulefile_name: str):
    """Ugrade env with modulefile at activate and deactivate.

    Parameters
    ----------
    env_type : str
        Type of environment.
    env_prefix : str
        Path to environment.
    modulefile_directory : str
        Path to modulefile directory.
    modulefile_name : str
        Modulefile name.
    """

    if env_type == ENV_TYPE_VENV:
        upgrade_venv(env_prefix, modulefile_directory, modulefile_name)

    elif env_type == ENV_TYPE_CONDA:
        upgrade_conda(env_prefix, modulefile_directory, modulefile_name)
