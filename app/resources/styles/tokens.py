"""Design tokens — the single source of truth for visual style.

Every colour, spacing value, font size, and radius used in the app
reads from this file. To rebrand or adjust the look, edit values
here only — never hard-code colours or sizes anywhere else.

Naming convention:
  - SCREAMING_SNAKE_CASE for token constants
  - Group by purpose (Brand, Surface, Text, etc.)
"""

# ════════════════════════════════════════════════════════════════════
# BRAND COLOURS — primary identity
# ════════════════════════════════════════════════════════════════════
PRIMARY         = "#2563EB"
PRIMARY_HOVER   = "#1D4ED8"
PRIMARY_ACTIVE  = "#1E40AF"
PRIMARY_LIGHT   = "#DBEAFE"
PRIMARY_TEXT    = "#FFFFFF"


# ════════════════════════════════════════════════════════════════════
# ACCENT COLOURS — gold, used sparingly for premium feel
# ════════════════════════════════════════════════════════════════════
ACCENT          = "#C9A961"
ACCENT_HOVER    = "#B8985A"
ACCENT_LIGHT    = "#F5EFE0"
ACCENT_DARK     = "#8B7340"

# ════════════════════════════════════════════════════════════════════
# SIDEBAR / DARK SURFACES — dark navy palette for the app shell sidebar
# Inspired by modern POS dashboards (Toast, Square, Lightspeed)
# ════════════════════════════════════════════════════════════════════
SIDEBAR_BG          = "#0F172A"   # slate-900 — deep navy, main sidebar fill
SIDEBAR_BG_HOVER    = "#1E293B"   # slate-800 — hover state for menu items
SIDEBAR_BG_ACTIVE   = "#1D4ED8"   # blue-700 — active menu item
SIDEBAR_BORDER      = "#1E293B"   # subtle separator lines on dark bg
SIDEBAR_TEXT        = "#CBD5E1"   # slate-300 — default menu text (readable on dark)
SIDEBAR_TEXT_MUTED  = "#64748B"   # slate-500 — section headers, store info
SIDEBAR_TEXT_ACTIVE = "#FFFFFF"   # white — active menu item text
SIDEBAR_BRAND_TEXT  = "#FFFFFF"   # "POS System" / "MosTek ElectroPOS" wordmark
SIDEBAR_BRAND_SUB   = "#94A3B8"   # "Premium Edition" / tagline
# ════════════════════════════════════════════════════════════════════
# SEMANTIC COLOURS
# ════════════════════════════════════════════════════════════════════
SUCCESS         = "#16A34A"
SUCCESS_LIGHT   = "#DCFCE7"
SUCCESS_TEXT    = "#FFFFFF"

WARNING         = "#F59E0B"
WARNING_LIGHT   = "#FEF3C7"
WARNING_TEXT    = "#FFFFFF"

DANGER          = "#DC2626"
DANGER_HOVER    = "#B91C1C"
DANGER_LIGHT    = "#FEE2E2"
DANGER_TEXT     = "#FFFFFF"

INFO            = "#0EA5E9"
INFO_LIGHT      = "#E0F2FE"


# ════════════════════════════════════════════════════════════════════
# SURFACES — backgrounds and borders
# ════════════════════════════════════════════════════════════════════
BG_APP          = "#F8FAFC"
BG_CARD         = "#FFFFFF"
BG_HOVER        = "#F1F5F9"
BG_ACTIVE       = "#E2E8F0"
BG_INPUT        = "#FFFFFF"
BG_DISABLED     = "#F1F5F9"

BORDER          = "#E2E8F0"
BORDER_STRONG   = "#CBD5E1"
BORDER_FOCUS    = "#2563EB"


# ════════════════════════════════════════════════════════════════════
# TEXT
# ════════════════════════════════════════════════════════════════════
TEXT_PRIMARY    = "#0F172A"
TEXT_SECONDARY  = "#334155"
TEXT_MUTED      = "#64748B"
TEXT_DISABLED   = "#94A3B8"
TEXT_INVERSE    = "#FFFFFF"


# ════════════════════════════════════════════════════════════════════
# TYPOGRAPHY
# ════════════════════════════════════════════════════════════════════
FONT_FAMILY     = "Inter"
FONT_FALLBACK   = "Segoe UI, system-ui, sans-serif"

FONT_SIZE_XS    = 12
FONT_SIZE_SM    = 13
FONT_SIZE_BASE  = 14
FONT_SIZE_LG    = 16
FONT_SIZE_XL    = 20
FONT_SIZE_2XL   = 24
FONT_SIZE_3XL   = 32

FONT_WEIGHT_REGULAR  = 400
FONT_WEIGHT_MEDIUM   = 500
FONT_WEIGHT_SEMIBOLD = 600
FONT_WEIGHT_BOLD     = 700


# ════════════════════════════════════════════════════════════════════
# SPACING SCALE (px)
# ════════════════════════════════════════════════════════════════════
SPACE_1  = 4
SPACE_2  = 8
SPACE_3  = 12
SPACE_4  = 16
SPACE_5  = 20
SPACE_6  = 24
SPACE_8  = 32
SPACE_10 = 40
SPACE_12 = 48


# ════════════════════════════════════════════════════════════════════
# BORDER RADIUS
# ════════════════════════════════════════════════════════════════════
RADIUS_SM = 4
RADIUS_MD = 8     # bumped from 6 — softer, more modern feel
RADIUS_LG = 12    # bumped from 8
RADIUS_XL = 16


# ════════════════════════════════════════════════════════════════════
# COMPONENT SIZES — bumped for premium feel and accessibility
# ════════════════════════════════════════════════════════════════════
INPUT_HEIGHT          = 52   # text fields, dropdowns — premium look (login, main forms)
INPUT_HEIGHT_COMPACT  = 40   # for dialogs and dense forms
INPUT_FONT_SIZE       = 16   # font inside inputs
BUTTON_HEIGHT         = 44   # standard buttons
BUTTON_HEIGHT_LG      = 52   # primary call-to-action buttons
ROW_HEIGHT            = 48


# ════════════════════════════════════════════════════════════════════
# SHADOWS (documentation only — Qt QSS doesn't support real box-shadow)
# ════════════════════════════════════════════════════════════════════
SHADOW_SM = "0 1px 2px rgba(0, 0, 0, 0.05)"
SHADOW_MD = "0 4px 6px rgba(0, 0, 0, 0.07)"
SHADOW_LG = "0 10px 15px rgba(0, 0, 0, 0.10)"