from aiogram import Bot
from aiogram.types import InputMediaPhoto, CallbackQuery, Message, InputMediaVideo
from aiogram.exceptions import TelegramBadRequest

from keyboards.global_kb import g_understand_kb

from dataclasses import dataclass
from db import DataBase


@dataclass
class UIContext:
    user_id: int
    chat_id: int
    username: str | None
    last_message_id: int | None
    bot: Bot
    db: DataBase

    @classmethod
    async def from_message(cls, message, database: DataBase):
        return cls(
            user_id=message.from_user.id,
            chat_id=message.chat.id,
            username=message.from_user.username,
            last_message_id=await database.get_last_ui_id(message.from_user.id),
            bot=message.bot,
            db=database
        )
        
    @classmethod
    async def from_callback(cls, callback, database):
        return cls(
            user_id=callback.from_user.id,
            chat_id=callback.message.chat.id,
            username=callback.from_user.username,
            last_message_id=await database.get_last_ui_id(callback.from_user.id),
            bot=callback.message.bot,
            db=database
        )
        
    async def update_message(self, text=None, photo=None, video=None, **kwargs):
        msg_id = await _update_message(self.bot, self.chat_id, self.last_message_id, text, photo, video, **kwargs)
        if msg_id:
            self.last_message_id = msg_id
        return msg_id

    async def update_specific(self, message_id, text=None, photo=None, video=None, **kwargs):
        return await _update_message(self.bot, self.chat_id, message_id, text, photo, video, **kwargs)
    
    async def delete(self, message_id):
        if not message_id:
            return
        
        try:
            await self.bot.delete_message(self.chat_id, message_id)
        except Exception:
            pass
    
    async def send_new(self, text=None, photo=None, **kwargs):
        if photo:
            msg = await self.bot.send_photo(
                chat_id=self.chat_id,
                photo=photo,
                caption=text,
                **kwargs
            )
        else:
            msg = await self.bot.send_message(
                chat_id=self.chat_id,
                text=text,
                **kwargs
            )
            
        if self.last_message_id:
            await self.delete(self.last_message_id)
            
        self.last_message_id = msg.message_id
        return msg.message_id


async def delete_message(bot, chat_id: int, message_id: int | None) -> None:
    try:
        if not message_id:
            return

        try:
            await bot.delete_message(chat_id, message_id)
        except Exception:
            pass
    except TelegramBadRequest:
        pass


async def _update_message(bot: Bot, chat_id, message_id, text=None, photo=None, video=None, **kwargs):
    try:
        if video:
            await bot.edit_message_media(
                chat_id=chat_id,
                message_id=message_id,
                media=InputMediaVideo(
                    media=video,
                    caption=text
                ),
                **kwargs
            )
        elif photo:
            await bot.edit_message_media(
                chat_id=chat_id,
                message_id=message_id,
                media=InputMediaPhoto(
                    media=photo,
                    caption=text
                ),
                **kwargs
            )
        else:
            await bot.edit_message_text(
                text=text,
                chat_id=chat_id,
                message_id=message_id,
                **kwargs
            )
            
        return message_id
    
    except TelegramBadRequest as e:
        if "message is not modified" in str(e):
            return
        
        if video:
            msg = await bot.send_video(
                chat_id=chat_id,
                video=video,
                caption=text,
                **kwargs
            )
        elif photo:
            msg = await bot.send_photo(
                chat_id=chat_id,
                photo=photo,
                caption=text,
                **kwargs
            )
        else:
            msg = await bot.send_message(
                chat_id=chat_id,
                text=text,
                **kwargs
            )
            
        await delete_message(bot, chat_id, message_id)
        
        return msg.message_id
    

async def update_last_message(database, user_id, msg_id):
    
    if msg_id:
        await database.set_last_ui_id(user_id, msg_id)
        
        
async def notify(bot: Bot, chat_id: int, text: str):
    await bot.send_message(chat_id, text, reply_markup=g_understand_kb)