from config import API_ID, API_HSH, admin, heart, members, adminusername
from telethon import TelegramClient, events, Button
from telethon.tl.custom import Message
import random
import datetime
import json
import os

Amir = TelegramClient(
                      "MetaBot",
                      api_id=API_ID,
                      api_hash=API_HSH
                    #   flood_sleep_threshold = 20
)

#پیام استارت
@Amir.on(events.NewMessage(pattern="/start"))
async def start_message(event: Message):
     userid = event.sender_id
     usermessages = event.message.message
     save_user_ids(userid)
     ghalb = random.choice(heart)
     time = datetime.datetime.now()
     if userid == admin and event.is_private:
        await Amir.send_message(entity=admin, message=f"**سلام مدیر عزیز به ربات خوش آمدید** {ghalb}\n **لیست دسترسی های شما:**", buttons=[
            Button.text(text="آمارربات",) , Button.text(text="پیام به کاربران"),
            Button.text(text="مسدود کردن", resize=True)
        ])
     elif event.is_private:
        await event.respond(f"**سلام به پیام رسان ما خوش آمدید {ghalb}**\n آیدی مدیر ربات : {adminusername}")
        await Amir.send_message(entity=admin, message=f"**این کاربر در ساعت {time.strftime("%H:%M:%S")} با آیدی عددی :** `{userid}` ربات را استارت کرد")
        await event.reply("**پیام خودرا ارسال کنید:**")

@Amir.on(events.NewMessage())
async def fwd_messages(event: Message):
    userid = event.sender_id
    usermessages = event.message.message
    if usermessages == "/start":
        pass
    elif userid == admin:
        pass
    elif event.is_private:
        await Amir.send_message(entity=admin, message=f"**پیام از طرف کاربر :** `{userid}`\n **متن پیام:** **{usermessages}\n ادمین محترم میتوانید با دستور /msg جواب کاربر را بدهید.**")
        await event.reply("**پیام شما به ادمین ارسال شد**")

@Amir.on(events.NewMessage(pattern="/msg", chats=admin))
async def send_msg(event: Message):
    #منتظر بودن پیام کاربر
    if event.text == "/msg":
        async with Amir.conversation(admin) as conv:
            try:
                await conv.send_message("**آیدی عددی کاربر را وارد کنید**")
                response = await conv.get_response()
                payam = int(response.text)
                await conv.send_message("**متن پیام خودرا وارد کنید**")
                response2 = await conv.get_response()
                await Amir.send_message(payam, f"**یک پیام از طرف مدیریت دارید:\n {response2.text}**")
                await event.respond("**پیام شما به کاربر ارسال شد**")
            except ValueError:
                await conv.send_message("**آیدی عددی اشتباه است مجدد از دستور /msg استفاده کنید و پیام ارسال کنید**")

@Amir.on(events.NewMessage(pattern="مسدود کردن", chats=admin))
async def ban_message(event: Message):
    if event.text == "مسدود کردن":
        async with Amir.conversation(admin) as cnv:
            await cnv.send_message("**آیدی عددی کاربر را وارد کنید:**")
            banid = await cnv.get_response()
            ban_id2 = int(banid.text)
            users_ban(ban_id2)


@Amir.on(events.NewMessage(pattern="آمارربات"))
async def show_members(event: Message):
    try:
        await Amir.send_message(entity=admin, message=f"**تعداد اعضا ربات:** {len(members)}")
        await Amir.send_file(entity=admin, file="members.txt")
    except:
        await Amir.send_message(entity=admin, message="**فایلی در سرور وجود ندارد**")
#توابع 
def save_user_ids(user_id):
    #نام فایل
    file_name = "members.txt"
    #بررسی فایل ایا از قبل وجود داره
    if os.path.exists(file_name):
        with open(file_name, "r") as f:
            user_ids = json.load(f)
    else:
        user_ids = []

    #اضاقه کردن ایدی عددی جدید در صورت عدم وجود
    if user_id not in user_ids:
        user_ids.append(user_id)

        #ذخیره مجدد اطلاعات در فایل
        with open(file_name, "w") as f:
            json.dump(user_ids, f)

def users_ban(banid):
    filename = "banlist.txt"

    if os.path.exists(filename):
        with open(filename, "r") as bans:
            ban_ids = json.load(bans)
    else:
        ban_ids = []

    if banid not in ban_ids:
        ban_ids.append(banid)
        with open(filename, "w") as bans:
            json.dump(ban_ids, bans)

Amir.start()
print("Meta Bot is Starting......")
Amir.run_until_disconnected()


#از داخل فایل config.py موارد مورد نیاز پر شود

# https://t.me/Amirhaminjast

#ارتقا میدیم تا چند وقت دیگه 