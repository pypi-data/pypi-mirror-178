"""
this module enable usage of modulefile in venv, virtualenv or conda python environments.
"""
import os
import sys


from .modulefile import ModuleBuilder
from .python_env import identify_env_status, test_module_import, upgrade_python_env, ENV_TYPE_CONDA
from .tools import logger


def initialize(options):  # pylint: disable=too-many-branches
    """
    Initialize the module file and place it in env.

    Parameters
    ----------
    options : Namespace
        argparse options read from parse_args method.

    Returns
    -------
    int
        Error code.
    """
    def _get_env():
        env_type, status, env_prefix = identify_env_status()
        if not status:
            raise AssertionError("To install in python environment, a venv, "
                                    "virtualenv or conda env must be already loaded.")
        if env_type == ENV_TYPE_CONDA:
            logger.warning(
                "Conda integration has never been tested."
                " Please contact a developer if errors occur.")
        return env_type, status, env_prefix

    env_type, _, env_prefix = _get_env()

    module_name = options.name
    module_directory = options.directory
    if not module_directory:
        if not env_prefix:
            raise AssertionError("A venv or a virtualenv or a conda env is expected"
                                    " if module directory is not defined.")
        module_directory = os.path.join(env_prefix, "etc", "modulefiles")

    if env_prefix:
        upgrade_python_env(env_type, env_prefix, module_directory, module_name)
    else:
        logger.warning(
            "Current module is not added to any python environnement.")

    prepend_paths = []
    if options.prepend_ld_library_path:
        for path in options.prepend_ld_library_path.split(":"):
            if path:
                prepend_paths.append(("LD_LIBRARY_PATH", path))
    prepend_paths.append(("LD_LIBRARY_PATH", os.path.join(os.path.abspath(env_prefix), 'lib')))

    if options.prepend_path:
        for path in options.prepend_path.split(":"):
            if path:
                prepend_paths.append(("PATH", path))

    if options.prepend_pythonpath:
        for path in options.prepend_pythonpath.split(":"):
            if path:
                prepend_paths.append(("PYTHONPATH", path))

    remove_paths = []
    if options.remove_paths:
        for elt in options.remove_paths:
            value = elt.split("=")
            if len(value) == 2:
                remove_paths.append((value[0], value[1].split(":")))
            else:
                raise ValueError(
                    f"'{elt}' is expected to contain a '=' between variable and paths"
                    f" ({options.remove_paths})")

    setenv_vars = {}
    if options.env_var:
        for elt in options.env_var:
            value = elt.split("=")
            if len(value) == 2:
                setenv_vars[value[0]] = value[1]
            else:
                raise ValueError(
                    f"'{elt}' is expected to contain a '=' between name and value"
                    f" ({options.env_var})")

    aliases = {}
    if options.aliases:
        for elt in options.aliases:
            value = elt.split("=")
            if len(value) == 2:
                aliases[value[0]] = value[1]
            else:
                raise ValueError(
                    f"'{elt}' is expected to contain a '=' between alias name and value"
                    f" ({options.aliases})")

    log_load=options.log_load
    if log_load:
        print("log_load")
        print(log_load)
        print("log_load")
        log_load=" ".join(log_load)

    mod_builder = ModuleBuilder(remove_paths=remove_paths,
                                prepend_paths=prepend_paths,
                                conflicts=options.module_conflict,
                                setenv_vars=setenv_vars,
                                aliases=aliases,
                                modules=options.module,
                                module_uses=options.module_use,
                                source_sh=options.source_sh,
                                log_load=log_load)

    return mod_builder.create(module_name=module_name,
                              module_directory=module_directory,
                              module_category=options.category if options.category\
                                                               else "custom_venv")


def test_import(options):
    """
    Tests imports of python modules.

    Parameters
    ----------
    options : Namespace
        argparse options read from parse_args method.

    Returns
    -------
    int
        Error code.
    """

    if options.verbose:
        print("Testing env :")

    failed = {}

    for module in set(options.modules):
        error = test_module_import(module, options.verbose)
        if error:
            failed[module] = error

    return len(failed)


def identify_environment(options):
    """Identify python environment.

    Parameters
    ----------
    options : Namespace
        argparse options read from parse_args method.

    Returns
    -------
    int
        Error code.
    """

    return 0 if identify_env_status(options.prefix, options.verbose) is not None else 1

