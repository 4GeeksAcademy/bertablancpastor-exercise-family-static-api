"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# create the jackson family object
jackson_family = FamilyStructure("Jackson")

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

#1/ALL MEMBERS
@app.route('/members', methods=['GET'])
def handle_hello():

    # this is how you can use the Family datastructure by calling its methods
    members = jackson_family.get_all_members()
    response_body = {
        "hello": "world",
        "family": members
    }

    return jsonify(response_body), 200

#2/ONE MEMBER
@app.route('/member/<int:member_id>', methods=['GET'])
def handle_member(member_id):

    member = jackson_family.get_member(member_id)

    response_body = {
        "member": member
    }
    
    return jsonify(response_body), 200

#3/CREATE ONE MEMBER
@app.route('/members/', methods=['POST'])
def handle_create():
    
    request_body = request.get_json(force=True)
    jackson_family.add_member(request_body)

    response_body = {
        "msg": "Member created"
    }

    return jsonify(response_body), 200


#4/ DELETE ONE MEMBER
@app.route('/delete/<int:member_id>', methods=['DELETE'])
def handle_delete(member_id):

    jackson_family.delete_member(member_id)

    response_body = {
        "msg": "Member delete"
    }
    
    return jsonify(response_body), 200

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
