from typing import Type

from fastapi import APIRouter, Depends, Form, HTTPException, Request, status

from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi_users import exceptions, models, schemas
from fastapi_users.manager import BaseUserManager, UserManagerDependency
from fastapi_users.router.common import ErrorCode, ErrorModel
from pydantic import EmailStr

from auth.schems import UserCreate

from starlette.status import HTTP_303_SEE_OTHER

router = APIRouter()


templates = Jinja2Templates(directory='templates')
router.mount('/static', StaticFiles(directory='static'), name='static')


@router.get('/login', name='login')
def home(request: Request,):
    return templates.TemplateResponse('login.html', {'request': request,})

@router.get('/register', name='register_get')
def home(request: Request,):
    return templates.TemplateResponse('register.html', {'request': request,})    



def get_register_router(
    get_user_manager: UserManagerDependency[models.UP, models.ID],
    user_schema: Type[schemas.U],
    user_create_schema: Type[schemas.UC],
) -> APIRouter:
    """Generate a router with the register route."""
    router = APIRouter()
    
    @router.post(
        "/register",
        response_model=user_schema,
        status_code=status.HTTP_201_CREATED,
        name="register",
        responses={
            status.HTTP_400_BAD_REQUEST: {
                "model": ErrorModel,
                "content": {
                    "application/json": {
                        "examples": {
                            ErrorCode.REGISTER_USER_ALREADY_EXISTS: {
                                "summary": "A user with this email already exists.",
                                "value": {
                                    "detail": ErrorCode.REGISTER_USER_ALREADY_EXISTS
                                },
                            },
                            ErrorCode.REGISTER_INVALID_PASSWORD: {
                                "summary": "Password validation failed.",
                                "value": {
                                    "detail": {
                                        "code": ErrorCode.REGISTER_INVALID_PASSWORD,
                                        "reason": "Password should be"
                                        "at least 3 characters",
                                    }
                                },
                            },
                        }
                    }
                },
            },
        },
    )
    async def register(
        request: Request,
        email: EmailStr = Form(...),
        password: str = Form(...),
        ful_mame: str = Form(...),
        faculty:str = Form(...),
        course:str = Form(...), 
        user_manager: BaseUserManager[models.UP, models.ID] = Depends(get_user_manager),
    ):
        
        user_create ={
            "email": email,
            "password": password,
            "is_active": True,
            "is_superuser": False,
            "is_verified": False,
            "ful_mame": ful_mame,
            'faculty': faculty,
            'course': course
        }

        user_create = UserCreate(**user_create)

        
        try:
            created_user = await user_manager.create(
                user_create, safe=True, request=request
            )
        except exceptions.UserAlreadyExists:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=ErrorCode.REGISTER_USER_ALREADY_EXISTS,
            )
        except exceptions.InvalidPasswordException as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={
                    "code": ErrorCode.REGISTER_INVALID_PASSWORD,
                    "reason": e.reason,
                },
            )

        url = 'http://127.0.0.1:8000/login'
        return RedirectResponse(url=url, status_code=HTTP_303_SEE_OTHER)    


        return schemas.model_validate(user_schema, created_user)

    return router
