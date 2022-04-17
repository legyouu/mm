import asyncio

from datetime import datetime
from sys import version_info
from time import time

from config import (
    ALIVE_IMG,
    ALIVE_NAME,
    BOT_NAME,
    ASSISTANT_NAME,
    BOT_USERNAME,
    GROUP_SUPPORT,
    OWNER_NAME,
    UPDATES_CHANNEL,
)
from program import __version__
from driver.veez import user
from driver.filters import command, other_filters
from driver.database.dbchat import add_served_chat, is_served_chat
from driver.database.dbpunish import is_gbanned_user
from pyrogram import Client, filters, __version__ as pyrover
from pyrogram.errors import FloodWait, MessageNotModified
from pytgcalls import (__version__ as pytover)
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message, ChatJoinRequest

__major__ = 0
__minor__ = 2
__micro__ = 1

__python_version__ = f"{version_info[0]}.{version_info[1]}.{version_info[2]}"


START_TIME = datetime.utcnow()
START_TIME_ISO = START_TIME.replace(microsecond=0).isoformat()
TIME_DURATION_UNITS = (
    ("week", 60 * 60 * 24 * 7),
    ("day", 60 * 60 * 24),
    ("hour", 60 * 60),
    ("min", 60),
    ("sec", 1),
)


async def _human_time_duration(seconds):
    if seconds == 0:
        return "inf"
    parts = []
    for unit, div in TIME_DURATION_UNITS:
        amount, seconds = divmod(int(seconds), div)
        if amount > 0:
            parts.append("{} {}{}".format(amount, unit, "" if amount == 1 else "s"))
    return ", ".join(parts)


