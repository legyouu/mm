# Copyright (C) 2021 By VeezMusicProject
from driver.decorators import check_blacklist
from driver.queues import QUEUE
from driver.database.dbpunish import is_gbanned_user
from pyrogram import Client, filters

from pyrogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from config import (
    ASSISTANT_NAME,
    ALIVE_NAME,
    BOT_NAME,
    BOT_USERNAME,
    GROUP_SUPPORT,
    OWNER_NAME,
    UPDATES_CHANNEL,
)


@Client.on_callback_query(filters.regex("cbstart"))
async def cbstart(_, query: CallbackQuery):
    await query.answer("تم العوده لبدايه✅")
    await query.edit_message_text(
        f"""**مرحبا انا {message.from_user.mention()} !**\n
💭 [{BOT_NAME}](https://t.me/{BOT_USERNAME})
        💭 انا بوت استطيع تشغيل الموسيقي والفديو في محادثتك الصوتية**\n
**💡 تعلم طريقة تشغيلي واوامر التحكم بي عن طريق  » 📚 الاوامر !**
**🔖 لتعلم طريقة تشغيلي بمجموعتك اضغط علي » ❓طريقة الاستخدام !**
**المبرمج [{ALIVE_NAME}](https://t.me/L120N)**
""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "ضيف البوت لمجموعتك ✅",
                        url=f"https://t.me/{BOT_USERNAME}?startgroup=true",
                    )
                ],
                [InlineKeyboardButton("طريقه الاستخدام ❓", callback_data="cbhowtouse")],
                [InlineKeyboardButton("الاوامر العربيه 👨‍💻", callback_data="cbbasic")],
                [
                    InlineKeyboardButton("الاوامر 📚", callback_data="cbcmds"),
                    InlineKeyboardButton("المساعد ❤️", url=f"https://t.me/{ASSISTANT_NAME}"),
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


@Client.on_callback_query(filters.regex("cbhowtouse"))
async def cbguides(_, query: CallbackQuery):
    await query.answer("قسم طريقه استخدام البوت✅")
    await query.edit_message_text(
        f""" الدليل الأساسي لاستخدام هذا البوت:

 1 ↤ أولاً ، أضفني إلى مجموعتك
 2 ↤ بعد ذلك ، قم بترقيتي كمشرف ومنح جميع الصلاحيات باستثناء الوضع الخفي
 3 ↤ بعد ترقيتي ، اكتب «تحديث» او /reload مجموعة لتحديث بيانات المشرفين
 3 ↤ أضف  @{ASSISTANT_NAME} إلى مجموعتك أو اكتب او «انضم»  /userbotjoin لدعوة حساب المساعد
 4 ↤ قم بتشغيل المكالمة  أولاً قبل البدء في تشغيل الفيديو / الموسيقى
 5 ↤ في بعض الأحيان ، يمكن أن تساعدك إعادة تحميل البوت باستخدام الأمر «تحديث» او /reload في إصلاح بعض المشكلات
 📌 إذا لم ينضم البوت إلى المكالمة ، فتأكد من تشغيل المكالمة  بالفعل ، أو اكتب «غادر» /userbotleave ثم اكتب «انضم» او /userbotjoin مرة أخرى

 💡 إذا كانت لديك أسئلة  حول هذا البوت ، فيمكنك إخبارنا منن خلال قروب الدعم الخاصة بي هنا ↤ @{GROUP_SUPPORT}

🕊قناة البوت @{UPDATES_CHANNEL}
__""",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("🔙رجوع", callback_data="cbstart")]]
        ),
    )


@Client.on_callback_query(filters.regex("cbcmds"))
async def cbcmds(_, query: CallbackQuery):
    await query.answer("قايمه الاوامر✅")
    await query.edit_message_text(
        f"""✨ **Hello [{query.message.chat.first_name}](tg://user?id={query.message.chat.id}) !**

» **⇦قم بالضغط علي الزر الذي تريده لمعرفه الاوامر لكل فئه منهم !**

🕊 __قناة البوت»  @{UPDATES_CHANNEL}  __""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("اوامر المشرف🙋🏼‍♂️", callback_data="cbadmin"),
                    InlineKeyboardButton("👨🏼‍💻اوامر المطور 👨🏼‍💻", callback_data="cbsudo"),
                ],[
                    InlineKeyboardButton("الاوامر العربيه 👨‍💻", callback_data="cbbasic")                    
                ],[
                    InlineKeyboardButton("🔙 رجوع", callback_data="cbstart")
                ],
            ]
        ),
    )


