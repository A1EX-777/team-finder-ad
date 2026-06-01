# projects/forms.py
STATUS_CLOSED = 'closed'
STATUS_OPEN = 'open'
STATUS_CLOSED_RU = 'Закрыт'
STATUS_OPEN_RU = 'Открыт'
STATUS_CHOICES = [
        (STATUS_OPEN, STATUS_OPEN_RU),
        (STATUS_CLOSED, STATUS_CLOSED_RU),
    ]

# projects/models.py
MAX_LEN_PROJECT_NAME = 200
MAX_LEN_STATUS = 6

# projects/views.py
PROJECTS_PAGINATE_BY = 12
PROJECTS_ORDERING = '-created_at'

# users/models.py
MAX_LEN_USER_NAME = 124
MAX_LEN_USER_SURNAME = 124
MAX_LEN_USER_PHONE = 12
MAX_LEN_GITHUB_URL = 256
MAX_LEN_ABOUT = 256
AVATAR_SIZE = (200, 200)
AVATAR_FONT_SIZE = AVATAR_SIZE[0] // 2
AVATAR_TEXT_COLOR = 'white'
FONT_PATHS = (
    'fonts/DejaVuSans-Bold.ttf',
    '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',
)
