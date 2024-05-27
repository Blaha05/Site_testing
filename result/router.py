from fastapi import APIRouter, Depends, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy import select
from auth.cokie import auth_backend
from auth.models import User
import fastapi_users
from auth.menger import get_user_manager
from databases import get_async_session
from sqlalchemy.ext.asyncio import AsyncSession
from result.model import Result
from starlette.status import HTTP_303_SEE_OTHER
import g4f

from testing.models import Test

router = APIRouter()

templates = Jinja2Templates(directory='templates')


fastapi_users = fastapi_users.FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)


current_user = fastapi_users.current_user()


@router.get('/result/{test_id}', name='get_result')
async def get_result(request: Request):
    data = await request.json() 
    return templates.TemplateResponse('result.html', data)
    
    


@router.post('/result/{test_id}')
async def calculation_point(request: Request, test_id:int, user = Depends(current_user), session: AsyncSession = Depends(get_async_session)):
    data = await request.json()

    choose_answer = data['selectedAnswers']
    point_choose = 0
    for i in choose_answer:
        if i == 'on':
            point_choose += 1
    
    all_answer = data['status']
    point_all = 0
    for i in all_answer:
        if i == 'on':
            point_all += 1
    
    test = await session.execute(select(Test).filter(Test.id == test_id))
    test_title = test.scalars().all()[0].title

    q = Result(user_id = user.id, test_id = int(test_id), point = point_choose, count_point=point_all, title=test_title)
    
    session.add(q)
    await session.commit()

    percentage_correct = (point_choose / point_all) * 100  
    
    return templates.TemplateResponse('result.html', {
        'request': request, 
        'all': point_choose, 
        'correct': point_all,  
        'percentage_correct': percentage_correct  
    })
    


@router.get('/get_user')
async def get_data_for_main_page(session: AsyncSession = Depends(get_async_session),user = Depends(current_user)):
    return 'hello'
    

@router.post('/generade_test')
async def generade_test(title:str):
    response = g4f.ChatCompletion.create(
        model='gpt-3.5-turbo',
        messages=[{"role": "user", "content": f"Твоє завдання згенерувати тест з відповідями a, b, c, d на тему {title}"}],
        stream=True,
    )

    for message in response:
        print(message, flush=True, end='')