from flask import jsonify, request, Blueprint
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import json

# Specific to API
from flask_httpauth import HTTPBasicAuth
from bson import json_util

# Import the models
from app.models.users import User
from app.models.package import Package
from app.models.token import UserTokens

from app.utils.api import extract_keys

api = Blueprint('api', __name__)

# This is protect the API routes using HTTP Basic Authentication
api_auth = HTTPBasicAuth()

# The API route to get a token
@api.route('/api/user/gettoken', methods=['POST'])
def api_gettoken():
    if request.method == 'POST': 

        # To handle both JSON payloads (commonly used with JavaScript or ReactJS) 
        # and form data (which can be sent from a Python script or a HTML form).
        try:
            data = request.json
            if data: # if using ReactJS
                email = data['email']
                password = data['password']
        except: # if using python
            email = request.form.get('email')
            password = request.form.get('password')

        # from OneMap: 400 - You have to enter a valid email address and valid password to generate a token.
        if not email or not password:
            return jsonify({'error': 'You have to enter a valid email address and valid password'}), 400 

        # from OneMap: 404 - User is not registered in system.
        user = User.getUser(email=email)
        if not user:
            return jsonify({'error': 'User is not registered'}), 404 

        # from OneMap: 401 - Authentication failed, please contact admin at support@onemap.gov.sg
        if not check_password_hash(user.password, password):
            return jsonify({'error': 'Authentication failed'}), 401 

        token =  UserTokens.getToken(email = email)
        
        # If token exists, return the token
        if token:
            return jsonify({'token': token}), 200

        current_datetime = datetime.now()
        datetime_str = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
        # Simulated token generation (replace with actual token logic)
        token = generate_password_hash(user.email+datetime_str, method='sha256')
        UserTokens.createToken(email = user.email, token=token)
        # Return the newly generated token
        return jsonify({'token': token}), 200

# The API route to get all packages  
@api.route('/api/package/getAllPackages', methods=['POST'])
@api_auth.login_required
def getAllPackages():
    allPackages = Package.getAllPackages()
    packages_list = [json.loads(json_util.dumps(package.to_mongo())) for package in allPackages]
    projected_list = [extract_keys(k, idx+1) for idx, k in enumerate(packages_list)]
    return jsonify({'data': projected_list}), 201

# Protected route for authorized users
@api.route('/api/protected')
@api_auth.login_required
def protected():
    return jsonify({'message': 'You are authorized to see this message'}), 201

# Part of the basic authentication
@api_auth.verify_password
def verify_password(email, token):
    user = UserTokens.getToken(email=email)
    if user and user.token==token:
        return True
    else:
        return False

# Q2ai
@booking.route('/api/booking/create', methods=['POST'])
@login_required
def create_booking():
    """
    Create a new booking for the user.
    Requires 'hotel_name' and 'check_in_date' in the form data.
    """
     try:
        data = request.json
        if data: # if using ReactJS
            hotel_name = data['hotel_name']
            check_in_date = data['check_in_date']
    except: # if using python
        hotel_name = request.form.get('hotel_name')
        check_in_date = request.form.get('check_in_date')
    
    existing_package = Package.getPackage(hotel_name=hotel_name)
    
    if current_user is None or existing_package is None:
        return jsonify({'error': 'Invalid user or package'}), 400
    
    aBooking = Booking.createBooking(check_in_date, current_user, existing_package)
    
    return jsonify({
        'message': 'Booking created successfully',
        'booking': {
            'hotel_name': aBooking.hotel_name,
            'check_in_date': aBooking.check_in_date,
            'user': aBooking.current_user.email,
            'total_cost': aBooking.current_user.total_cost
        }
    }), 201

# Q2aii
@booking.route('/api/booking/manage', methods=['GET'])
@login_required
def manage_booking():
    """
    Get all bookings for the current user.
    Query parameter 'days' can be used to specify how far back to retrieve bookings.
    """
    days = int(request.args.get('days', '-2000'))  # Default is -2000 days
    bookings = list(Booking.getUserBookingsFromDate(customer=current_user, from_date=date.today() + timedelta(days=days)))
    
    if bookings:
        bookings.sort(key=lambda b: b.check_in_date)
    
    return jsonify({
        'message': 'Bookings retrieved successfully',
        'bookings': [{'hotel_name': b.hotel_name, 'check_in_date': b.check_in_date} for b in bookings]
    }), 200

# Q2aiii
@booking.route('/api/booking/update', methods=['POST'])
@login_required
def update_booking():
    """
    Update an existing booking for the user.
    Requires 'hotel_name', 'old_check_in_date', and 'check_in_date' in the form data.
    """
    hotel_name = request.form.get("hotel_name")
    old_check_in_date = request.form.get("old_check_in_date")
    new_check_in_date = request.form.get("check_in_date")
    
    success = Booking.updateBooking(old_check_in_date, new_check_in_date, current_user, hotel_name)
    
    if success:
        return jsonify({
            'message': 'Booking updated successfully',
            'hotel_name': hotel_name,
            'new_check_in_date': new_check_in_date
        }), 200
    else:
        return jsonify({'error': 'Failed to update booking'}), 400

# Q2aiv
@booking.route('/api/booking/delete', methods=['POST'])
@login_required
def delete_booking():
    """
    Delete an existing booking for the user.
    Requires 'hotel_name' and 'check_in_date' in the form data.
    """
    hotel_name = request.form.get("hotel_name")
    check_in_date = request.form.get("check_in_date")
    
    success = Booking.deleteBooking(check_in_date, current_user, hotel_name)
    
    if success:
        return jsonify({
            'message': 'Booking deleted successfully',
            'hotel_name': hotel_name,
            'check_in_date': check_in_date
        }), 200
    else:
        return jsonify({'error': 'Failed to delete booking'}), 400
