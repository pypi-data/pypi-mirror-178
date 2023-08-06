"""Main `pizza` CLI."""
import collections
import json
import os
import sys

import click
from pizza import __version__
from pizza.config import get_user_config
from pizza.exceptions import (
    ContextDecodingException,
    InvalidModeException,
    OutputDirExistsException,
    RepositoryCloneFailed,
    RepositoryNotFound,
    UndefinedVariableInTemplate,
    UnknownExtension,
)
from pizza.main import pizza


def version_msg():
    """Return the Pizza version, location and Python powering it."""
    python_version = sys.version
    location = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return f"Pizza {__version__} from {location} (Python {python_version})"


def validate_extra_context(ctx, param, value):
    """Validate extra context."""
    for string in value:
        if "=" not in string:
            raise click.BadParameter(
                f"EXTRA_CONTEXT should contain items of the form key=value; "
                f"'{string}' doesn't match that form"
            )

    # Convert tuple -- e.g.: ('program_name=foobar', 'startsecs=66')
    # to dict -- e.g.: {'program_name': 'foobar', 'startsecs': '66'}
    return collections.OrderedDict(s.split("=", 1) for s in value) or None


def list_installed_templates(default_config, passed_config_file):
    """List installed (locally cloned) templates. Use pizza --list-installed."""
    config = get_user_config(passed_config_file, default_config)
    pizza_folder = config.get("pizzas_dir")
    if not os.path.exists(pizza_folder):
        click.echo(
            f"Error: Cannot list installed templates. " f"Folder does not exist: {pizza_folder}"
        )
        sys.exit(-1)

    template_names = [
        folder
        for folder in os.listdir(pizza_folder)
        if os.path.exists(os.path.join(pizza_folder, folder, "pizza.json"))
    ]
    click.echo(f"{len(template_names)} installed templates: ")
    for name in template_names:
        click.echo(f" * {name}")


@click.command(context_settings=dict(help_option_names=["-h", "--help"]))
@click.version_option(__version__, "-V", "--version", message=version_msg())
@click.argument("template", required=False)
@click.option(
    "--no-input",
    is_flag=True,
    help="Do not prompt for parameters and only use pizza.json file content. "
    "Defaults to deleting any cached resources and re-downloading them. "
    "Cannot be combined with the --replay flag.",
)

@click.option(
    "-f",
    "--overwrite-if-exists",
    is_flag=True,
    help="Overwrite the contents of the output directory if it already exists",
)
@click.option(
    "-s",
    "--skip-if-file-exists",
    is_flag=True,
    help="Skip the files in the corresponding directories if they already exist",
    default=False,
)
@click.option(
    "-o",
    "--output-dir",
    default=".",
    type=click.Path(),
    help="Where to output the generated project dir into",
)

@click.option("--config-file", type=click.Path(), default=None, help="User configuration file")

@click.option(
    "--default-config",
    is_flag=True,
    help="Do not load a config file. Use the defaults instead",
)


def main(
    template,
    no_input,
    overwrite_if_exists,
    output_dir,
    config_file,
    default_config,
    skip_if_file_exists,
):
    """Create a project from a Pizza project template (TEMPLATE)."""

    # Raising usage, after all commands that should work without args.
    if not template or template.lower() == "help":
        click.echo(click.get_current_context().get_help())
        sys.exit(0)

    try:
        pizza(
            template,
            no_input,
            overwrite_if_exists=overwrite_if_exists,
            output_dir=output_dir,
            config_file=config_file,
            default_config=default_config,
            password=os.environ.get("PIZZA_REPO_PASSWORD"),
            directory=None,
            skip_if_file_exists=skip_if_file_exists,
        )
    except (
        ContextDecodingException,
        OutputDirExistsException,
        InvalidModeException,
        UnknownExtension,
        RepositoryNotFound,
        RepositoryCloneFailed,
    ) as e:
        click.echo(e)
        sys.exit(1)
    except UndefinedVariableInTemplate as undefined_err:
        click.echo(f"{undefined_err.message}")
        click.echo(f"Error message: {undefined_err.error.message}")

        context_str = json.dumps(undefined_err.context, indent=4, sort_keys=True)
        click.echo(f"Context: {context_str}")
        sys.exit(1)


if __name__ == "__main__":
    main()
