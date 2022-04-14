import asyncio
from config import BOT_USERNAME, SUDO_USERS
from driver.decorators import authorized_users_only, sudo_users_only, errors
from driver.filters import command, other_filters
from driver.veez import user as USER
from pyrogram import Client, filters
from pyrogram.errors import UserAlreadyParticipant


@Client.on_message(
    command(["userbotjoin","نضم","انضم", f"userbotjoin@{BOT_USERNAME}"]) & ~filters.private & ~filters.bot
)
@authorized_users_only
@errors
async def join_group(client, message):
    chid = message.chat.id
    try:
        invitelink = await client.export_chat_invite_link(chid)
    except BaseException:
        await message.reply_text(
            "• **ليس لدي صلاحيات:**\n\n» ❌ __اضافة المستخدمين__",
        )
        return

    try:
        user = await USER.get_me()
    except BaseException:
        user.first_name = "L120N"

    try:
        await USER.join_chat(invitelink)
    except UserAlreadyParticipant:
        pass
    except Exception as e:
        print(e)
        await message.reply_text(
            f"🛑 خطأ تاكد من عدم حظر الحساب المساعد في الجروب🛑 \n\n**لم يتمكن حساب المساعد من الانضمام إلى مجموعتك بسبب كثرة طلبات الانضمام **"
            "\n\n**قم بتوجيه الرساله الي مالك البوت @lell_x أو أضف مساعدًا @L120N  يدويًا إلى مجموعتك وحاول مرة أخرى**",
        )
        return
    await message.reply_text(
           f"✅ ** دخل حساب المساعد للمجموعه او القناة بنجاح**",
    )


@Client.on_message(command(["userbotleave","ادر","غادر",
                            f"leave@{BOT_USERNAME}"]) & filters.group & ~filters.edited)
@authorized_users_only
async def leave_one(client, message):
    try:
        await USER.send_message(message.chat.id, "✅ قام الحساب المساعد بمغادرة المجموعه بنجاح")
        await USER.leave_chat(message.chat.id)
    except BaseException:
        await message.reply_text(
            "❌ **لايستطيع الحساب المساعد مغادره الجروب ربما يكون بسبب الضغط.**\n\n**» حاول لاحقا او قم بطرده يدويا من جروبك**"
        )

        return


@Client.on_message(command(["leaveall","ادرالجميع","غادرالجميع", f"leaveall@{BOT_USERNAME}"]))
@sudo_users_only
async def leave_all(client, message):
    if message.from_user.id not in SUDO_USERS:
        return

    left = 0
    failed = 0
    lol = await message.reply("🔄 **البوت** الحساب المساعد يغادر كل الجروبات !")
    async for dialog in USER.iter_dialogs():
        try:
            await USER.leave_chat(dialog.chat.id)
            left += 1
            await lol.edit(
                f"🚫الحساب المساعد يغادر كل الجروبات...\n\n🥺غادر: {left} جروب.\n❌فشل: {failed} جروب."
            )
        except BaseException:
            failed += 1
            await lol.edit(
                f"🚫الحساب المساعد غادر...\n\n🥺غادر: {left} جروب.\n❌فشل: {failed} جروب."
            )
        await asyncio.sleep(0.7)
    await client.send_message(
        message.chat.id, f"✅ 👨🏼‍💻غادر من: {left} جروب.\n❌ 🚨فشل في مغادره: {failed} جروب."
    )
