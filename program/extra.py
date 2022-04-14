""" broadcast & statistic collector """


import asyncio
import traceback

from pyrogram.types import Message
from pyrogram import Client, filters, __version__ as pyrover

from pytgcalls import (__version__ as pytgver)
from program import __version__ as ver
from program.start import __python_version__ as pyver

from driver.filters import command
from driver.decorators import bot_creator, sudo_users_only
from driver.database.dbchat import get_served_chats
from driver.database.dbusers import get_served_users
from driver.database.dbpunish import get_gbans_count
from driver.database.dbqueue import get_active_chats

from config import BOT_USERNAME as uname


@Client.on_message(command(["broadcast","يع", f"broadcast@{uname}"]) & ~filters.edited)
@bot_creator
async def broadcast_message_nopin(c: Client, message: Message):
    if not message.reply_to_message:
        pass
    else:
        x = message.reply_to_message.message_id
        y = message.chat.id
        sent = 0
        chats = []
        schats = await get_served_chats()
        for chat in schats:
            chats.append(int(chat["chat_id"]))
        for i in chats:
            try:
                m = await c.forward_messages(i, y, x)
                await asyncio.sleep(0.3)
                sent += 1
            except Exception:
                pass
        await message.reply_text(f"✅ تم اكتمال الاذاعه في {sent} جروب.")
        return
    if len(message.command) < 2:
        await message.reply_text(
            "**usage**:\n\n/broadcast (`message`) or (`reply to message`)"
        )
        return
    text = message.text.split(None, 1)[1]
    sent = 0
    chats = []
    schats = await get_served_chats()
    for chat in schats:
        chats.append(int(chat["chat_id"]))
    for i in chats:
        try:
            m = await c.send_message(i, text=text)
            await asyncio.sleep(0.3)
            sent += 1
        except Exception:
            pass
    await message.reply_text(f"✅ تم اكتمال الاذاعه في {sent} جروب.")


@Client.on_message(command(["broadcast_pin","يع_بالتثبيت", f"broadcast_pin@{uname}"]) & ~filters.edited)
@bot_creator
async def broadcast_message_pin(c: Client, message: Message):
    if not message.reply_to_message:
        pass
    else:
        x = message.reply_to_message.message_id
        y = message.chat.id
        sent = 0
        pin = 0
        chats = []
        schats = await get_served_chats()
        for chat in schats:
            chats.append(int(chat["chat_id"]))
        for i in chats:
            try:
                m = await c.forward_messages(i, y, x)
                try:
                    await m.pin(disable_notification=True)
                    pin += 1
                except Exception:
                    pass
                await asyncio.sleep(0.3)
                sent += 1
            except Exception:
                pass
        await message.reply_text(
            f"✅ اكتملت الاذاعه في {sent} جروب.\n📌 ارسلت بالتثبيت الي {pin} جروب."
        )
        return
    if len(message.command) < 2:
        await message.reply_text(
            "**usage**:\n\n/broadcast_pin (`message`) or (`reply to message`)"
        )
        return
    text = message.text.split(None, 1)[1]
    sent = 0
    pin = 0
    chats = []
    schats = await get_served_chats()
    for chat in schats:
        chats.append(int(chat["chat_id"]))
    for i in chats:
        try:
            m = await c.send_message(i, text=text)
            try:
                await m.pin(disable_notification=True)
                pin += 1
            except Exception:
                pass
            await asyncio.sleep(0.3)
            sent += 1
        except Exception:
            pass
    await message.reply_text(
        f"✅ اكتملت الاذاعه في {sent} جروب.\n📌 ارسلت بالتثبيت الي {pin} جروب."
    )


@Client.on_message(command(["stats","لاحصائيات", f"stats@{uname}"]) & ~filters.edited)
@sudo_users_only
async def bot_statistic(c: Client, message: Message):
    name = (await c.get_me()).first_name
    chat_id = message.chat.id
    user_id = message.from_user.id
    msg = await c.send_message(
        chat_id, "❖ Collecting Stats..."
    )
    served_chats = len(await get_served_chats())
    served_users = len(await get_served_users())
    gbans_usertl = await get_gbans_count()
    tgm = f"""
📊 الاحصائيات الحاليه للبوت [{name}](https://t.me/{uname})`:`

➥ **المجموعات** : `{served_chats}`
➥ **المشتركين** : `{served_users}`
➥ **المحظورين عام** : `{gbans_usertl}`

➛ **اصدار البايثون** : `{pyver}`
➛ **اصدار البيتاجكول** : `{pytgver.__version__}`
➛ **اصدار البايروجرام** : `{pyrover}`

🤖 اصدار البوت: `{ver}`"""
    
    await msg.edit(tgm, disable_web_page_preview=True)


@Client.on_message(command(["calls","لنشطه", f"calls@{uname}"]) & ~filters.edited)
@sudo_users_only
async def active_calls(c: Client, message: Message):
    served_chats = []
    try:
        chats = await get_active_chats()
        for chat in chats:
            served_chats.append(int(chat["chat_id"]))
    except Exception as e:
        traceback.print_exc()
        await message.reply_text(f"🚫 error: `{e}`")
    text = ""
    j = 0
    for x in served_chats:
        try:
            title = (await c.get_chat(x)).title
        except Exception:
            title = "Private Group"
        if (await c.get_chat(x)).username:
            user = (await c.get_chat(x)).username
            text += (
                f"**{j + 1}.** [{title}](https://t.me/{user}) [`{x}`]\n"
            )
        else:
            text += f"**{j + 1}.** {title} [`{x}`]\n"
        j += 1
    if not text:
        await message.reply_text("❌ لا يوجد جروبات نشطه")
    else:
        await message.reply_text(
            f"✏️ **قايمه الجروبات النشطه:**\n\n{text}\n\n❖ هذه هي الجروبات النشطه حاليا في بيانات البوت",
            disable_web_page_preview=True,
        )
