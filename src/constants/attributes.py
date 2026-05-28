"""Stable attribute ids used across API and E2E tests.

Keep global, environment-independent ids here.
Environment-specific entities belong in data/ids.<env>.json.

Note:
The legacy source maps both AVATAR and WHATSAPP to id=12.
This may be correct for that API version or may need later verification
against swagger. We keep both names for compatibility with old tests.
"""

# V2 attributes / mobile / cards
AVATAR_ATTRIBUTE_ID_V2 = 12
FILE_ATTRIBUTE_ID = 7
PHOTO_GALLERY_ATTRIBUTE_ID = 10
PHONE_ATTRIBUTE_ID = 2
EMAIL_ATTRIBUTE_ID = 3
WHATSAPP_ATTRIBUTE_ID = 12
TELEGRAM_ATTRIBUTE_ID = 15
TEXT_ATTRIBUTE_ID = 6
BANNER_ATTRIBUTE_ID = 9
YOUTUBE_ATTRIBUTE_ID = 39
