# projects/forms.py
STATUS_CHOICES = [
        ('open', 'Открыт'),
        ('closed', 'Закрыт'),
    ]

# projects/models.py
MAX_LEN_PROJECT_NAME = 200
MAX_LEN_STATUS = 6

# projects/views.py
PROJECTS_PAGINATE_BY = 12
PROJECTS_ORDERING = '-created_at'
STATUS_CLOSED = 'closed'

# users/models.py
MAX_LEN_USER_NAME = 124
MAX_LEN_USER_SURNAME = 124
MAX_LEN_USER_PHONE = 12
MAX_LEN_GITHUB_URL = 256
MAX_LEN_ABOUT = 256
AVATAR_SIZE = (200, 200)
AVATAR_TEXT_COLOR = 'white'
