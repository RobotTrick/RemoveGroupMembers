from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message

app = Client("RemoveAllMembers")

STARTED = 'הרובוט מתחיל בהסרת {} משתמשים מהקבוצה 🥾'
FINISH = 'הרובוט סיים להסיר {} משתמשים מהקבוצה'
ERROR = 'משהו נכשל. בדוק אם קיבלתי הרשאות ניהול מספיקות, או שלח זה למפתח:\n {}'
ADMIN_NEEDED = "כנראה שאו אני או אתה לא מנהלים... \nבשביל לבצע את הפעולה, שנינו זקוקים להיות מנהלים, ואני צריך הרשאה למחוק הודעות ולהעיף משתמשים."
PRIVATE = '''היי, אני רובוט שיעזור לכם להסיר את כל המשתמשים מהקבוצה שלכם 🥾

הוסיפו אותי לקבוצה, ואל תשכחו לתת לי ניהול מתאים כדי שאוכל להסיר אותם.
הוספתם? מעולה. עכשיו תשלחו בקבוצה /kick ואני אתחיל בעבודה שלי.'''


@app.on_message(filters.group & filters.command("kick"))
def main(_, msg: Message):
    chat = msg.chat
    me = chat.get_member(app.get_me().id)
    if chat.get_member(msg.from_user.id).can_manage_chat and me.can_restrict_members and me.can_delete_messages:
        try:
            msg.reply(STARTED.format(chat.members_count))
            count_kicks = 0
            for member in chat.iter_members():
                if not member.can_manage_chat:
                    chat.kick_member(member.user.id)
                    count_kicks += 1
            msg.reply(FINISH.format(count_kicks))
        except Exception as e:
            msg.reply(ERROR.format(str(e)))
    else:
        msg.reply(ADMIN_NEEDED)


@app.on_message(filters.group & filters.service, group=2)
def service(c, m):
    m.delete()


@app.on_message(filters.private)
def start(_, msg: Message):
    msg.reply(PRIVATE, reply_markup=InlineKeyboardMarkup([[
        InlineKeyboardButton("ערוץ עדכוני בוטים", url="t.me/m100achuzBots")]]))


app.run()
