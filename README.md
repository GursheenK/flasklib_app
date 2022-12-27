
# Library Management Web Application Using Flask.

The library management system is a web application created using Flask that allows the user to -

- Manage **BOOKS** along with their stocks.
- Manage **MEMBERS** and their details.
- Issue books to members.





## Features

### Books
- Add books by optionally specifying the *amount*, *name*, *author* or *ISBN*.
- View existing books and their details.
- Search for a book using the *Title* or *Author*.
- Update the details of a book.
- Delete a specific book.

### Members
- Add new members by specifying the *Name*, *Email* and *Contact*.
- View existing members and their details.
- Search for a member using the *Name*.
- Update the details of a member.
- Delete a specific member.
- View debt and clear debt after payment.

### Issues
- Issue a book to a member by specifying the number of *days* ( default = 7 ).
- Issue a book return from a member.
- Issue warning if member debt exceeds Rs. 500.


## Tech Stack

**Client:** HTML, CSS, JavaScript

**Server:** Flask, Flask SQLAlchemy


## Installation

#### Using Git Bash  
Clone the project.

```bash
  git clone https://github.com/GursheenK/flasklib_app.git
```

#### Alternatively, you can download the zip file by going to Code > Download Zip. After downloading, unzip the file contents. 

Go to the project directory.

```cmd
  cd flasklib_app
```

Create and activate a virtual environment.

```cmd
  python -m venv env
  env\Scripts\activate.bat
```

Install the necessary requirements.

```cmd
  pip install -r requirements.txt
```
Install wkhtmltopdf from the following link - https://wkhtmltopdf.org/downloads.html 


## Deployment

To deploy this project run

```bash
  python run.py
```

Open http://localhost:5000 inside the browser to view the application.

## Screenshots

## Login Page
![Login Screenshot](images/login.png)

Credentials 

*Username* - admin

*Password* - password

## Dashboard
![Dashboard Screenshot](images/dashboard.png)


## Books
![Books Screenshot](images/books.png)

### Searching Books

Can be searched using Title/Author.

![Books Screenshot](images/search_books.png)

### Importing Books

Can be imported using any parameters.

![Books Screenshot](images/add_books.png)

![Books Screenshot](images/add_books_success.png)

### Updating a book

![Books Screenshot](images/update_book.png)

### Deleting a book

![Books Screenshot](images/delete_book_success.png)


## Members
![Members Screenshot](images/view_members.png)

### Adding a Member

![Members Screenshot](images/add_member.png)

### Viewing Member Information

![Members Screenshot](images/member_info.png)

### Updating Member Information

![Members Screenshot](images/update_member.png)

### Deleting a Member

![Members Screenshot](images/delete_member_success.png)


## Issues

### Issuing a book to a Member
![Issues Screenshot](images/issue_book.png)

### Issuing a book return from a Member
![Issues Screenshot](images/issue_return.png)


## Reports
![Reports Screenshot](images/reports.png)

### Books Report PDF
![Reports Screenshot](images/member_reports_pdf.png)

### Members Report PDF
![Reports Screenshot](images/books_reports_pdf.png)


## Guest

Can be viewed by anyone.

### Guest View - Search
![Guest Screenshot](images/guest.png)

### Guest View - Book Information
![Guest Screenshot](images/guest_more.png)

## Documentation

[Flask Documentation](https://flask.palletsprojects.com/en/2.2.x/)

[Flask-SQLAlchemy Documentation](https://flask-sqlalchemy.palletsprojects.com/en/3.0.x/)

[WTForms Documentation](https://wtforms.readthedocs.io/en/3.0.x/)
## 🔗 Links
Live on Render - https://gursheen-flasklib-app.onrender.com/

## Authors

[@GursheenKaurAnand](https://github.com/GursheenK)

