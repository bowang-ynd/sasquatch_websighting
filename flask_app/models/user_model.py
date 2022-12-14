from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATABASE, bcrypt
from flask import flash
from flask_app.models.skeptic_model import Skeptic

import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User:

    #? class constructor
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

        # mannually declare a boolean to set if a user is skeptical
        self.is_skeptical = False

    #? ==================== CREATE ====================
    @classmethod
    def register(cls, data):
        query = """
            INSERT INTO users (first_name, last_name, email, password)
            VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s);
        """
        return connectToMySQL(DATABASE).query_db(query, data)

    #? ==================== READ ====================
    @classmethod
    def get_by_id(cls, data):
        query = """
            SELECT * FROM users WHERE users.id = %(id)s;
        """

        results = connectToMySQL(DATABASE).query_db(query, data)

        if results:
            found_user = User(results[0])
            return found_user
        else: 
            return False

    @classmethod
    def get_by_email(cls, data):
        query = """
            SELECT * FROM users WHERE users.email = %(email)s;
        """

        results = connectToMySQL(DATABASE).query_db(query, data)

        if results and len(results) > 0:
            found_user = User(results[0])
            return found_user
        else: 
            return False
        
    # An instance method to get user's full name
    def get_name(self):
        return self.first_name + " " + self.last_name

    #? ==================== UPDATE ====================    
    # An instance method to check if user is skeptical about a specific sighting
    def set_skeptical(self, data):
        name_lst = Skeptic.get_skeptics_one_sighting(data)
        
        if self.get_name() in name_lst:
            self.is_skeptical = True
        else:
            self.is_skeptical = False

    # an instance method to change user's skeptical bool value
    def change_skeptical(self, bool):
        if bool == True:
            self.is_skeptical = False
        else:
            self.is_skeptical = True

    #? ==================== VALIDATION ====================
    @classmethod
    def validate_login(cls, data):

        #! ========== Checking if EMAIL or PASSWORD are empty ==========
        if (len(data['email']) == 0) or (len(data['password']) == 0):
            flash("Email or Password should not be blank!", "login")
            return False

        #! ========== Checking if EMAIL or PASSWORD are correct ==========
        # first checks if the input email exists in database
        found_user = cls.get_by_email(data)

        # if no users associated with the given email address exist in database, return False
        if not found_user:
            flash("Invalid Email or Password!", "login")
            return False
        # if the user's password does not match that of the associated email address, return False
        elif not bcrypt.check_password_hash(found_user.password, data['password']):
            flash("Invalid Email or Password!", "login")
            return False
        
        # if the login info are valid, login the user
        return found_user

    @staticmethod
    def validate_register(data):
        is_valid = True

        #! ==================== Checking NAMES ====================
        if len(data['first_name']) == 0 or len(data['last_name']) == 0:
            flash("Please input Name", "register")
            is_valid = False

        #* names should have at least 2 characters
        elif (len(data['first_name']) < 2) or (len(data['last_name']) < 2):
            flash("First Name or Last Name should have at least two letters", "register")
            is_valid = False

        #*  names should only contain letters
        elif (not data['first_name'].isalpha()) or (not data['last_name'].isalpha()):
            flash("First Name or Last Name should only contain letters", "register")
            is_valid = False
        
        #! ==================== Checking EMAIL ====================
        if len(data['email']) == 0:
            flash("Please input Email", "register")
            is_valid = False

        #* Email should not be registered already
        elif User.get_by_email({'email' : data['email']}):
            flash("Email already registered", "register")
            is_valid = False

        #* Email should match pattern
        elif not EMAIL_REGEX.match(data['email']):
            flash("Please input a proper email address", "register")
            is_valid = False

        #! ==================== Checking PASSWORD ====================
        if len(data['password']) == 0:
            flash("Please input Password", "register")
            is_valid = False

        #* Password should have at least 8 characters
        elif len(data['password']) < 8:
            flash("Your password should have at least 8 characters", "register")
            is_valid = False

        #* Password should match Confirm Password
        elif data['password'] != data['confirm_password']:
            flash("Your confirmed password does not match your password", "register")
            is_valid = False

        return is_valid


