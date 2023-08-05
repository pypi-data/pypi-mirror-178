import os
import time
from typing import List, Tuple, Optional

import typer
from rich.console import Console
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn


from kclii.helper.message import new_message
from kclii.helper.data import request_value
from .core import EnvironmentVariables, ProfileCoreIn
from .repository import Repository


TITLE = "👤 Profile"

app = typer.Typer()
repository = Repository()
console = Console()


def request_profile_data(
    skip_name: Optional[bool] = False,
    skip_environment_variables: Optional[bool] = False,
) -> Tuple[str, List[EnvironmentVariables]]:
    if not skip_name:
        name = request_value(
            message="Profile name",
            description="Type the profile name should be unique",
            example="company",
        )
    else:
        name = ""

    if not skip_environment_variables:
        environment_variables = request_value(
            description="Add all the environments variables you need to this profile.",
            message="Environment Variables",
            example="MY_TOKEN=ThisIsMyAwesomeToken!",
            rules="Once you finish please type stop",
            multiple=True,
            key_value=True,
        )

        environment_variables = [
            EnvironmentVariables(key=list(env.keys())[0], value=list(env.values())[0])
            for env in environment_variables
        ]
    else:
        environment_variables = []

    return name, environment_variables


def print_list_environment_variables_by_profile(
    name: str, raw: Optional[bool] = False
) -> None:
    saved_profile = repository.get_profile_by_name(name=name)
    saved_environment_variables = repository.get_environment_variables_by_profile(
        profile_id=saved_profile.id
    )

    if raw:
        for saved_environment_variable in saved_environment_variables:
            print(
                f"{saved_environment_variable.key}={saved_environment_variable.value}"
            )
    else:
        table = Table("ID", "Name", "Value")
        for saved_environment_variable in saved_environment_variables:

            table.add_row(
                str(saved_environment_variable.id),
                saved_environment_variable.key,
                saved_environment_variable.value,
            )

        console.print(table)


def print_list_profiles() -> None:
    saved_profiles = repository.get_all()

    table = Table("ID", "Name", "CreatedAt")
    for saved_profile in saved_profiles:

        table.add_row(
            str(saved_profile.id),
            saved_profile.name,
            str(saved_profile.created_at),
        )

    console.print(table)


@app.command()
def new() -> None:
    new_message(
        title=TITLE,
        status="info",
        title_type="bold",
        message="Create a new profile",
    )
    name, environment_variables = request_profile_data()
    profile = ProfileCoreIn(name=name, environment_variables=environment_variables)
    saved_profile = repository.create_profile(profile=profile)
    repository.add_environment_variables(
        profile_id=saved_profile.id, environment_variables=profile.environment_variables
    )


@app.command()
def update(add: Optional[bool] = False, delete: Optional[bool] = False) -> None:
    name, _ = request_profile_data(skip_environment_variables=True)
    profile = repository.get_profile_by_name(name=name)

    if add:
        _, environment_variables = request_profile_data(skip_name=True)
        repository.add_environment_variables(
            profile_id=profile.id, environment_variables=environment_variables
        )

    if delete:
        environment_variables = request_value(
            description="Type environment variables to delete",
            message="Environment Variables",
            example="MY_TOKEN",
            rules="Once you finish please type stop",
            multiple=True,
        )
        repository.delete_environment_variables(
            environment_variables=environment_variables
        )


@app.command()
def ls() -> None:
    new_message(
        title=TITLE,
        status="info",
        title_type="bold",
        message="List all profiles",
    )

    print_list_profiles()


@app.command()
def ls_env(raw: Optional[bool] = False) -> None:
    if not raw:
        new_message(
            title=TITLE,
            status="info",
            title_type="bold",
            message="List all environment variables by pofile",
        )

    current_profile = repository.get_current_profile()
    print_list_environment_variables_by_profile(
        name=current_profile.profile.name, raw=raw
    )

@app.command()
def test() -> None:
    current_profile = repository.get_current_profile()
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
    ) as progress:
        for environment_variable in current_profile.profile.environment_variables:
            progress.add_task(description=environment_variable.key, total=None)

            if not os.getenv(environment_variable.key):
                raise NameError("Not all env variables are correct")
            time.sleep(0.3)

@app.command("set")
def _set(name: str) -> None:
    saved_profile = repository.get_profile_by_name(name=name)
    new_message(
        title=TITLE,
        status="success",
        title_type="bold",
        message=f"{saved_profile.name} ACTIVE",
    )

    repository.set_profile(saved_profile)


@app.command()
def current() -> None:
    print(repository.get_current_profile().profile.name)
