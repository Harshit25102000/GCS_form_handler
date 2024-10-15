import re
from flask import jsonify, make_response



def return_error(error="SOMETHING_WENT_WRONG", message="Error", data={}, code=200):
    return make_response(jsonify({"success": False, "error": error, "message": message, "data": data}), 401)


def return_success(data={}, status="SUCCESS", code=200):
    if isinstance(data, (dict, list)):
        if isinstance(data, (list)):
            l_data = {}
            l_data['status'] = status
            l_data['data'] = data
            return jsonify({"success": True, "data": l_data})
        if data.get('status', False):
            return jsonify({"success": True, "data": data})
        else:
            data['status'] = status
            return jsonify({"success": True, "data": data})
    else:
        raise Exception(f'data obj must be list or dict but got {type(data)}')

regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
def valid_email(email):
    try:
        if(re.fullmatch(regex, email)):
            return True
        else:
            return False
    except:
        return False

def read_credentials_from_file(file_path):
    with open(file_path, 'r') as file:
        email = file.readline().strip()
        password = file.readline().strip()
    return email, password