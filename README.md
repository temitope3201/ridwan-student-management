# ridwan-student-management

## Table of Contents
- [Introduction](#introduction)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [Live Demo](#live-demo)
- [Upcoming Features](#upcoming-features)
- [License](#license)

## Introduction
This is a simple school management system API built with Flask and Flask_RestX built by according to [this requirements](https://docs.google.com/document/d/19ayXN5P1oV2aqW_7-As6EUpn7OQShkpAlZK4wRbrgBQ/). It is a simple API that does basic student management duties for an educational institution. It allows an admin to create, read, update and delete students and courses.

## Features
- The first user/admin created will be the default admin
- Admin can create, read, update and delete students and courses
- Only Admins can add other admin users
- Students can register and unregister for courses
- Admin can add grade for students in each course
- Admin can view all students and courses
- Admin can view all students registered to a course
- Admin can view all courses a student is registered to
- User/Student can view all courses he/she is registered to and the grade he/she got for each course
- Student can view their overall GPA
- User/Student can update his/her password
- Default password for any user created by an admin is the user's last name

## Installation
- Clone the repository
- Create a virtual environment `python3 -m venv venv` or with `virtualenv venv`
- Install the requirements `pip install -r requirements.txt`
- Set the flask app using `set FLASK_APP='api/'`
- In the terminal run `flask shell`
- In the shell create the database using `db.create_all()`
- Run the application `python3 runserver.py`



## Usage
- To run the application, run `python3 runserver.py`
- To run the tests, run `python3 -m pytest`


## Contributing
- Fork the repository
- Clone the repository
- Create a virtual environment `python3 -m venv venv` or with `virtualenv venv`
- Install the requirements `pip install -r requirements.txt`
- Create a new branch `git checkout -b new-branch`
- Make your changes
- Commit your changes `git commit -m "commit message"`
- Push to the branch `git push origin new-branch`
- Create a pull request

## Live Demo
- [PythonAnywhere](https://ridwan993.pythonanywhere.com/)

## Upcoming Features
- Add more tests 
- Add more features to the API
- Add more documentation to the API
- Update to Postgres database instead of SQLite for production

## License

[MIT](https://github.com/temitope3201/ridwan-student-management/blob/main/LICENSE)
