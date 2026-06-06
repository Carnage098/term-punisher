import aiosqlite
import datetime

DB_PATH = "data/judge.db"


# ==========================================================
# UTILITAIRES
# ==========================================================

def utc_now():
    return datetime.datetime.utcnow().isoformat()


# ==========================================================
# TABLES SQL
# ==========================================================

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
    sanction_channel_id INTEGER,
    appeal_channel_id INTEGER
);

CREATE TABLE IF NOT EXISTS seasons(
    id INTEGER PRIMARY KEY AUTOINCREMENT,

    guild_id INTEGER NOT NULL,

    name TEXT NOT NULL,

    active INTEGER DEFAULT 1,

    created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS players(
    guild_id INTEGER,
    user_id INTEGER,

    points INTEGER DEFAULT 0,

    PRIMARY KEY(guild_id,user_id)
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

CREATE TABLE IF NOT EXISTS audit_logs(
    id INTEGER PRIMARY KEY AUTOINCREMENT,

    guild_id INTEGER,

    user_id INTEGER,

    action TEXT,

    details TEXT,

    created_at TEXT
);
"""


# ==========================================================
# INITIALISATION
# ==========================================================

async def init_db():
    async with aiosqlite.connect(DB_PATH) as db:
        await db.executescript(CREATE_TABLES)
        await db.commit()


# ==========================================================
# SETTINGS
# ==========================================================

async def create_guild_settings(guild_id: int):
    async with aiosqlite.connect(DB_PATH) as db:

        await db.execute(
            """
            INSERT OR IGNORE INTO settings(guild_id)
            VALUES(?)
            """,
            (guild_id,)
        )

        await db.commit()


async def get_settings(guild_id: int):

    await create_guild_settings(guild_id)

    async with aiosqlite.connect(DB_PATH) as db:

        cursor = await db.execute(
            """
            SELECT *
            FROM settings
            WHERE guild_id = ?
            """,
            (guild_id,)
        )

        return await cursor.fetchone()


# ==========================================================
# JOUEURS
# ==========================================================

async def get_player_points(
    guild_id: int,
    user_id: int
):
    async with aiosqlite.connect(DB_PATH) as db:

        cursor = await db.execute(
            """
            SELECT points
            FROM players
            WHERE guild_id = ?
            AND user_id = ?
            """,
            (guild_id, user_id)
        )

        row = await cursor.fetchone()

        return row[0] if row else 0


async def update_player_points(
    guild_id: int,
    user_id: int,
    delta: int
):

    async with aiosqlite.connect(DB_PATH) as db:

        cursor = await db.execute(
            """
            SELECT points
            FROM players
            WHERE guild_id = ?
            AND user_id = ?
            """,
            (guild_id, user_id)
        )

        row = await cursor.fetchone()

        if row:

            new_points = row[0] + delta

            await db.execute(
                """
                UPDATE players
                SET points = ?
                WHERE guild_id = ?
                AND user_id = ?
                """,
                (
                    new_points,
                    guild_id,
                    user_id
                )
            )

        else:

            new_points = delta

            await db.execute(
                """
                INSERT INTO players(
                    guild_id,
                    user_id,
                    points
                )
                VALUES(?,?,?)
                """,
                (
                    guild_id,
                    user_id,
                    new_points
                )
            )

        await db.commit()

        return new_points


# ==========================================================
# SAISONS
# ==========================================================

async def create_season(
    guild_id: int,
    name: str
):
    async with aiosqlite.connect(DB_PATH) as db:

        await db.execute(
            """
            UPDATE seasons
            SET active = 0
            WHERE guild_id = ?
            """,
            (guild_id,)
        )

        await db.execute(
            """
            INSERT INTO seasons(
                guild_id,
                name,
                active,
                created_at
            )
            VALUES(?,?,1,?)
            """,
            (
                guild_id,
                name,
                utc_now()
            )
        )

        await db.commit()


# ==========================================================
# INFRACTIONS
# ==========================================================

async def add_infraction(
    guild_id,
    user_id,
    moderator_id,
    infraction_type,
    severity,
    points,
    reason
):

    async with aiosqlite.connect(DB_PATH) as db:

        await db.execute(
            """
            INSERT INTO infractions(
                guild_id,
                user_id,
                moderator_id,
                infraction_type,
                severity,
                points,
                reason,
                created_at
            )
            VALUES(?,?,?,?,?,?,?,?)
            """,
            (
                guild_id,
                user_id,
                moderator_id,
                infraction_type,
                severity,
                points,
                reason,
                utc_now()
            )
        )

        await db.commit()

    return await update_player_points(
        guild_id,
        user_id,
        points
    )


async def get_player_infractions(
    guild_id,
    user_id
):

    async with aiosqlite.connect(DB_PATH) as db:

        cursor = await db.execute(
            """
            SELECT *
            FROM infractions
            WHERE guild_id = ?
            AND user_id = ?
            ORDER BY id DESC
            """,
            (
                guild_id,
                user_id
            )
        )

        return await cursor.fetchall()


# ==========================================================
# SIGNALEMENTS
# ==========================================================

async def create_report(
    guild_id,
    reporter_id,
    reported_id,
    report_type,
    description,
    proof,
    anonymous,
    wants_contact
):

    async with aiosqlite.connect(DB_PATH) as db:

        cursor = await db.execute(
            """
            INSERT INTO reports(
                guild_id,
                reporter_id,
                reported_id,
                report_type,
                description,
                proof,
                anonymous,
                wants_contact,
                created_at
            )
            VALUES(?,?,?,?,?,?,?,?,?)
            """,
            (
                guild_id,
                reporter_id,
                reported_id,
                report_type,
                description,
                proof,
                int(anonymous),
                int(wants_contact),
                utc_now()
            )
        )

        await db.commit()

        return cursor.lastrowid


async def get_report(
    report_id
):

    async with aiosqlite.connect(DB_PATH) as db:

        cursor = await db.execute(
            """
            SELECT *
            FROM reports
            WHERE id = ?
            """,
            (report_id,)
        )

        return await cursor.fetchone()


async def get_all_reports():

    async with aiosqlite.connect(DB_PATH) as db:

        cursor = await db.execute(
            """
            SELECT *
            FROM reports
            ORDER BY id DESC
            """
        )

        return await cursor.fetchall()


# ==========================================================
# TÉMOIGNAGES
# ==========================================================

async def add_witness(
    report_id,
    witness_id,
    testimony,
    proof
):

    async with aiosqlite.connect(DB_PATH) as db:

        await db.execute(
            """
            INSERT INTO report_witnesses(
                report_id,
                witness_id,
                testimony,
                proof,
                created_at
            )
            VALUES(?,?,?,?,?)
            """,
            (
                report_id,
                witness_id,
                testimony,
                proof,
                utc_now()
            )
        )

        await db.commit()


# ==========================================================
# ACCEPTATION / REFUS
# ==========================================================

async def accept_report(
    report_id,
    moderator_id
):

    async with aiosqlite.connect(DB_PATH) as db:

        await db.execute(
            """
            UPDATE reports
            SET
                status='ACCEPTE',
                handled_by=?
            WHERE id=?
            """,
            (
                moderator_id,
                report_id
            )
        )

        await db.commit()


async def reject_report(
    report_id,
    moderator_id
):

    async with aiosqlite.connect(DB_PATH) as db:

        await db.execute(
            """
            UPDATE reports
            SET
                status='REFUSE',
                handled_by=?
            WHERE id=?
            """,
            (
                moderator_id,
                report_id
            )
        )

        await db.commit()


# ==========================================================
# LOGS
# ==========================================================

async def add_log(
    guild_id,
    user_id,
    action,
    details
):

    async with aiosqlite.connect(DB_PATH) as db:

        await db.execute(
            """
            INSERT INTO audit_logs(
                guild_id,
                user_id,
                action,
                details,
                created_at
            )
            VALUES(?,?,?,?,?)
            """,
            (
                guild_id,
                user_id,
                action,
                details,
                utc_now()
            )
        )

        await db.commit()
# ==========================================================
# ROLES
# ==========================================================

async def set_role_id(
    guild_id: int,
    role_type: str,
    role_id: int
):

    column_map = {
        "admin": "admin_role_id",
        "modo": "mod_role_id",
        "warning": "warning_role_id",
        "probation": "probation_role_id",
        "suspendu": "suspended_role_id",
        "banni": "banned_role_id"
    }

    column = column_map.get(role_type)

    if not column:
        return False

    async with aiosqlite.connect(DB_PATH) as db:

        await db.execute(
            f"""
            INSERT OR IGNORE INTO settings(guild_id)
            VALUES(?)
            """,
            (guild_id,)
        )

        await db.execute(
            f"""
            UPDATE settings
            SET {column}=?
            WHERE guild_id=?
            """,
            (
                role_id,
                guild_id
            )
        )

        await db.commit()

    return True


async def get_role_id(
    guild_id: int,
    role_type: str
):

    column_map = {
        "admin": "admin_role_id",
        "modo": "mod_role_id",
        "warning": "warning_role_id",
        "probation": "probation_role_id",
        "suspendu": "suspended_role_id",
        "banni": "banned_role_id"
    }

    column = column_map.get(role_type)

    if not column:
        return None

    async with aiosqlite.connect(DB_PATH) as db:

        cursor = await db.execute(
            f"""
            SELECT {column}
            FROM settings
            WHERE guild_id=?
            """,
            (guild_id,)
        )

        row = await cursor.fetchone()

        if row:
            return row[0]

        return None
    # ==========================================================
# SALONS
# ==========================================================

async def set_channel_id(
    guild_id: int,
    channel_type: str,
    channel_id: int
):

    column_map = {
        "signalements": "report_channel_id",
        "sanctions": "sanction_channel_id",
        "appel": "appeal_channel_id"
    }

    column = column_map.get(channel_type)

    if not column:
        return False

    async with aiosqlite.connect(DB_PATH) as db:

        await db.execute(
            """
            INSERT OR IGNORE INTO settings(guild_id)
            VALUES(?)
            """,
            (guild_id,)
        )

        await db.execute(
            f"""
            UPDATE settings
            SET {column}=?
            WHERE guild_id=?
            """,
            (
                channel_id,
                guild_id
            )
        )

        await db.commit()

    return True


async def get_channel_id(
    guild_id: int,
    channel_type: str
):

    column_map = {
        "signalements": "report_channel_id",
        "sanctions": "sanction_channel_id",
        "appel": "appeal_channel_id"
    }

    column = column_map.get(channel_type)

    if not column:
        return None

    async with aiosqlite.connect(DB_PATH) as db:

        cursor = await db.execute(
            f"""
            SELECT {column}
            FROM settings
            WHERE guild_id=?
            """,
            (guild_id,)
        )

        row = await cursor.fetchone()

        if row:
            return row[0]

        return None

# ==========================================================
# PERMISSIONS
# ==========================================================

async def is_admin(
    guild_id: int,
    member
):

    admin_role_id = await get_role_id(
        guild_id,
        "admin"
    )

    if not admin_role_id:
        return member.guild_permissions.administrator

    return any(
        role.id == admin_role_id
        for role in member.roles
    )


async def is_modo(
    guild_id: int,
    member
):

    if await is_admin(
        guild_id,
        member
    ):
        return True

    mod_role_id = await get_role_id(
        guild_id,
        "modo"
    )

    if not mod_role_id:
        return False

    return any(
        role.id == mod_role_id
        for role in member.roles
    )

async def get_all_reports_pending():

    async with aiosqlite.connect(DB_PATH) as db:

        cursor = await db.execute(
            """
            SELECT *
            FROM reports
            WHERE status='PENDING'
            ORDER BY id DESC
            """
        )

        return await cursor.fetchall()

async def get_all_reports_by_user(
    guild_id,
    user_id
):

    async with aiosqlite.connect(DB_PATH) as db:

        cursor = await db.execute(
            """
            SELECT *
            FROM reports
            WHERE guild_id=?
            AND reported_id=?
            ORDER BY id DESC
            """,
            (
                guild_id,
                user_id
            )
        )

        return await cursor.fetchall()
async def reset_player_points(
    guild_id,
    user_id
):

    async with aiosqlite.connect(DB_PATH) as db:

        await db.execute(
            """
            UPDATE players
            SET points=0
            WHERE guild_id=?
            AND user_id=?
            """,
            (
                guild_id,
                user_id
            )
        )

        await db.commit()

async def get_all_players(
    guild_id
):

    async with aiosqlite.connect(DB_PATH) as db:

        cursor = await db.execute(
            """
            SELECT *
            FROM players
            WHERE guild_id=?
            """
            ,
            (guild_id,)
        )

        return await cursor.fetchall()

async def get_all_reports_pending():

    async with aiosqlite.connect(DB_PATH) as db:

        cursor = await db.execute(
            """
            SELECT *
            FROM reports
            WHERE status='PENDING'
            ORDER BY id DESC
            """
        )

        return await cursor.fetchall()

async def get_all_reports_by_user(
    guild_id,
    user_id
):

    async with aiosqlite.connect(DB_PATH) as db:

        cursor = await db.execute(
            """
            SELECT *
            FROM reports
            WHERE guild_id=?
            AND reported_id=?
            ORDER BY id DESC
            """,
            (
                guild_id,
                user_id
            )
        )

        return await cursor.fetchall()

async def get_all_reports_pending():

    async with aiosqlite.connect(DB_PATH) as db:

        cursor = await db.execute(
            """
            SELECT *
            FROM reports
            WHERE status='PENDING'
            ORDER BY id DESC
            """
        )

        return await cursor.fetchall()


async def get_all_reports_by_user(
    guild_id,
    user_id
):

    async with aiosqlite.connect(DB_PATH) as db:

        cursor = await db.execute(
            """
            SELECT *
            FROM reports
            WHERE guild_id=?
            AND reported_id=?
            ORDER BY id DESC
            """,
            (
                guild_id,
                user_id
            )
        )

        return await cursor.fetchall()

async def get_all_reports_pending():

    async with aiosqlite.connect(DB_PATH) as db:

        cursor = await db.execute(
            """
            SELECT *
            FROM reports
            WHERE status='PENDING'
            ORDER BY id DESC
            """
        )

        return await cursor.fetchall()

async def get_all_reports_by_user(
    guild_id,
    user_id
):

    async with aiosqlite.connect(DB_PATH) as db:

        cursor = await db.execute(
            """
            SELECT *
            FROM reports
            WHERE guild_id=?
            AND reported_id=?
            ORDER BY id DESC
            """,
            (
                guild_id,
                user_id
            )
        )

        return await cursor.fetchall()

async def get_infraction_count(
    guild_id,
    user_id
):

    async with aiosqlite.connect(DB_PATH) as db:

        cursor = await db.execute(
            """
            SELECT COUNT(*)
            FROM infractions
            WHERE guild_id=?
            AND user_id=?
            """,
            (
                guild_id,
                user_id
            )
        )

        row = await cursor.fetchone()

        return row[0]

async def get_player_status(points: int):

    from config import (
        WARNING_THRESHOLD,
        PROBATION_THRESHOLD,
        SUSPENDED_THRESHOLD,
        BANNED_THRESHOLD
    )

    if points <= BANNED_THRESHOLD:
        return "BANNED"

    if points <= SUSPENDED_THRESHOLD:
        return "SUSPENDED"

    if points <= PROBATION_THRESHOLD:
        return "PROBATION"

    if points <= WARNING_THRESHOLD:
        return "WARNING"

    return "NORMAL"
    




