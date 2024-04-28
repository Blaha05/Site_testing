from typing import Optional
from fastapi import Depends, FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import fastapi_users
from auth.cokie import auth_backend
from auth.models import User
from result.model import Result
from testing.models import Test
from auth.menger import get_user_manager
from auth.router import get_register_router
from auth.schems import UserCreate, UserRead
from databases import get_async_session
from auth.router import router as router_auth
from testing.router import router as router_testing
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from result.router import router as router_result
from custom_get_user import FastAPIUsers

app = FastAPI()


templates = Jinja2Templates(directory='templates')
app.mount('/static', StaticFiles(directory='static'), name='static')

                                  
fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)



app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)


app.include_router(
    get_register_router(get_user_manager, UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)

app.include_router(router_testing)

app.include_router(router_auth)

app.include_router(router_result)

current_user = fastapi_users.current_user()

@app.get('/', name='home')
async def home(request: Request, user: Optional[User] = Depends(current_user), session: AsyncSession = Depends(get_async_session)):
    
    my_test = []
    active_test = []
    result_test = []

    try:
        my_test = await session.execute(select(Test).filter(Test.uset_id == user.id))
        my_test = my_test.scalars().all()

        active_test = await session.execute(select(Test).filter(Test.faculty == user.faculty, Test.course == user.course))
        active_test = active_test.scalars().all()

        result_test = await session.execute(select(Result).filter(Result.user_id == user.id))
        result_test = result_test.scalars().all()

        return templates.TemplateResponse('new_main.html', {'request': request, 
                                                            'my_test':my_test, 
                                                            'active_test':active_test, 
                                                            'result_test':result_test
                                                            })
    except:
        return templates.TemplateResponse('new_main.html', {'request': request, 
                                                            'my_test':my_test, 
                                                            'active_test':active_test, 
                                                            'result_test':result_test
                                                            })

    


@app.exception_handler(401)
async def unauthorized(request, exc):
    return templates.TemplateResponse("error401.html", {"request": request})


@app.exception_handler(403)
async def unauthorized(request, exc):
    return templates.TemplateResponse("error403.html", {"request": request})

