""" This Module contains a parent class which is named as User """


class User:
    """
    User class for storing basic information.

    Attributes:
    - user_name (str): The name of the user.
    - gender (str): The gender of the user.
    - email (str): The email address of the user.
    - phone (str): The phone number of the user.
    - school_name (str): The name of the user's school.
    """

    def __init__(self, name, gender, email, phone, school_name):
        """
        Initializes a User object with basic information.

        Parameters:
        - user_name (str): The name of the user.
        - gender (str): The gender of the user.
        - email (str): The email address of the user.
        - phone (str): The phone number of the user.
        - school_name (str): The name of the user's school.
        """
        self.name = name
        self.gender = gender
        self.email = email
        self.phone = phone
        self.school_name = school_name
