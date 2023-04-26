from . messages import MESSAGES
from . states import TestStates
from . app import dp
from aiogram import types


async def GetCurrentState(message: types.Message) -> str:
    state = dp.current_state(user=message.from_user.id)
    text = MESSAGES['current_state'].format(
        current_state=await state.get_state(),
        states=TestStates.all())
    return text