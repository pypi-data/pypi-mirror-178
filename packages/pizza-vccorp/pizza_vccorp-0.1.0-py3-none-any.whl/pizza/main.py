"""
Main entry point for the `pizza` command.

The code in this module is also a good example of how to use Pizza as a
library rather than a script.
"""
import logging
import os
import sys
from copy import copy

from pizza.config import get_user_config
from pizza.generate import generate_context, generate_files
from pizza.prompt import prompt_for_config
from pizza.replay import dump
from pizza.repository import determine_repo_dir
from pizza.utils import rmtree


logger = logging.getLogger(__name__)


def pizza(
    template,
    no_input,
    overwrite_if_exists=False,
    output_dir=".",
    config_file=None,
    default_config=False,
    password=None,
    directory=None,
    skip_if_file_exists=False,
    keep_project_on_failure=False,
):
    """
    Run Pizza just as if using it from the command line.

    :param template: A directory containing a project template directory,
        or a URL to a git repository.
    :param output_dir: Where to output the generated project dir into.
    :param config_file: User configuration file path.
    :param default_config: Use default values rather than a config file.
    :param password: The password to use when extracting the repository.
    :param directory: Relative path to a pizza template in a repository.
    :param keep_project_on_failure: If `True` keep generated project directory even when
        generation fails
    """

    config_dict = get_user_config(
        config_file=config_file,
        default_config=default_config,
    )

    repo_dir, cleanup = determine_repo_dir(
        template=template,
        abbreviations=config_dict["abbreviations"],
        clone_to_dir=config_dict["pizzas_dir"],
        password=password,
        directory=directory,
    )
    import_patch = _patch_import_path_for_repo(repo_dir)

    template_name = os.path.basename(os.path.abspath(repo_dir))
    
    context_file = os.path.join(repo_dir, "pizza.json")
    logger.debug("context_file is %s", context_file)

    context = generate_context(
        context_file=context_file,
        default_context=config_dict["default_context"],
    )
    # prompt the user to manually configure at the command line.
    with import_patch:
        context["pizza"] = prompt_for_config(context, no_input)

    # include template dir or url in the context dict
    context["pizza"]["_template"] = template

    # include output+dir in the context dict
    context["pizza"]["_output_dir"] = os.path.abspath(output_dir)

    dump(config_dict["replay_dir"], template_name, context)

    # Create project from local context and project template.
    with import_patch:
        result = generate_files(
            repo_dir=repo_dir,
            context=context,
            overwrite_if_exists=overwrite_if_exists,
            skip_if_file_exists=skip_if_file_exists,
            output_dir=output_dir,
            keep_project_on_failure=keep_project_on_failure,
        )

    # Cleanup (if required)
    if cleanup:
        rmtree(repo_dir)

    return result


class _patch_import_path_for_repo:
    def __init__(self, repo_dir):
        self._repo_dir = repo_dir
        self._path = None

    def __enter__(self):
        self._path = copy(sys.path)
        sys.path.append(self._repo_dir)

    def __exit__(self, type, value, traceback):
        sys.path = self._path
