# ==========================================================
# TeRom-Punisher
# Configuration générale
# ==========================================================

BOT_NAME = "TeRom-Punisher"

# ==========================================================
# Seuils disciplinaires
# ==========================================================

WARNING_THRESHOLD = -3
PROBATION_THRESHOLD = -6
SUSPENDED_THRESHOLD = -10
BANNED_THRESHOLD = -15

# ==========================================================
# Types d'infractions
# ==========================================================

INFRACTIONS = {

    "TRICHE": {
        "label": "Triche"
    },

    "STREAMHACK": {
        "label": "Streamhack"
    },

    "INSULTE": {
        "label": "Insulte"
    },

    "TRASHTALK": {
        "label": "Trash-talk excessif"
    },

    "ANTI_SPORTIF": {
        "label": "Comportement anti-sportif"
    },

    "RETARD": {
        "label": "Retard"
    },

    "ABSENCE": {
        "label": "Absence"
    },

    "REFUS_MATCH": {
        "label": "Refus de jouer"
    },

    "AUTRE": {
        "label": "Autre"
    }
}

# ==========================================================
# Gravités
# ==========================================================

GRAVITIES = {

    "MINEURE": {
        "points": -1,
        "label": "Mineure"
    },

    "MOYENNE": {
        "points": -2,
        "label": "Moyenne"
    },

    "GRAVE": {
        "points": -3,
        "label": "Grave"
    },

    "CRITIQUE": {
        "points": -5,
        "label": "Critique"
    }
}

# ==========================================================
# Statuts disciplinaires
# ==========================================================

STATUS_NORMAL = "Normal"
STATUS_WARNING = "⚠️ Avertissement"
STATUS_PROBATION = "🟡 Probation"
STATUS_SUSPENDED = "🔴 Suspendu"
STATUS_BANNED = "⛔ Banni Ligue"

# ==========================================================
# Types de signalement
# ==========================================================

REPORT_TYPES = [
    "TRICHE",
    "STREAMHACK",
    "INSULTE",
    "TRASHTALK",
    "ANTI_SPORTIF",
    "RETARD",
    "ABSENCE",
    "REFUS_MATCH",
    "AUTRE"
]

# ==========================================================
# Statuts des dossiers
# ==========================================================

REPORT_PENDING = "PENDING"
REPORT_ACCEPTED = "ACCEPTE"
REPORT_REJECTED = "REFUSE"

# ==========================================================
# Protection des rôles
# Ces rôles ne seront jamais retirés
# automatiquement par le bot
# ==========================================================

PROTECTED_ROLE_NAMES = [

    "Admin",

    "🛑Modo",

    "⚠️ Avertissement",

    "🟡 Probation",

    "🔴 Suspendu",

    "⛔ Banni Ligue"
]

# ==========================================================
# Noms de rôles attendus
# ==========================================================

ADMIN_ROLE_NAME = "Admin"
MOD_ROLE_NAME = "🛑Modo"

WARNING_ROLE_NAME = "⚠️ Avertissement"
PROBATION_ROLE_NAME = "🟡 Probation"
SUSPENDED_ROLE_NAME = "🔴 Suspendu"
BANNED_ROLE_NAME = "⛔ Banni Ligue"

# ==========================================================
# Salons recommandés
# ==========================================================

REPORT_CHANNEL_NAME = "journal-signalements"
SANCTION_CHANNEL_NAME = "journal-sanctions"
APPEAL_CHANNEL_NAME = "appel-sanction"

# ==========================================================
# Limites signalements
# ==========================================================

MAX_REPORTS_PER_DAY = 5

REPORT_COOLDOWN_SECONDS = 300

# ==========================================================
# Messages
# ==========================================================

EMBED_COLOR = 0xE74C3C

SUCCESS_EMOJI = "✅"
ERROR_EMOJI = "❌"
WARNING_EMOJI = "⚠️"
REPORT_EMOJI = "📢"
