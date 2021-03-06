from app import db, login
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class Departments(db.Model): # Departments class defined, inherits from db.Model baseclass. This is the standard baseclass for defining database models in Flask-SQLAlchemy.
                             # Represents Departments table in the database schema.
    id = db.Column(db.Integer, primary_key=True) # Primary key identifier field for Departments table, type integer. Fields are created as instances of the db.Column class.
    department_name = db.Column(db.String(64), index=True, unique=True) # Field for department name, type string and max length 64.
    risk_score = db.Column(db.Integer, default=0) # Field for department risk score, type integer, default value is set to 0.
    staff_members = db.relationship('Staff', backref='department', lazy='dynamic') # One-to-many relationship expressed with relationship() function. Foreign key is
                                                                                   # defined in the Staff class definition (many end of the relationship) with the ForeignKey class.
                                                                                   # Notice uppercase 'S' for 'Staff' - this is the name of the MODEL, not table.

    def __repr__(self): # Method defines how Python should print objects of this class, useful for debugging.
        return '<Department {}>'.format(self.department_name)

class Staff(db.Model): # Staff class defined. Represents Staff table in the database schema.
    id = db.Column(db.Integer, primary_key=True) # nullable=False is implied with primary key, specifies that the field is required for a given database record
    department_id = db.Column(db.Integer, db.ForeignKey('departments.id')) # Defines foreign key field... 'departments' is the name of the database table, NOT the model (hence lowercase 'd')
    staff_name = db.Column(db.String(64), index=True, unique=False) # unique=False explicitly states that the field does not have to be unique.
    email = db.Column(db.String(120), index=True, unique=True) # unique=True states that the email field must to be unique for a given record, i.e. no two staff records can have the same email
    clicked = db.Column(db.Integer, default=0) # Field for number of test phishing email links clicked, type integer, default value is set to 0.
    submitted = db.Column(db.Integer, default=0)
    delivered = db.Column(db.Integer, default=0)
    risk_score = db.Column(db.Integer, default=0)
    latest_risk = db.Column(db.Integer, default=0)
    direction = db.Column(db.Boolean, default=False) # False = increased risk in latest performance, True = decreased risk in latest performance, where a performance is a phishing email response
    last_sent = db.Column(db.DateTime) # Field for the send datetime of the last test phishing email sent to the staff member's email, type datetime, default None.
    scheduled_emails = db.relationship('ScheduledEmails', backref='staff', lazy='dynamic') # Defines one-to-many relationship for staff-scheduled emails.
    

    def __repr__(self):
        return '<Staff {}>'.format(self.staff_name)

class ScheduledEmails(db.Model): # ScheduledEmails class defined. Represents ScheduledEmails table in the database schema.
    id = db.Column(db.Integer, primary_key=True)
    staff_id = db.Column(db.Integer, db.ForeignKey('staff.id'))
    staff_email = db.Column(db.String(120), index=True, nullable=False) # Field is not unique, as several emails can be scheduled to the same staff member.  
    template = db.Column(db.String(30), nullable=False) # Field for the template of the test phishing email to be sent.
    send_time = db.Column(db.DateTime, index=True, nullable=False) # Field to specify the time at which the email scheduled is due to be sent. The emailer script will check this datetime attribute.
    sent = db.Column(db.Boolean, default=False) # Field to identify whether or not the scheduled email has been sent, boolean type, default is set to False.

    def __repr__(self):
        return '<ScheduledEmail {}>'.format(self.staff_email)

class Admin(UserMixin, db.Model): # Admin class defined. Represents Admin table in the database schema. It is used to control system administrator logins.
                                  # Class inherits from additional UserMixin baseclass, which provides default implementations for generic attributes and methods appropriate for most user model classes.
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    def __repr__(self):
        return '<Admin {}>'.format(self.username)

    def set_password(self, password): # Implements method that generates a password hash using (by default) the SHA256 hash function. Passwords should never be stored as hardcoded strings in a database for security reasons.
        self.password_hash = generate_password_hash(password)

    def check_password(self, password): # Implements method that takes a password hash previously generated, and a password entered by a user at login, and returns True if the password entered by the user matches the hash. Otherwise, returns False. 
        return check_password_hash(self.password_hash, password)

    # An additional security measure makes it such that if the same password is hashed multiple times, different hashes will be generated each time. This makes it
    # impossible to distinguish from their hashes whether two passwords are the same.

@login.user_loader # This decorator registers the user_loader() function, which is used to reload a user's object from the user ID stored in the session.
def load_user(id):
    return Admin.query.get(int(id)) # The id Flask-Login passes to the load_user() function as an argument is a string, and hence needs to be converted to an integer for database querying.