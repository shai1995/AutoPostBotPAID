from pyrogram import Client, filters
from pyrogram.types import Message
import asyncio
import datetime
import pytz
import pymongo
from pyrogram.enums import ChatMemberStatus
from pyrogram.types import InlineKeyboardButton as ikb, InlineKeyboardMarkup as ikm
from config import API_ID, API_HASH, BOT_TOKEN, MONGO_DB_URL, ADMIN
# Connect to MongoDB Atlas
mongo_client = pymongo.MongoClient(
    MONGO_DB_URL)
db = mongo_client["AutoPost_Bot"]
chat_id_collection = db["chat_ids"]
time_collection = db['time']


ADMIN_ID = [int(admin_id) for admin_id in ADMIN.split(',')]


# Initialize Pyrogram Client
bot = Client("auto_post_bottt",
             bot_token=BOT_TOKEN,
             api_id=API_ID,
             api_hash=API_HASH
             )
keyboard = [
    [
        ikb(text="Contact Admin", url='https://t.me/brandsfoxtenx')
    ]
]
reply_markup = ikm(keyboard)


@bot.on_message(filters.command('start') & filters.private)
async def start(bot, message):
    if message.from_user.id not in ADMIN_ID:
        emej = "AgACAgUAAxkBAAIBg2X8mdjM7R_oRIvdXoMgRMzdGKaUAAI7uzEbaZ7gV8thiDujveP5AAgBAAMCAAN5AAceBA"
        await bot.send_photo(message.chat.id,emej,f'''<b>ACCESS DENIED ⚠️ 

Dear {message.from_user.first_name},
You don’t have any access to use this Bot, Kindly contact admin by clicking on Contact admin button or contact by mail : 

brandsfox.official@gmail.com 

Thankyou 
AUTO POST BOT 🤖</b>.''')
        return
    emoji = "AgACAgUAAxkBAAMaZfm5nPDx3MSExO0ur9LEuInpai4AAhq8MRv1lslXDW5_2SlrXdUACAEAAwIAA3kABx4E"
    await bot.send_photo(message.chat.id, emoji, caption=f'''<b>Hello {message.from_user.first_name},

Welcome to AUTO POST UPDATER BOT🤖 

I can post messeges &   Photos to any channel with schedule time.

Powered By : Brandsfox Media Pvt Ltd 

 Type /help to know more ! </b>''', reply_markup=reply_markup)


@bot.on_message(filters.command('help') & filters.private)
async def help_command(bot, message):
    if message.from_user.id not in ADMIN_ID:
        emej = "AgACAgUAAxkBAAIBg2X8mdjM7R_oRIvdXoMgRMzdGKaUAAI7uzEbaZ7gV8thiDujveP5AAgBAAMCAAN5AAceBA"
        await bot.send_photo(message.chat.id,emej,f'''<b>ACCESS DENIED ⚠️ 

Dear {message.from_user.first_name},
You don’t have any access to use this Bot, Kindly contact admin by clicking on Contact admin button or contact by mail : 

brandsfox.official@gmail.com 

Thankyou 
AUTO POST BOT 🤖</b>.''')
        return
    help_text = """
    <b>How to Use AutoPost Bot:</b>

    <b>Step 1:</b> Add the bot to your channel and make it an admin.

    <b>Step 2:</b> Get your channel ID.

    <b>Step 3:</b> Add the channel ID to the bot using the /add command.
        <i>Example: /add [channel_id] [id_value]</i>

    <b>Step 4:</b> Select the channel for which you want to set the message using the /set command.
        <i>Example: /set</i>

    <b>Step 5:</b> The bot will prompt you to send the message that you want to post to the selected channel.

    <b>Step 6:</b> Once you send the message, it will be stored for the selected channel.

    <b>Step 7:</b> Add a scheduled time to post the message using the /time command.
        <i>Example: /time [HH:MM] [DD/MM/YYYY]</i>

    <b>Commands:</b>
    <code>
    /start - Start the bot
    /help - Display this help message
    /add [channel_id] [id_value] - Add a channel ID to the bot
    /set - Select a channel to set a message
    /time [HH:MM] [DD/MM/YYYY] - Schedule a time to post the message
    </code>

    """
    await message.reply_text(help_text)


