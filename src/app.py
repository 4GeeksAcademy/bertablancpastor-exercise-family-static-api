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
    
    if members:
        response_body = {
            "hello": "world",
            "family": members
        }
        return jsonify(response_body), 200
    else:
        response_body = {
            "msg error": "There is no members"
        }
        return jsonify(response_body), 404

#2/ GET ONE MEMBER or EDIT ONE MEMBER
@app.route('/member/<int:member_id>', methods=['GET', 'PUT'])
def handle_get_put_member(member_id):

    if request.method == 'GET':
        member = jackson_family.get_member(member_id)
        if member is not None:
            response_body = {
            "member": member
            }
            return jsonify(response_body), 200
        else:
            response_body = {
            "msg error": "Member not found"
        }
        return jsonify(response_body), 404
      
    elif request.method == 'PUT':
        request_body = request.get_json(force=True)
        member = jackson_family.get_member(member_id)
        if member is not None:
            updated_member = {
            "id": member_id,
            "first_name": request_body["first_name"],
            "last_name": jackson_family.last_name,
            "age": request_body["age"],
            "lucky_numbers": request_body["lucky_numbers"]
            }
            jackson_family.update_member(member_id, updated_member)
            response_body = {
                "msg": "Update member"
            }
            return jsonify(response_body), 200
        else:
            response_body = {
            "msg error": "Member not found"
        }
        return jsonify(response_body), 404
    

#3/CREATE ONE MEMBER
@app.route('/members/', methods=['POST'])
def handle_create():
    
    request_body = request.get_json(force=True)
    if "last_name" not in request_body:
        response_body = {
            "msg error": "Incomplete data"
        }
        return jsonify(response_body), 404
    else:
        jackson_family.add_member(request_body)
        
        response_body = {
        "msg": "Member created"
        }
        return jsonify(response_body), 200


#4/ DELETE ONE MEMBER
@app.route('/delete/<int:member_id>', methods=['DELETE'])
def handle_delete(member_id):

    if jackson_family.delete_member(member_id):
        response_body = {
        "msg": "Member delete"
        }
        
        return jsonify(response_body), 200
    else:
        response_body = {
            "msg error": "Member not found"
        }
        return jsonify(response_body), 404


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
