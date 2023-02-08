from typing import Iterator

from aiolinebot.api_base import AioLineBotApi
from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from starlette.background import BackgroundTasks

from config.settings.base import settings
from driver.rdb import SessionLocal
from infrastructure.mysql.line_user.lien_user_repository import LineUserRepository, LineUserRepositoryImpl, \
    LineUserCommandUseCaseUnitOfWorkImpl

from linebot import WebhookParser
from linebot.models import TextMessage

from infrastructure.mysql.student_task.student_task_repository import StudentTaskRepository, StudentTaskRepositoryImpl, \
    StudentTaskCommandUseCaseUnitOfWorkImpl
from usecase.line_user.line_user_usecase import LineUserCommandUseCase, LineUserCommandUseCaseUnitOfWork, \
    LineUserCommandUseCaseImpl
from usecase.student_task.student_task_usecase import StudentTaskCommandUseCase, StudentTaskCommandUseCaseUnitOfWork, \
    StudentTaskCommandUseCaseImpl

router = APIRouter(
    prefix='/line_user',
    tags=['line_user'],
)


def get_session() -> Iterator[Session]:
    session: Session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


def user_command_usecase(session: Session = Depends(get_session)) -> LineUserCommandUseCase:
    user_repository: LineUserRepository = LineUserRepositoryImpl(session)
    uow: LineUserCommandUseCaseUnitOfWork = LineUserCommandUseCaseUnitOfWorkImpl(
        session,
        user_repository,
    )
    return LineUserCommandUseCaseImpl(uow)


def task_command_usecase(session: Session = Depends(get_session)) -> StudentTaskCommandUseCase:
    task_repository: StudentTaskRepository = StudentTaskRepositoryImpl(session)
    uow: StudentTaskCommandUseCaseUnitOfWork = StudentTaskCommandUseCaseUnitOfWorkImpl(
        session,
        task_repository,
    )
    return StudentTaskCommandUseCaseImpl(uow)


line_api = AioLineBotApi(channel_access_token=settings.LINE_CHANNEL_ACCESS_TOKEN)
parser = WebhookParser(channel_secret=settings.LINEBOT_CHANNEL_SECRET)


@router.post("/callback")
async def callback(
        request: Request,
        background_tasks: BackgroundTasks,
        user_command_usecase=Depends(user_command_usecase),
        task_command_usecase=Depends(task_command_usecase),
):
    events = parser.parse(
        (await request.body()).decode("utf-8"),
        request.headers.get("X-Line-Signature", "")
    )

    try:
        user_id = str(events[0].source.user_id)
        task = str(events[0].message.text)
        a = task_command_usecase.create_task(user_id, task)
        background_tasks.add_task(handle_events, events=events)
        return "OK"

    # # 新規ユーザー登録
    except:
        user_id = events[0].source.user_id
        profile = line_api.get_profile(user_id).display_name
        user = user_command_usecase.create_task(user_id, profile)
        background_tasks.add_task(handle_events, events=events)
        return "OK"


async def handle_events(events):
    for event in events:
        try:
            await line_api.reply_message(
                event.reply_token,
                TextMessage(text="登録完了しました。")
            )
        except Exception as e:
            print(e)