def main(args=None):
    """Main program. Parse command line arguments or read it from function parameters.

    Parameters
    ----------
    args : List, optional
        Argument list, by default None

    Returns
    -------
    int
        Error code.

    Raises
    ------
    ValueError
        If python < 3.3 is used.
    """
    compatible = True
    if sys.version_info < (3, 3):
        compatible = False
    elif not hasattr(sys, 'base_prefix'):
        compatible = False
    if not compatible:
        raise ValueError('This script is only for use with Python >= 3.3')

    import argparse  # pylint: disable=import-outside-toplevel

    parser = argparse.ArgumentParser(prog=__name__,
                                        description='Creates module file to append in Python '
                                                    'virtual or conda environments. '
                                                    'The environment must be loaded before '
                                                    'the execution.',
                                        epilog='Once the module has been '
                                            'created, you should reload the environment.')
    subparsers = parser.add_subparsers(help="The following subcommands are available. "
                                            "See their help for more details.")
    parser_init = subparsers.add_parser("initialize", help='Initialize the modulefile and '
                                        'insert it in the python environment')
    parser_init.add_argument('name', metavar='MODULE_NAME',
                        help='Name of the module to create.')
    parser_init.add_argument('--directory', metavar='DIRECTORY',
                        help='Module directory')
    parser_init.add_argument('--category', metavar='CATEGORY', default="custom_env",
                        help='Category attribute of the module')
    parser_init.add_argument('--pre-env', action='store_true',
                                help='To load the module before the virtual environment.'
                                ' Only available for venv or virtualenv.')

    parser_init.add_argument('--prepend-pythonpath', metavar='some/paths/splits:by/two/dots',
                        help='Values to add to the existing PYTHONPATH')
    parser_init.add_argument('--prepend-ld-library-path', metavar='some/paths/splits:by/two/dots',
                        help='Values to add to the existing LD_LIBRARY_PATH')
    parser_init.add_argument('--prepend-path', metavar='some/paths/splits:by/two/dots',
                        help='Values to add to the existing PATH')
    parser_init.add_argument('--remove-paths',
                        metavar='VAR_NAME=one/path/:another/path/',
                        nargs='+', default=[],
                        help='Values to remove from the existing variables')
    parser_init.add_argument('--env-var', metavar='VAR=value', nargs='+', default=[],
                        help='Add variable to export as VAR=value')
    parser_init.add_argument('--aliases',
                        metavar='name1=value1 name2=value2',
                        nargs='+', default=[],
                        help='Add alias as name=value')
    parser_init.add_argument('--module', metavar='module_name', nargs='+', default=[],
                        help='Add module to load')
    parser_init.add_argument('--module-use', metavar='module_path', nargs='+', default=[],
                        help='Add module path to use')
    parser_init.add_argument('--module-conflict', metavar='module_name', nargs='+', default=[],
                        help='Add module conflict')
    parser_init.add_argument('--source-sh', metavar='source_file', nargs='+', default=[],
                        help='Add files to source')
    parser_init.add_argument('--log-load', metavar='message', nargs='+', default=None,
                        help='Add message when environment is loaded.')
    parser_init.set_defaults(func=initialize)


    parser_test = subparsers.add_parser("test", help='Tool to test import of modules')
    parser_test.add_argument('modules', metavar='PYTHON_MODULE', nargs='+', default=[],
                        help='Name of the pyhton modules to test import.')
    parser_test.add_argument('--verbose', action='store_true')
    parser_test.set_defaults(func=test_import)


    parser_idnt = subparsers.add_parser("identify",
                                        help='Identify the python environment. ',
                                        description=
                                        'Displays the environment type (None, venv or conda), '
                                        'its status (True if activated else False) '
                                        'and its prefix. "venv" type is a virtual environment '
                                        'from venv or virtualenv.')
    parser_idnt.add_argument('--prefix', metavar='environment/prefix/path', default=None,
                        help='Path to python environment prefix')
    parser_idnt.add_argument('--verbose', action='store_true', help='To display the result.')
    parser_idnt.set_defaults(func=identify_environment)

    options = parser.parse_args(args)
    return options.func(options)


if __name__ == '__main__':
    try:
        sys.exit(main())
    except Exception as exception:  # pylint: disable=broad-except
        print('Error: %s' % exception, file=sys.stderr)