async def check_time_match(user_time, user_date):
    # Get the current Indian time
    ist = pytz.timezone('Asia/Kolkata')
    current_time = datetime.datetime.now(ist)

    # Parse user-provided time and date
    user_hour, user_minute = map(int, user_time.split(':'))
    user_day, user_month, user_year = map(int, user_date.split('/'))

    # Convert user-provided date to a datetime object
    user_datetime = ist.localize(datetime.datetime(
        user_year, user_month, user_day, user_hour, user_minute))
    if (current_time.hour == user_datetime.hour and
        current_time.minute == user_datetime.minute and
        current_time.day == user_day and
            current_time.month == user_month):
        return True
    else:
        return False

async def start(self):
        # Start aiohttp web server
        app = web.AppRunner(await wsrvr())
        await app.setup()
        ba = "0.0.0.0"
        port = int(os.environ.get("PORT", 8080)) or 8080
        await web.TCPSite(app, ba, port).start()

async def perform_broadcast():
    try:
        for chat in chat_id_collection.find():
            chat_id = chat["chat_id"]
            message = chat.get("message")
            media = chat.get("media", None)
            if media:
                try:
                    await bot.send_photo(chat_id, media, caption=message)
                except:
                    pass
            else:
                try:
                    await bot.send_message(chat_id, message)
                except:
                    pass
    except Exception as e:
        print(f"Error during broadcast: {e}")


@bot.on_message(filters.command('time') & filters.private)
async def set_broadcast_time(bot, message):
    if message.from_user.id not in ADMIN_ID:
        emej = "AgACAgUAAxkBAAIBg2X8mdjM7R_oRIvdXoMgRMzdGKaUAAI7uzEbaZ7gV8thiDujveP5AAgBAAMCAAN5AAceBA"
        await bot.send_photo(message.chat.id,emej,f'''<b>ACCESS DENIED ⚠️ 

Dear {message.from_user.first_name},
You don’t have any access to use this Bot, Kindly contact admin by clicking on Contact admin button or contact by mail : 

brandsfox.official@gmail.com 

Thankyou 
AUTO POST BOT 🤖</b>.''')
        return
    try:
        user_input = message.text.split(maxsplit=1)[1]
        user_time, user_date = user_input.split()[:2]

        BroadcastMSG = await message.reply_text(f"Broadcast is scheduled for {user_input}.")

        while True:
            if await check_time_match(user_time, user_date):
                TimeOut = await message.reply_text(f"<i>The scheduled time {user_input} has been reached. Broadcasting now!</i>")
                await perform_broadcast()
                await BroadcastMSG.delete()
                await TimeOut.delete()
                break

            await asyncio.sleep(5)  # Check every 30 seconds
    except ValueError:
        INVLDtmpFrmt = await message.reply_text("<b> Invalid time format. Please provide the time in 'HH:MM DD/MM/YY' format. </b>")
        await asyncio.sleep(5)
        await INVLDtmpFrmt.delete()


@bot.on_message(filters.command('add') & filters.private)
async def ChannelAdd(bot, message):
    if message.from_user.id not in ADMIN_ID:
        emej = "AgACAgUAAxkBAAIBg2X8mdjM7R_oRIvdXoMgRMzdGKaUAAI7uzEbaZ7gV8thiDujveP5AAgBAAMCAAN5AAceBA"
        await bot.send_photo(message.chat.id,emej,f'''<b>ACCESS DENIED ⚠️ 

Dear {message.from_user.first_name},
You don’t have any access to use this Bot, Kindly contact admin by clicking on Contact admin button or contact by mail : 

brandsfox.official@gmail.com 

Thankyou 
AUTO POST BOT 🤖</b>.''')
        return
    try:
        # Extract chat ID and ID from the command
        parts = message.text.split(maxsplit=2)
        chat_id = int(parts[1])
        id_value = int(parts[2]) if len(parts) > 2 else None
        if id_value == None:
            return
        AddChannelDB = await bot.send_message(message.chat.id, "<code><b><i>Adding Channel in Database..</i></b></code>")
        if chat_id_collection.find_one({"id": id_value}):
            await AddChannelDB.delete()
            IDisTakenMsg = await bot.send_message(message.chat.id, f"The ID {id_value} is already taken.")
            await asyncio.sleep(3)
            await IDisTakenMsg.delete()
            return
        else:
            await AddChannelDB.delete()
            pass
        try:

            chat_info = await bot.get_chat(chat_id)
            chat_name = chat_info.title if chat_info.title else "Unnamed Chat"

            # Insert the chat ID and name into the database
            await AddChannelDB.delete()
            chat_id_collection.insert_one(
                {"chat_id": chat_id, "name": chat_name, "id": id_value})
            AddMsg = await bot.send_message(message.chat.id, f"<b><i>Chat ID {chat_id} added successfully with ID {id_value}.</b></i>")
            await asyncio.sleep(5)
            await AddMsg.delete()
        except:
            TRY_ADD = await bot.send_message(message.chat.id, "INVALID CHANNEL ID.... \nor \nITS NOT A CHANNEL ID....")
            await asyncio.sleep(5)
            await TRY_ADD.delete()
    except ValueError:
        Err1 = await bot.send_message(message.chat.id, "Invalid parameters. Please provide a valid chat ID and ID value.")
        await asyncio.sleep(2)
        await Err1.delete()
