""" This module is for displaying message in the console """


class DisplayMenu:
    """This Class Contains All the display prompt for the console"""

    SUPER_ADMIN_MAIN_PROMPT = """\nWelcome Super Admin
    What do you want to do?
    1> Handle Principal
    2> Handle Staff
    3> Distribute Salary
    4> Approve Leave
    5> Change Password
    6> Log Out
    \n"""
    PRINCIPAL_MAIN_PROMPT = """\nWelcome Principal
    What do you want to do?
    1> Handle Teacher 
    2> Manage Feedbacks
    3> Manage Events
    4> Manage Leaves
    5> View My Profile
    6> See Salary History
    7> Read Issues
    8> Change Password
    9> Log Out
    \n"""
    TEACHER_MAIN_PROMPT = """\nWelcome Teacher
    What do you want to do?
    1> View My Profile
    2> Read Notice Board
    3> Read FeedBacks
    4> Raise Issues
    5> See Salary History
    6> Handle Leaves
    7> Change Password
    8> Log Out
    \n"""
    HANDLE_TEACHER_PROMPT = """\nWhat do you want to do?
    1> Approve Teacher
    2> Get All Teacher
    3> Get Teacher by ID
    4> Update Teacher
    5> Delete Teacher
    6> Go Back
    \n"""
    FEEDBACK_PROMPT = """\nWhat do yu want to do?
    1> Read Feedback
    2> Create Feedback
    3> Go Back
    \n"""
    EVENTS_PROMPT = """\nWhat do you want to do?
    1> Read Event
    2> Create Event
    3> Go Back
    \n"""
    LEAVES_PROMPT = """\nWhat do you want to do?
    1> Check Leave Status
    2> Apply for Leave
    3> Go Back
    \n"""
    HANDLE_PRINCIPAL_PROMPT = """\nWhat do you want to do?
    1> Approve Principal
    2> Get All Principal
    3> Get Principal by ID
    4> Update Principal
    5> Delete Principal
    6> Go Back
    \n"""
    HANDLE_STAFF_PROMPT = """\nWhat do you want to do?
    1> View All Staff Members
    2> Create Staff Members
    3> Update Staff Members
    4> Delete Staff Members
    5> Go Back
    \n"""
    ENTRY_POINT_PROMPT = """\nWelcome User
    1> Log In
    2> Sign Up
    \n"""


class PromptMessage:
    """This class contains prompts for displayind in console"""

    GREET_PROMPT = """Welcome {}"""
    NOTHING_FOUND = "No such {} Found"
    ADDED_SUCCESSFULLY = """{} Added Successfully"""
    INVALID_INPUT = """Invalid Input {}"""
    TAKE_INPUT = """Enter Your {}: """
    DENIED_ACCESS = """You Don't have access to {}"""
    LOGGED_OUT = """Logged Out Successfully"""
    DATE_INPUT = """Enter date in format dd-mm-yyyy: """
    NO_SCHOOL_FOUND = """Wrong School Or School is not in the system"""
    SIGNED_UP_SUCCESS = """Signed Up Successfully Wait for Super Admin to approve it."""
    WRONG_CREDENTIALS = """Wrong Credentials"""
    PENDING_USER_LOG_IN = """Ask Super Admin to approve first"""
    APPROVE_PROMPT = "Enter the {} you want to approve: "
    TAKE_SPECIFIC_ID = """Enter {} User ID: """
    INVALID_DATE = """{} is previous to curr date {}"""
    MULTIPLE_PRINCIPAL_ERROR = """Can't add more than one principal"""
    FIELD_UPDATE = """Enter the field you want to update: """
    APPROVE_FAILED = """{} Can't be Approved"""
    APPROVE_SUCCESS = """{} Approved SuccessFully"""
    FAILED_ACTION = """Can't perform {} action on entered user_id"""
    SUCCESS_ACTION = """{} Successfully"""
    WRONG_QUERY = """kindly Check Your Query: """
    NEW_PASSWORD_PROMPT = "Enter Your New Password"
    TOKEN_RESPONSE = "Token is {}"
