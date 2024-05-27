from typing import Any, Dict, List
from fastapi import APIRouter, Body, Depends, Form, HTTPException, Request
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
import fastapi_users
from sqlalchemy import select, delete
from auth.menger import get_user_manager
from auth.models import User
from testing.models import Test, Question, Answers
from databases import get_async_session
from sqlalchemy.ext.asyncio import AsyncSession
from auth.cokie import auth_backend
from starlette.status import HTTP_303_SEE_OTHER
from testing.shems import Question2
from result.model import Result

templates = Jinja2Templates(directory='templates')


router = APIRouter(
    prefix='/create_test',
    tags=['operations']
    )


fastapi_users = fastapi_users.FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)


current_user = fastapi_users.current_user()



@router.get('/', name='create')
def home(request: Request, user = Depends(current_user)):
    print(user.is_superuser)
    if user.is_superuser == False:
        raise HTTPException(status_code=403, detail="Forbidden")
    return templates.TemplateResponse('create_test.html', {'request': request,})



@router.post('/', name='create_test')
async def create_test(title: str = Form(...),
                description: str = Form(...),
                faculty: str = Form(...),
                course: str = Form(...),
                user: User = Depends(current_user),
                session: AsyncSession = Depends(get_async_session)
            ):
    q = Test(title=title, description=description, uset_id=user.id, faculty=faculty, course=course)
    await session.flush()  # Запис не вставляється в базу даних, але id генерується
    session.add(q)
    await session.commit()
    
    test_id = q.id

    url = router.url_path_for('add_question', test_id=test_id)
    return RedirectResponse(url=url, status_code=HTTP_303_SEE_OTHER)






@router.get("/{test_id}", response_class=JSONResponse, name='add_question')
async def get_test(request: Request, test_id: int, session: AsyncSession = Depends(get_async_session)):
    
    questions = await session.execute(select(Question).filter(Question.test_id == test_id))
    questions = questions.scalars().all()
    questions.reverse()

    results = await session.execute(select(Result).filter(Result.test_id == test_id))
    results = results.scalars().all()

    questions_with_answers = []
    for question in questions:
        answers = await session.execute(select(Answers).filter(Answers.question_id == question.id))
        answers = answers.scalars().all()
        questions_with_answers.append({"question": question.text, "answers": [answer.text for answer in answers]})

    return templates.TemplateResponse('add_qutions.html', {'request': request, 
                                                           'test_id': test_id, 
                                                           "questions_with_answers": questions_with_answers,
                                                           "results": results
                                                           })
    



@router.post('/{test_id}', name='add_3')
async def get_form_data(test_id, data:Question2 = Depends(), session: AsyncSession = Depends(get_async_session)):
    
    q = Question(text = data.question,test_id = int(test_id))
    session.add(q)
    await session.flush()
    
    id_question = q.id

    q1 = Answers(question_id=id_question, text=data.answer1, status=data.answer1_checkbox)
    q2 = Answers(question_id=id_question, text=data.answer2, status=data.answer2_checkbox)
    q3 = Answers(question_id=id_question, text=data.answer3, status=data.answer3_checkbox)
    q4 = Answers(question_id=id_question, text=data.answer4, status=data.answer4_checkbox)

    session.add_all([q1,q2,q3,q4])
    await session.commit()

    url = router.url_path_for('add_question', test_id=test_id)
    return RedirectResponse(url=url, status_code=HTTP_303_SEE_OTHER)    


@router.get("/testing/{test_id}", response_class=JSONResponse, name='testing_get')
async def get_test(request: Request, test_id: int, session: AsyncSession = Depends(get_async_session)):
    
    questions = await session.execute(select(Question).filter(Question.test_id == test_id))
    questions = questions.scalars().all()

    questions_with_answers = []
    status_answer = []
    for question in questions:
        answers = await session.execute(select(Answers).filter(Answers.question_id == question.id))
        answers = answers.scalars().all()
        status_answer.append({answer.text:answer.status for answer in answers})
        questions_with_answers.append({"question": question.text, "answers": [answer.text for answer in answers]})

    return templates.TemplateResponse('view_test.html', {'request': request, 
                                                        'test_id': test_id, 
                                                        "questions_with_answers": questions_with_answers,
                                                        'status_answer': status_answer
                                                        })


@router.get("/delete_test/{test_id}", name='delate_test')
async def delete_test(test_id, session: AsyncSession = Depends(get_async_session)):
    q = await session.execute(delete(Test).filter(Test.id == int(test_id)))
    await session.commit()

    url = 'http://127.0.0.1:8000/'
    return RedirectResponse(url=url, status_code=HTTP_303_SEE_OTHER)

   
@router.get("/deletequestion/{test}/{test_id}", name='delate_question')
async def delete_question(request: Request, test, test_id:str, session: AsyncSession = Depends(get_async_session)):
    q = await session.execute(delete(Question).filter(Question.text == test_id))
    await session.commit()

    url = router.url_path_for('add_question', test_id=int(test))
    return RedirectResponse(url=url, status_code=HTTP_303_SEE_OTHER)

