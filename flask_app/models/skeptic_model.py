from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATABASE

class Skeptic:

    # class constructor
    def __init__(self, data):
        self.id = data['id']
        self.user_id = data['user_id']
        self.sighting_id = data['sighting_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    #? ==================== CREATE ====================
    @classmethod
    def create_skeptic(cls, data):
        query = """
            INSERT INTO skeptics (user_id, sighting_id)
            VALUES (%(user_id)s, %(sighting_id)s);
        """

        connectToMySQL(DATABASE).query_db(query, data)
    
    #? ==================== READ ====================
    @classmethod # find skeptics num for one sighting
    def get_skeptics_one_sighting(cls, data):
        query = """
            SELECT * FROM sightings 
            JOIN skeptics ON sightings.id = skeptics.sighting_id
            JOIN users ON users.id = skeptics.user_id
            WHERE sightings.id = %(id)s;
        """

        results = connectToMySQL(DATABASE).query_db(query, data)

        # declare a local list to store any skeptics for this sighting
        skeptics = []
        # if no valid results returned or found, then method should return empty list skeptics
        # otherwise return the length of results
        if not results or len(results) <= 0:
            return skeptics

        # for each valid skeptic, append to skeptics list 
        for result in results:
            # set the skeptic's name
            skeptic_name = result['first_name'] + " " + result['last_name']
            skeptics.append(skeptic_name)
        return skeptics

    #? ==================== UPDATE ====================
    @classmethod
    def update_skeptics(cls, bool, user_id, sighting_id):
        # create data for later input into CREATE or DELETE methods
        data = {
            'user_id' : user_id,
            'sighting_id' : sighting_id
        }

        if bool:
            cls.create_skeptic(data)
        else:
            cls.delete_user_skeptic(data)

    #? ==================== DELETE ====================
    # delete a specific skeptic based on user_id and sighting_id
    @classmethod 
    def delete_user_skeptic(cls, data):
        query = """
            DELETE FROM skeptics WHERE user_id = %(user_id)s AND sighting_id = %(sighting_id)s;
        """

        connectToMySQL(DATABASE).query_db(query, data)
    
    # delete all skeptics based on sighting_id
    @classmethod
    def delete_sighting_skeptic(cls, data):
        query = """
            DELETE FROM skeptics WHERE sighting_id = %(id)s;
        """

        connectToMySQL(DATABASE).query_db(query, data)