@Client.on_callback_query(filters.regex("cbbasic"))
async def cbbasic(_, query: CallbackQuery):
    await query.answer("قايمه الاوامر المعربه الكامله✅")
    await query.edit_message_text(
        f"""🕊 ها هي الاوامر المعربه الكامله :
الاوامر المعربه تكتب كما هي بدون شرط او اي شيء
◤━───━𝑬𝑳𝑴𝑼𝑺𝑳𝑰𝑴━───━◥
اوامر تشغيل البوت في المجموعه 🕊
🕊 تشغيل 『اسم الأغنية او / رابط』تشغيل الصوت mp3
🕊 فديو 『اسم الفديو او / رابط الفيديو』 تشغيل الفيديو داخل المكالمة
🕊 ايقاف او انهاء 『لايقاف التشغيل』
🕊 وقف 『ايقاف التشغيل مؤقتا 』 
🕊 تقدم 『تخطي الئ التالي』
🕊 مواصله 『استئناف التشغيل』
🕊 كتم او سكوت 『لكتموالبوت』
🕊 الغاء كتم 『لرفع كتم البوت』
◤━───━𝑬𝑳𝑴𝑼𝑺𝑳𝑰𝑴━───━◥
اوامر التحكم بالبوت خارج و داخل المجموعه 🕊
🕊 تحكم 『تظهر لك قائمه التشغيل』
🕊 تنزيل 『 اسم الفيديو للتحميل من اليوتيوب』
🕊 تحميل 『 اسم الاغنيه للتحميل من اليوتيوب』
🕊 بحث 『 للبحث عن اي شئ』
🕊 الصوت 『كتابه رقم ضبط الصوت』
🕊 تحديث 『لتحديث البوت و قائمه المشرفين』
🕊 انضم 『لدخول الحساب المساعد』
🕊 غادر 『لخروج الحساب المساعد』
🕊 تيست 『لاظهار حاله البوت』
🕊 الوقت 『لاظهار الوقت』
🕊 السورس 『اظهار معلومات البوت في المجموعه』
◤━───━𝑬𝑳𝑴𝑼𝑺𝑳𝑰𝑴━───━◥
اوامر المطور 🕊
🕊 مسح 『لمسح ملفات المستخدمه』
🕊 تنظيف 『لتنظيف الملفات المحمله』
🕊 معلومات 『لرويه معلومات النظام』
🕊 ترقيه 『لترقيه البوت لاخر اصدار من السورس』
🕊 تنصيب 『لاعاده التشغيل』
🕊 غادر الجميع 『للمغادره من المجموعات』
◤━───━𝑬𝑳𝑴𝑼𝑺𝑳𝑰𝑴━───━◥
قناة البوت @{UPDATES_CHANNEL}
__""",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("🔙رجوع", callback_data="cbcmds")]]
        ),
    )


@Client.on_callback_query(filters.regex("cbadmin"))
async def cbadmin(_, query: CallbackQuery):
    await query.answer("قايمه الادمنيه✅")
    await query.edit_message_text(
        f"""  »
 » /playlist  او «تحكم» ↤ تظهر لك قائمة التشغيل
 » /videoاو «تنزيل» + الاسم  تنزيل فيديو من youtube
 » /song +  او« تحميل» الاسم تنزيل صوت من youtube
» /volume  او «الصوت»+ الرقم لضبط مستوئ الصوت
» /reload  او «تحديث» لتحديث البوت و قائمة المشرفين
» /userbotjoin  او «انضم» لاستدعاء حساب المساعد
» /userbotleave  او «غادر» لطرد حساب المساعد 
 » /pingاو«تيست» - إظهار حالة البوت بينغ
 » /alive   او «السورس» إظهار معلومات البوت  (في المجموعه) 
 🕊قناة البوت @{UPDATES_CHANNEL}
__""",

        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("🔙رجوع", callback_data="cbcmds")]]
        ),
    )

@Client.on_callback_query(filters.regex("cbsudo"))
async def cbsudo(_, query: CallbackQuery):
    await query.answer("قايمه المطور✅")
    await query.edit_message_text(
        f"""🕊 here is the قايمه المطور✅:

» /gban (`username` or `user id`) - for global banned people
» /ungban (`username` or `user id`) - for un-global banned people
» /speedtest - run the bot server speedtest
» /sysinfo - show the system information
» /update - update your bot to latest version
» /restart - restart your bot
» /leaveall - order userbot to leave from all group
» /leavebot (`chat id`) - order bot to leave from the group you specify

» /eval - execute any code
» /sh - run any command

» /broadcast (`message`) - send a broadcast message to all groups entered by bot
» /broadcast_pin (`message`) - send a broadcast message to all groups entered by bot with the chat pin

🕊قناة البوت @{UPDATES_CHANNEL}
""",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("🔙رجوع", callback_data="cbcmds")]]
        ),
    )


@Client.on_callback_query(filters.regex("cbmenu"))
async def cbmenu(_, query: CallbackQuery):
    if query.message.sender_chat:
        return await query.answer("you're an Anonymous Admin !\n\n» revert back to user account from admin rights.")
    a = await _.get_chat_member(query.message.chat.id, query.from_user.id)
    if not a.can_manage_voice_chats:
        return await query.answer("💡 المسؤول الوحيد الذي لديه إذن إدارة الدردشات الصوتية يمكنه النقر على هذا الزر !", show_alert=True)
    chat_id = query.message.chat.id
    if chat_id in QUEUE:
          await query.edit_message_text(
              f"⚙️ **الإعدادات** {query.message.chat.title}\n\n⏸ : ايقاف التشغيل موقتآ\n▶️ : استئناف التشغيل\n🔇 : كتم الصوت\n🔊 : الغاء كتم الصوت\n⏹ : ايقاف التشغيل",
              reply_markup=InlineKeyboardMarkup(
                  [[
                      InlineKeyboardButton("⏹", callback_data="cbstop"),
                      InlineKeyboardButton("⏸", callback_data="cbpause"),
                      InlineKeyboardButton("▶️", callback_data="cbresume"),
                  ],[
                      InlineKeyboardButton("🔇", callback_data="cbmute"),
                      InlineKeyboardButton("🔊", callback_data="cbunmute"),
                  ],[
                      InlineKeyboardButton("🗑 اغلاق", callback_data="cls")],
                  ]
             ),
         )
    else:
        await query.answer("❌ قائمة التشغيل فارغه", show_alert=True)


@Client.on_callback_query(filters.regex("cls"))
async def close(_, query: CallbackQuery):
    a = await _.get_chat_member(query.message.chat.id, query.from_user.id)
    if not a.can_manage_voice_chats:
        return await query.answer("💡 المسؤول الوحيد الذي لديه إذن إدارة الدردشات الصوتية يمكنه النقر على هذا الزر !", show_alert=True)
    await query.message.delete()
