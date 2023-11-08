"""This file contains patterns for validating different input fields"""


class RegexPatterns:
    """This class has those Regex Pattern variables"""

    USERNAME_PATTERN = r"[A-Za-z0-9._%+-]+"
    NAME_PATTERN = r"([A-Za-z]{2,25}[\s]?)+"
    EMAIL_PATTERN = r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}"
    ROLE_PATTERN = r"(teacher|principal)"
    GENDER_PATTERN = r"^[m,f]{1}$"
    UUID_PATTERN = r"^[A-Za-z0-9]{6}$"
    DATE_PATTERN = r"^\d{2}-\d{2}-\d{4}$"
    DAYS_PATTERN = r"^[0-9]{1,2}$"
    MESSAGE_PATTERN = r"[\w\s.,!?'\"()/-]+"
    FAV_SUBJECT_PATTERN = r"([a-zA-z]+[\s]?)+"
    EXPERIENCE_PATTERN = r"^[0-9]{1,2}$"
    SCHOOL_NAME_PATTERN = r"^[A-Za-z]+([\sA-Za-z]+)*"
    PHONE_PATTERN = r"^[0-9]{10}$"
    PASSWORD_PATTERN = (
        r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{6,20}$"
    )