# Command handler for /set


@bot.on_message(filters.command('set') & filters.private & ~filters.reply)
async def select_chat_for_message(bot, message):
    if message.from_user.id not in ADMIN_ID:
        emej = "AgACAgUAAxkBAAIBg2X8mdjM7R_oRIvdXoMgRMzdGKaUAAI7uzEbaZ7gV8thiDujveP5AAgBAAMCAAN5AAceBA"
        await bot.send_photo(message.chat.id,emej,f'''<b>ACCESS DENIED ⚠️ 

Dear {message.from_user.first_name},
You don’t have any access to use this Bot, Kindly contact admin by clicking on Contact admin button or contact by mail : 

brandsfox.official@gmail.com 

Thankyou 
AUTO POST BOT 🤖</b>.''')
        return
    try:
        chats = list(chat_id_collection.find({}))

        if not chats:
            await message.reply_text("No chats found. Please add chats using /add command first.")
            return
        keyboard = []
        for chat in chats:
            try:
                chat_id = chat.get('id')
                chat_name = chat.get('name', 'Unnamed Chat')
            except:
                pass
            if chat_id:
                keyboard.append(
                    [ikb(chat_name, callback_data=f"select_chat_{chat_id}")])

        if not keyboard:
            await message.reply_text("No valid chats found. Please ensure chat documents have 'id' field.")
            return

        reply_markup = ikm(keyboard)
        global SelectChatMsg
        SelectChatMsg = await message.reply_text("Select chat:", reply_markup=reply_markup)
    except Exception as e:
        print(f"Error in select_chat_for_message: {e}")


# Command handler for /set with ID argument
awaiting_message = False

# Command handler for /set with ID argument


@bot.on_callback_query(filters.regex(r'select_chat_(\d+)'))
async def select_chat_callback(bot, query):

    try:
        global awaiting_message

        chat_id = int(query.matches[0].group(1))

        # Retrieve chat name
        chat_data = chat_id_collection.find_one({"id": chat_id})
        chat_name = chat_data.get("name", "Unnamed Chat")

        # Update user's selected chat ID
        chat_id_collection.update_one({"user_id": query.from_user.id}, {
                                      "$set": {"selected_chat_id": chat_id}}, upsert=True)

        # Send confirmation message with selected ID and chat name
        await SelectChatMsg.delete()
        global SelectedChatMsg
        SelectedChatMsg = await bot.send_message(query.message.chat.id, f"You have selected:\nID: {chat_id}\nGroup: {chat_name}\n\nPlease send a message to store.")

        # Set the flag to indicate that the bot is awaiting a message
        awaiting_message = True
    except Exception as e:
        print(f"Error in select_chat_callback: {e}")

# Handler to store the message in the database


