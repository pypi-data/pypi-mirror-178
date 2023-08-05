from typing import Union, List

from sqlalchemy.exc import NoResultFound

from kclii.database.database import session
from kclii.error.database import NotRecordFound
from .models import ProfileModel, EnvironmentVariablesModel, CurrentModel
from .core import ProfileCoreIn, EnvironmentVariables


class Repository:
    @staticmethod
    def set_profile(profile: ProfileModel) -> CurrentModel:
        try:
            current = session.query(CurrentModel).one()
            current.profile_id = profile.id
        except NoResultFound:
            current = CurrentModel(profile_id=profile.id)

        session.add(current)
        session.commit()
        return current

    @staticmethod
    def get_current_profile() -> CurrentModel:
        try:
            current = session.query(CurrentModel).one()
        except NoResultFound as error:
            raise NotRecordFound(filter_by={}) from error

        return current

    @staticmethod
    def get_all() -> List[ProfileModel]:
        return session.query(ProfileModel).all()

    @staticmethod
    def get_profile_by_name(name: str) -> Union[ProfileModel, NoResultFound]:
        try:
            saved_profile = (
                session.query(ProfileModel).filter(ProfileModel.name == name).one()
            )
        except NoResultFound as error:
            raise NotRecordFound(filter_by={"name": name}) from error

        return saved_profile

    @staticmethod
    def create_profile(profile: ProfileCoreIn) -> ProfileModel:
        new_profile = ProfileModel(name=profile.name)

        session.add(new_profile)
        session.commit()

        return new_profile

    @staticmethod
    def add_environment_variables(
        profile_id: int, environment_variables: List[EnvironmentVariables]
    ):
        environment_variables = [
            EnvironmentVariablesModel(
                key=environment_variable.key,
                value=environment_variable.value,
                profile_id=profile_id,
            )
            for environment_variable in environment_variables
        ]

        session.add_all(environment_variables)
        session.commit()

    @staticmethod
    def delete_environment_variables(
        environment_variables: List[str],
    ):
        session.query(EnvironmentVariablesModel).filter(
            EnvironmentVariablesModel.key.in_(environment_variables)
        ).delete()
        session.commit()

    @staticmethod
    def get_environment_variables_by_profile(
        profile_id: int,
    ) -> Union[List[EnvironmentVariablesModel], NoResultFound]:
        try:
            saved_environment_variables = (
                session.query(EnvironmentVariablesModel)
                .filter(EnvironmentVariablesModel.profile_id == profile_id)
                .all()
            )
        except NoResultFound as error:
            raise NotRecordFound(filter_by={"id": str(profile_id)}) from error

        return saved_environment_variables
