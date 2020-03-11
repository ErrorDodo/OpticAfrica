import sqlite3

db = sqlite3.connect('main.sqlite')
cursor = db.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS main(
    guild_id TEXT,
    msg TEXT,
    channel_id TEXT,
    role TEXT
    )
''')
cursor.execute('''
    CREATE TABLE IF NOT EXISTS bans(
    guild_id TEXT,
    member_id TEXT
    )
''')
print("Sucessfully created tables")