@bot.on_message(filters.private)
async def store_message(bot, message):
    global awaiting_message
    try:
        if awaiting_message:
            # Retrieve user's selected chat ID
            user_data = chat_id_collection.find_one(
                {"user_id": message.from_user.id})
            if not user_data or 'selected_chat_id' not in user_data:
                await message.reply_text("No chat selected. Please use /set command to select a chat first.")
                return

            chat_id = user_data['selected_chat_id']

            # Check if a message already exists for the selected chat ID
            existing_message = chat_id_collection.find_one({"id": chat_id})

            # Extract text and media from the message
            text = message.text or ""
            photo = message.photo
            caption = message.caption or ""
            media = None

            if photo:
                media = photo.file_id or f"https://t.me/{
                    message.chat.username}/{photo.file_unique_id}"

            if existing_message:
                if caption == "baaz1":
                    text = '''<b>BAAZIGAR ONLINE BOOK‼️
🏏🎰⚽️🎾🐎🏒🏟️

Top service provider in whole market /- 
> 5Min For Withdrawal 
> 24/7 Service available 
> 24/7 Customer support 
> 365 Days withdrawal ( including holidays) 

To ab Der kis baat ki hojaao shuru 🤩

Contact on Whatsapp for new id or deposit 📞☎️👇👇👇</b>

wa.me/917742107728
wa.me/917742107728
wa.me/917742107728

Join Telegram 👇
https://t.me/baazigarbook_official

Join instagram 👇
https://instagram.com/baazigar_online_book_?igshid=YmMyMTA2M2Y='''
                    await SelectedChatMsg.delete()
                    chat_id_collection.update_one(
                        {"id": chat_id}, {"$set": {"message": text or caption, "media": media}})
                    await message.reply_text(f"Message updated successfully for ID {chat_id}!")
                if caption == "sq1":
                    text = '''<b>SWEETY QUEEN ✔️ ONLINE BOOK 💙
🏏🎰⚽️🎾🐎🏒🏟️

PLAY BIG EARN BIG

ALL FANCIES & PREMIUM SITES AVAILABLE

WhatsApp For I'd</b>

💬https://wa.me/919368909962
💬https://wa.me/919368909962
💬https://wa.me/919368909962
💬https://wa.me/919368909962
💬https://wa.me/919368909962

❤️ Sweety Book Telegram 👇
https://t.me/sweety_tiwari1'''
                    await SelectedChatMsg.delete()
                    chat_id_collection.update_one(
                        {"id": chat_id}, {"$set": {"message": text or caption, "media": media}})
                    await message.reply_text(f"Message updated successfully for ID {chat_id}!")
                else:
                    await SelectedChatMsg.delete()
                    chat_id_collection.update_one(
                        {"id": chat_id}, {"$set": {"message": text or caption, "media": media}})
                    await message.reply_text(f"Message updated successfully for ID {chat_id}!")
            else:
                if caption == "baaz1":
                    text = '''<b>BAAZIGAR ONLINE BOOK‼️
🏏🎰⚽️🎾🐎🏒🏟️

Top service provider in whole market /- 
> 5Min For Withdrawal 
> 24/7 Service available 
> 24/7 Customer support 
> 365 Days withdrawal ( including holidays) 

To ab Der kis baat ki hojaao shuru 🤩

Contact on Whatsapp for new id or deposit 📞☎️👇👇👇</b>

wa.me/917742107728
wa.me/917742107728
wa.me/917742107728

Join Telegram 👇
https://t.me/baazigarbook_official

Join instagram 👇
https://instagram.com/baazigar_online_book_?igshid=YmMyMTA2M2Y='''
                    await SelectedChatMsg.delete()
                    chat_id_collection.insert_one(
                        {"id": chat_id}, {"$set": {"message": text or caption, "media": media}})
                    await message.reply_text(f"Message updated successfully for ID {chat_id}!")
                if caption == "sq1":
                    text = '''<b>SWEETY QUEEN ✔️ ONLINE BOOK 💙
🏏🎰⚽️🎾🐎🏒🏟️

PLAY BIG EARN BIG

ALL FANCIES & PREMIUM SITES AVAILABLE

WhatsApp For I'd</b>

💬https://wa.me/919368909962
💬https://wa.me/919368909962
💬https://wa.me/919368909962
💬https://wa.me/919368909962
💬https://wa.me/919368909962

❤️ Sweety Book Telegram 👇
https://t.me/sweety_tiwari1'''
                    await SelectedChatMsg.delete()
                    chat_id_collection.insert_one(
                        {"id": chat_id}, {"$set": {"message": text or caption, "media": media}})
                    await message.reply_text(f"Message updated successfully for ID {chat_id}!")
                else:
                    await SelectedChatMsg.delete()
                    chat_id_collection.insert_one(
                        {"id": chat_id, "message": text or caption, "media": media})
                    await message.reply_text(f"Message stored successfully for ID {chat_id}!")

            try:
                chat_id_collection.delete_many(
                    {"selected_chat_id": {"$exists": True}})
            except:
                pass

            awaiting_message = False
    except Exception as e:
        print(f"Error in store_message: {e}")

bot.run()
