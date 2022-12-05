import dataclasses
import enum
import re
from typing import Callable



@dataclasses.dataclass
class UserState:
    exercise_name: str
    command: str
    output: str
    cwd: str
    environ: dict[str, str]


class ExistState(str, enum.Enum):
    """
    PRESENT = 'PRESENT'
    ABSENT = 'ABSENT'
    """
    PRESENT = 'PRESENT'
    ABSENT = 'ABSENT'


@dataclasses.dataclass
class FileSystemCondition:
    path: str
    relative: bool = True
    directory: bool = False
    state: ExistState = ExistState.PRESENT
    content: str = None
    content_regex: re.Pattern = None


@dataclasses.dataclass
class EnvVarCondition:
    name: str
    value_regex: re.Pattern = None
    state: ExistState = ExistState.PRESENT


@dataclasses.dataclass
class Exercise:
    name: str = None
    complete: bool = False
    start_message: str = None
    win_message: str = 'Congrats! You did the exercise by typing {user_command}'
    hint_message: str = None
    command_regex: re.Pattern = None
    output_regex: re.Pattern = None
    cwd_regex: re.Pattern = None
    filesystem_conditions: list[FileSystemCondition] = None
    env_var_conditions: list[EnvVarCondition] = None
    eject_function: Callable[['Exercise', UserState], bool] = None

    def __str__(self):
        name = self.name
        return f'<Exercise {name=}>'

    def __repr__(self):
        return str(self)
