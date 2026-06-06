import aiosqlite

DB_PATH = "data/judge.db"

CREATE_TABLES = """
CREATE TABLE IF NOT EXISTS settings(
    guild_id INTEGER PRIMARY KEY,

    admin_role_id INTEGER,
    mod_role_id INTEGER,

    warning_role_id INTEGER,
    probation_role_id INTEGER,
    suspended_role_id INTEGER,
    banned_role_id INTEGER,

    report_channel_id INTEGER,
    sanction_channel_id INTEGER
);

CREATE TABLE IF NOT EXISTS players(
    guild_id INTEGER,
    user_id INTEGER,
    points INTEGER DEFAULT 0,

    PRIMARY KEY(guild_id,user_id)
);

CREATE TABLE IF NOT EXISTS reports(
    id INTEGER PRIMARY KEY AUTOINCREMENT,

    guild_id INTEGER,

    reporter_id INTEGER,
    reported_id INTEGER,

    report_type TEXT,

    description TEXT,
    proof TEXT,

    anonymous INTEGER DEFAULT 0,
    wants_contact INTEGER DEFAULT 0,

    status TEXT DEFAULT 'PENDING',

    handled_by INTEGER,

    created_at TEXT
);

CREATE TABLE IF NOT EXISTS report_witnesses(
    id INTEGER PRIMARY KEY AUTOINCREMENT,

    report_id INTEGER,
    witness_id INTEGER,

    testimony TEXT,
    proof TEXT,

    created_at TEXT
);

CREATE TABLE IF NOT EXISTS infractions(
    id INTEGER PRIMARY KEY AUTOINCREMENT,

    guild_id INTEGER,

    user_id INTEGER,
    moderator_id INTEGER,

    infraction_type TEXT,
    severity TEXT,

    points INTEGER,

    reason TEXT,

    created_at TEXT
);
"""

async def init_db():
    async with aiosqlite.connect(DB_PATH) as db:
        await db.executescript(CREATE_TABLES)
        await db.commit()
