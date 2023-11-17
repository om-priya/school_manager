# SCHOOL MANAGEMENT SYSTEM

**By: Om Priya (Batch 3)**

## Overview

This project aims to provide a management system for a school through which they can manage different entities in their school. The base assumption of this project is that it manages with the perspective of one school.

## Technologies Used

1. Python for programming language.
2. Sqlite3 for Database.
3. Tabulate Package to show data in a pretty format.
4. Shortuuid for unique Id.
5. Regular Expression for input validations.
6. VS Code for IDE.
7. Start UML for creating Diagrams.
8. Hashlib for hashing the password.
9. Makpass for masking the password.
10. Used logging for monitoring errors and information.

## Modules

### Super Admin

Super Admin is an entity which is one per school. Super Admin has different functionalities which include:

- Handling Principal: Super Admin can approve a principal, view, update, and delete a principal from the database.
- Handle Staff: Super Admin can perform CRUD operations on staff members.
- Distribute Salary: Super Admin can distribute salary to the respective teacher and principal.
- Approve Leave: Super Admin can approve the leave status applied by other entities.

### Principal

Principal is an entity which is also one per school. Principal has different functionalities which include:

- Handle Teacher
- Handle Feedback
- Handle Events
- Handle Leaves
- See Salary History
- View Issues

### Teacher

Teacher is an entity which can be many per school. The teacher can see his/her feedback, salary history, events, raise issues, and view the profile.

**Other Functionalities:**

- Login and Signup for different profiles.
- Input validation through regular expressions.
- Decorator to handle exceptions in the code.
- Pretty Print module which will print data in a pretty format.
