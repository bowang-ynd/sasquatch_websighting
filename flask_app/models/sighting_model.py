from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATABASE
from flask import flash
from flask_app.models.skeptic_model import Skeptic

class Sighting:

    # class constructor
    def __init__(self, data):
        self.id = data['id']
        self.location = data['location']
        self.description = data['description']
        self.date_sighted = data['date_sighted']
        self.sasquatch_num = data['sasquatch_num']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.owner_id = data['owner_id']

        # additionally declare a owner_name for each sighting
        self.owner_name = ""

        # additionally declare a list of skeptical users for each sighting
        self.skeptics = []

    #? ==================== CREATE ====================
    @classmethod
    def create(cls, data):
        query = """
            INSERT INTO sightings (location, description, date_sighted, sasquatch_num ,owner_id)
            VALUES (%(location)s, %(description)s, %(date_sighted)s, %(sasquatch_num)s, %(owner_id)s);
        """

        connectToMySQL(DATABASE).query_db(query, data)
    
    #? ==================== READ ====================
    @classmethod
    def get_one_sighting(cls, data):
        query = """
            SELECT * FROM sightings 
            JOIN users ON users.id = sightings.owner_id
            WHERE sightings.id = %(id)s;
        """

        results = connectToMySQL(DATABASE).query_db(query, data)

        # if no sightings found, return false
        if (not results) or (len(results) <= 0):
            return False
        
        # else instantiate and return the found sighting 
        print(results)
        found_sighting = cls(results[0])

        # set owner_name for this sighting
        owner_name = results[0]['first_name'] + " " + results[0]['last_name']
        found_sighting.set_owener_name(owner_name)

        # find skeptics num on this sighting
        found_sighting.set_skeptics()

        return found_sighting
    
    @classmethod # get all existing sightings
    def get_all(cls):
        query = """
            SELECT * FROM sightings
            JOIN users ON users.id = sightings.owner_id;
        """

        results = connectToMySQL(DATABASE).query_db(query)

        # if no sightings found, return false
        if (not results) or (len(results) <= 0):
            return False
        # else instantiate and return all found sightings 
        found_sightings = []

        for result in results:
            sighting = cls(result)

            # set owner_name for this sighting
            owner_name = result['first_name'] + " " + result['last_name']
            sighting.set_owener_name(owner_name)

            # find skeptics num on this sighting
            sighting.set_skeptics()

            found_sightings.append(sighting)
        return found_sightings
    
    #? ==================== UPDATE ====================
    @classmethod
    def edit_sighting_with_id(cls, data):
        query = """
            UPDATE sightings
            SET location = %(location)s, description = %(description)s, date_sighted = %(date_sighted)s, sasquatch_num = %(sasquatch_num)s
            WHERE sightings.id = %(id)s;
        """

        connectToMySQL(DATABASE).query_db(query, data)
    
    # An instance method to set each instance's owner_name
    def set_owener_name(self, name):
        self.owner_name = name
    
    # An instance method to set each instance's skeptics
    def set_skeptics(self):
        self.skeptics = Skeptic.get_skeptics_one_sighting({'id' : self.id})

    # An instance method to update each instance's skeptics list
    def update_skeptics(self, bool, name):
        if bool:
            self.skeptics.append(name)
        else:
            self.skeptics.remove(name)
    
    def clear_skeptics(self):
        self.skeptics.clear()

    #? ==================== DELETE ====================
    @classmethod
    def delete_sighting_with_id(cls, data):
        query = """
            DELETE FROM sightings WHERE sightings.id = %(id)s;
        """

        connectToMySQL(DATABASE).query_db(query, data)

    #? ==================== VALIDATION ====================
    @staticmethod
    def validate_sighting(data):
        is_valid = True

        #! ========== Checking LOCATION ==========
        # Name should not be void
        if len(data['location']) == 0:
            flash("Location should not be blank!", "sighting")
            is_valid = False

        #! ========== Checking DESCRIPTION ==========
        # Name should not be void
        if len(data['description']) == 0:
            flash("Please talk about what happened!", "sighting")
            is_valid = False

        #! ========== Checking DATE ==========
        # DATE should not be empty
        if len(data['date_sighted']) == 0:
            flash("Please select date of sighting", "sighting")
            is_valid = False

        #! ========== Checking SASQUATCH_NUM ==========
        # SASQUATCH_NUM should not be empty
        if len(data['sasquatch_num']) == 0:
            flash("Please specify the number of sasquatches sighted", "sighting")
            is_valid = False
        
        return is_valid