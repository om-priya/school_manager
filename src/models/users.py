""" This Module contains a parent class which is named as User """


class User:
    """User class for getting basic info which will be inherited later on"""

    def __init__(self, name, gender, email, phone, school_name):
        self.name = name
        self.gender = gender
        self.email = email
        self.phone = phone
        self.school_name = school_name
