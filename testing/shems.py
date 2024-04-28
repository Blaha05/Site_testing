from typing import Optional
from fastapi.param_functions import Form
from pydantic import BaseModel
from typing_extensions import Annotated, Doc  # type: ignore [attr-defined]

from typing import List

class Question(BaseModel):
    question: str
    answer1_checkbox: Optional[str] = 'off'
    answer1: str
    answer2_checkbox: Optional[str] = 'off'
    answer2: str
    answer3_checkbox: Optional[str] = 'off'
    answer3: str
    answer4_checkbox: Optional[str] = 'off'
    answer4: str


class CreateTest(BaseModel):
    title: str
    description: str
    faculty: str
    course: str


class TestAnswers(BaseModel):
    answers: List[str]



class TestAnswers2:
    def __init__(
            self,
            *,
            answers: Annotated[
                list[str],
                Form(),
            ]
                 ):    
        self.answers = answers



class GetForm:
    def __init__(
            self,
            *,
            username: Annotated[
                str,
                Form(),
            ],
            password: Annotated[
                str,
                Form(),
            ],
            answer4_checkbox:Annotated[
                str,
                Form(),
            ] = 'None',
                 ):    
        self.username = username
        self.password = password
        self.answer4_checkbox = answer4_checkbox


class Question2():
    def __init__(
            self,
            *,
            question:Annotated[
                str,
                Form(),
            ],
            answer1_checkbox:Annotated[
                str,
                Form(),
            ] = 'off',
            answer1:Annotated[
                str,
                Form(),
            ],
            answer2_checkbox:Annotated[
                str,
                Form(),
            ] = 'off',
            answer2:Annotated[
                str,
                Form(),
            ],
            answer3_checkbox:Annotated[
                str,
                Form(),
            ] = 'off',
            answer3:Annotated[
                str,
                Form(),
            ],
            answer4_checkbox:Annotated[
                str,
                Form(),
            ] = 'off',
            answer4:Annotated[
                str,
                Form(),
            ],
                 ) :
        self.question = question
        self.answer1_checkbox = answer1_checkbox
        self.answer1 = answer1
        self.answer2_checkbox = answer2_checkbox
        self.answer2 = answer2
        self.answer3_checkbox = answer3_checkbox
        self.answer3 = answer3
        self.answer4_checkbox = answer4_checkbox
        self.answer4 = answer4