@Client.on_message(
    command(["start", f"start@{BOT_USERNAME}"]) & filters.private & ~filters.edited
)
async def start_(client: Client, message: Message):
    await message.reply_text(
        f""" مرحبا {message.from_user.mention()} !**\n
💭 [{BOT_NAME}](https://t.me/{BOT_USERNAME})/n
        💭 انا بوت استطيع تشغيل الموسيقي والفديو في محادثتك الصوتية**\n
**💡 تعلم طريقة تشغيلي واوامر التحكم بي عن طريق  » 📚 الاوامر !**
**🔖 لتعلم طريقة تشغيلي بمجموعتك اضغط علي » ❓طريقة الاستخدام !**
**المبرمج [{ALIVE_NAME}](https://t.me/L120N)**""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "☑️اضغط لاضافتي لمجموعتك☑️",
                        url=f"https://t.me/{BOT_USERNAME}?startgroup=true",
                    )
                ],
                [InlineKeyboardButton("❓طريقه الاستخدام", callback_data="cbhowtouse")],
                [InlineKeyboardButton("الاوامر العربيه 👨", callback_data="cbbasic")],
                [
                    InlineKeyboardButton("الاوامر 📚", callback_data="cbcmds"),
                    InlineKeyboardButton("المساعد ❤️`", url=f"https://t.me/{ASSISTANT_NAME}"),
                ],
                [
                    InlineKeyboardButton(
                        "جروب الدعم 👥", url=f"https://t.me/{GROUP_SUPPORT}"
                    ),
                    InlineKeyboardButton(
                        "قناه البوت 📣", url=f"https://t.me/{UPDATES_CHANNEL}"
                    ),
                ],
                [
                    InlineKeyboardButton(
                        ALIVE_NAME, url=f"https://t.me/L120N"
                    )
                ],
            ]
        ),
        disable_web_page_preview=True,
    )


@Client.on_message(command(["لمطور","طور","مبير","لبرمج"]) & ~filters.edited)
async def help(client: Client, message: Message):
    await message.reply_photo(
        photo=f"https://t.me/L120N",
        caption=f"""◍ الزرار الاول: قناه السورس \n◍ الزرار الثاني: هو مبرمج السورس\n√""",
        reply_markup=InlineKeyboardMarkup(
         [
            [
                InlineKeyboardButton("قناه السورس 📣", url=f"https://t.me/{UPDATES_CHANNEL}"),
            ],
            [
                InlineKeyboardButton(
                        ALIVE_NAME, url=f"https://t.me/L120N"
                ),
            ],
            [
                InlineKeyboardButton("ضيف البوت لمجموعتك ✅", url=f"https://t.me/{BOT_USERNAME}?startgroup=true"),
            ]
         ]
     )
  )

@Client.on_message(
    command(["alive","لسورس","ورس", f"alive@{BOT_USERNAME}"]) & filters.group & ~filters.edited
)
async def alive(c: Client, message: Message):
    chat_id = message.chat.id
    current_time = datetime.utcnow()
    uptime_sec = (current_time - START_TIME).total_seconds()
    uptime = await _human_time_duration(int(uptime_sec))

    keyboard = InlineKeyboardMarkup(
        [
            [
                    InlineKeyboardButton(
                        ALIVE_NAME,
                        url=f"https://t.me/L120N",
                    )
                ],
                [
                    InlineKeyboardButton(
                        "جروب الدعم 🕊", url=f"https://t.me/{GROUP_SUPPORT}"
                    ),
                    InlineKeyboardButton(
                        "🕊 𝑬𝑳𝑴𝑼𝑺𝑳𝑰𝑴 🕊", url=f"https://t.me/{UPDATES_CHANNEL}"
                    ),
                ],
                [
                    InlineKeyboardButton(
                        "🎧اضافه البوت اللي مجموعتك🎧", url="https://t.me/{BOT_USERNAME}?startgroup=true"
                ),
            ]
        ]
    )

    alive = f"**اهلا {message.from_user.mention()}, انا{BOT_NAME}**\n\n👨🏼‍💻 المبرمــج: [{ALIVE_NAME}](https://t.me/L120N)\n👾 اصدار البوت: `v{__version__}`\n🔥 اصدار البايروجرام: `{pyrover}`\n🐍 اصدار البايثون: `{__python_version__}`\n✨ PyTgCalls Version: `{pytover.__version__}`\n🆙 وقت التشغيل: `{uptime}`\n\n❤ **شكرًا لإضافتي هنا ، لتشغيل الفيديو والموسيقى على دردشة الفيديو الخاصة بمجموعتك**"

    await c.send_photo(
        chat_id,
        photo=f"{ALIVE_IMG}",
        caption=alive,
        reply_markup=keyboard,
    )


@Client.on_message(command(["ping","يست", f"ping@{BOT_USERNAME}"]) & ~filters.edited)
async def ping_pong(client: Client, message: Message):
    start = time()
    m_reply = await message.reply_text("pinging...")
    delta_ping = time() - start
    await m_reply.edit_text("🏓 `PONG!!`\n" f"⚡️ `{delta_ping * 1000:.3f} ms`")


@Client.on_message(command(["uptime","لوقت", f"uptime@{BOT_USERNAME}"]) & ~filters.edited)
async def get_uptime(client: Client, message: Message):
    current_time = datetime.utcnow()
    uptime_sec = (current_time - START_TIME).total_seconds()
    uptime = await _human_time_duration(int(uptime_sec))
    await message.reply_text(
        "🤖 bot status:\n"
        f"• **uptime:** `{uptime}`\n"
        f"• **start time:** `{START_TIME_ISO}`"
    )


@Client.on_chat_join_request()
async def approve_join_chat(c: Client, m: ChatJoinRequest):
    if not m.from_user:
        return
    try:
        await c.approve_chat_join_request(m.chat.id, m.from_user.id)
    except FloodWait as e:
        await asyncio.sleep(e.x + 2)
        await c.approve_chat_join_request(m.chat.id, m.from_user.id)


@Client.on_message(filters.new_chat_members)
async def new_chat(c: Client, m: Message):
    chat_id = m.chat.id
    if await is_served_chat(chat_id):
        pass
    else:
        await add_served_chat(chat_id)
    ass_uname = (await user.get_me()).username
    bot_id = (await c.get_me()).id
    for member in m.new_chat_members:
        if member.id == bot_id:
            return await m.reply(
                "❤️ شكرا لاضافتي بالمجموعه **المجموعه** !\n\n"
                "قم بترقيتي الي مشرف لكي اعمل بشكل صحيح **المجموعه**, ولاتنسي كتابه انضم `/userbotjoin` لدعوة الحساب المساعد.\n\n"
                "وقم بكتابه تحديث لتحديث قايمه الادمنيه `/reload`",
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton("🕊 𝑬𝑳𝑴𝑼𝑺𝑳𝑰𝑴 🕊", url=f"https://t.me/{UPDATES_CHANNEL}"),
                            InlineKeyboardButton("جروب الدعم 🕊", url=f"https://t.me/{GROUP_SUPPORT}")
                        ],
                        [
                            InlineKeyboardButton("الاوامر العربيه 🕊", callback_data="cbbasic")],
                        [
                            InlineKeyboardButton("المساعد 🕊", url=f"https://t.me/{ass_uname}")
                        ]
                    ]
                )
            )


chat_watcher_group = 5

@Client.on_message(group=chat_watcher_group)
async def chat_watcher_func(_, message: Message):
    try:
        userid = message.from_user.id
    except Exception:
        return
    suspect = f"[{message.from_user.first_name}](tg://user?id={message.from_user.id})"
    if await is_gbanned_user(userid):
        try:
            await message.chat.ban_member(userid)
        except Exception:
            return
        await message.reply_text(
            f"👮🏼 (> {عفوا} <)\n\n**الحظر العام** حساب غير مرغوب فيه تم حظر هذا الحساب بواسطه المبرمج!\n\n🚫 **السبب:**يرسل رسايل غير مرغوب فيها للأناث"
        )
