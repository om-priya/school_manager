""" This module is for displaying message in the console """


class DisplayMenu:
    """This Class Contains All the display prompt for the console"""

    SUPER_ADMIN_MAIN_PROMPT = """\nWelcome Super Admin
    What do you want to do?
    1> Handle Principal
    2> Handle Staff
    3> Distribute Salary
    4> Approve Leave
    5> Log Out
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
    8> Log Out
    \n"""
    TEACHER_MAIN_PROMPT = """\nWelcome Teacher
    What do you want to do?
    1> View My Profile
    2> Read Notice Board
    3> Read FeedBacks
    4> Raise Issues
    5> See Salary History
    6> Log Out
    \n"""
    HANDLE_TEACHER_PROMPT = """\nWhat do you want to do?
    1> Approve Teacher
    2> Get All Teacher
    3> Get Teacher by ID
    4> Update Teacher
    5> Delete Teacher
    \n"""
    FEEDBACK_PROMPT = """\nWhat do yu want to do?
    1> Read Feedback
    2> Create Feedback
    \n"""
    EVENTS_PROMPT = """\nWhat do you want to do?
    1> Read Event
    2> Create Event
    \n"""
    LEAVES_PROMPT = """\nWhat do you want to do?
    1> Check Leave Status
    2> Apply for Leave
    \n"""
    HANDLE_PRINCIPAL_PROMPT = """\nWhat do you want to do?
    1> Approve Principal
    2> Get All Principal
    3> Get Principal by ID
    4> Update Principal
    5> Delete Principal
    \n"""
    HANDLE_STAFF_PROMPT = """\nWhat do you want to do?
    1> View All Staff Members
    2> Create Staff Members
    3> Update Staff Members
    4> Delete Staff Members
    \n"""
    ENTRY_POINT_PROMPT = """\nWelcome User
    1> Log In
    2> Sign Up
    \n"""


class PromptMessage:
    """This class contains prompts for displayind in console"""

    GREET_PROMPT = """\nWelcome {}\n"""
    NOTHING_FOUND = "\nNo such {} Found\n"
    ADDED_SUCCESSFULLY = """\n{} Added Successfully\n"""
    INVALID_INPUT = """\nInvalid Input {}\n"""
    TAKE_INPUT = """\nEnter Your {}: """
    DENIED_ACCESS = """\nYou Don't have access to {}"""
    LOGGED_OUT = """\nLogged Out Successfully"""
    DATE_INPUT = """\nEnter date in format dd-mm-yyyy: """
    NO_SCHOOL_FOUND = """\nWrong School Or School is not in the system"""
    SIGNED_UP_SUCCESS = (
        """\nSigned Up Successfully Wait for Super Admin to approve it."""
    )
    WRONG_CREDENTIALS = """\nWrong Credentials"""
    PENDING_USER_LOG_IN = """\nAsk Super Admin to approve first"""
    APPROVE_PROMPT = "\nEnter the {} you want to approve: "
    TAKE_SPECIFIC_ID = """\nEnter {} User ID: """
    INVALID_DATE = """\n{} is previous to curr date {}"""
    MULTIPLE_PRINCIPAL_ERROR = """\nCan't add more than one principal"""
    FIELD_UPDATE = """\nEnter the field you want to update: """
    APPROVE_FAILED = """\n{} Can't be Approved"""
    APPROVE_SUCCESS = """\n{} Approved SuccessFully"""
    FAILED_ACTION = """\nCan't perform {} action on entered user_id"""
    SUCCESS_ACTION = """\n{} Successfully"""
