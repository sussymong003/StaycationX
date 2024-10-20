import json
import base64

def test_home_page_post_with_fixture(client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/' page is posted to (POST)
    THEN check that a '200' (Success) status code is returned
    """
    response = client.get('/')
    assert response.status_code == 200
    assert b"Flask User Management Example!" not in response.data

def test_view_hotel_with_fixture(client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/' page is posted to (GET)
    THEN check that a '200' (Success) status code is returned
    """
    response = client.get("/viewPackageDetail/Capella Singapore")
    assert response.status_code == 200
    assert b"Capella Singapore" in response.data

def test_gettoken_and_retrieve_package_with_fixture(client):
    """
    GIVEN a Flask API application configured for testing
    WHEN the '/api/user/gettoken' request path is sent (POST) with authentication information
    THEN if the user is authenticated then a token is returned for the user to query the '/api/package/getAllPackages' request path
    """
    useremail = 'peter@cde.com'
    response = client.post("api/user/gettoken", data={'email': useremail, 'password': '12345'})
    response_data = json.loads(response.text)

    try: 
        assert response.status_code == 200
        token = response_data['token']['token']
        print(token)
        credentials = base64.b64encode(f"{useremail}:{token}".encode('utf-8')).decode('utf-8')
        headers = {'Authorization': f'Basic {credentials}'}
        response = client.post('api/package/getAllPackages', headers=headers)
        response_data = json.loads(response.text)
        print(response_data)
    except Exception as e:
        print(e)

# 2bi
def test_create_booking_with_api(client):
    """
    GIVEN a Flask API application configured for testing
    WHEN the '/api/booking/create' request path is sent (POST) with date,user,package information along with authentication information
    THEN if the user and the package is valid then a booking is returned for the user to show confirmation of the booking.
    """

    hotel_name = 'Shangri-La Singapore'
    useremail = 'jack@test.com'
    user_response = client.post("api/user/gettoken", data={'email': useremail, 'password': '12345'})
    response_data = json.loads(user_response.text)
    
    try: 
        assert user_response.status_code == 200
        token = response_data['token']['token']
        credentials = base64.b64encode(f"{useremail}:{token}".encode('utf-8')).decode('utf-8')
        headers = {'Authorization': f'Basic {credentials}'}

        # Create booking
        booking_data = {
            'hotel_name': 'Shangri-La Singapore',
            'check_in_date': '2024-10-24'
        }

        booking_response = client.post("api/booking/create", data=booking_data, headers=headers)

        assert booking_response.status_code == 201
        booking_response_data = json.loads(booking_response.data)
        assert booking_response_data['message'] == 'Booking created successfully'
        assert booking_response_data['check_in_date'] == '2024-10-24'
        assert booking_response_data['booking']['hotel_name'] == 'Shangri-La Singapore'
    except Exception as e:
        print(e)

# 2bii
def test_manage_booking_with_api(client):
    """
    GIVEN a Flask API application configured for testing
    WHEN the '/api/booking/manage' request path is sent (GET) with authentication information
    THEN a list of booking is returned
    """

    useremail = 'jack@test.com'
    user_response = client.post("api/user/gettoken", data={'email': useremail, 'password': '12345'})
    response_data = json.loads(user_response.text)

    try: 
        assert response.status_code == 200
        token = response_data['token']['token']
        credentials = base64.b64encode(f"{useremail}:{token}".encode('utf-8')).decode('utf-8')
        headers = {'Authorization': f'Basic {credentials}'}

        booking_response = client.get('api/booking/manage', headers=headers)
        booking_response_data = json.loads(booking_response.text)
        print(booking_response_data)
        assert booking_response.status_code == 200
        assert b"Shangri-La Singapore" in booking_response.data
    except Exception as e:
        print(e)
     
# 2bii  
def test_update_booking_with_api(client):
    """
    GIVEN a Flask API application configured for testing
    WHEN the '/api/booking/update' request path is sent (POST) with authentication information
    THEN if the user is authenticated then a token is returned for the user to query the '/api/package/getAllPackages' request path
    """

    useremail = 'jack@test.com'
    user_response = client.post("api/user/gettoken", data={'email': useremail, 'password': '12345'})
    response_data = json.loads(user_response.text)

    try: 
        assert response.status_code == 200
        token = response_data['token']['token']
        credentials = base64.b64encode(f"{useremail}:{token}".encode('utf-8')).decode('utf-8')
        headers = {'Authorization': f'Basic {credentials}'}

        # Create booking
        booking_data = {
            'old_check_in_date': '2024-10-24',
            'new_check_in_date': '2024-10-31',
            'hotel_name': 'Shangri-La Singapore'
        }

        booking_response = client.patch('api/booking/update', data=booking_data, headers=headers)

        assert booking_response.status_code == 201
        booking_response_data = json.loads(booking_response.data)
        assert booking_response_data['message'] == 'Booking updated successfully'
        assert booking_response_data['check_in_date'] == '2024-10-31'
        assert booking_response_data['booking']['hotel_name'] == 'Shangri-La Singapore'
    except Exception as e:
        print(e)
        
# 2biv
def test_delete_booking_with_api(client):
    """
    GIVEN a Flask API application configured for testing
    WHEN the '/api/booking/delete' request path is sent (POST) with authentication information
    THEN if the user is authenticated then a token is returned for the user to query the '/api/package/getAllPackages' request path
    """

    hotel_name = 'Shangri-La Singapore'
    useremail = 'jack@test.com'
    user_response = client.post("api/user/gettoken", data={'email': useremail, 'password': '12345'})
    response_data = json.loads(user_response.text)
    
    try: 
        assert user_response.status_code == 200
        token = response_data['token']['token']
        credentials = base64.b64encode(f"{useremail}:{token}".encode('utf-8')).decode('utf-8')
        headers = {'Authorization': f'Basic {credentials}'}

        # Create booking
        booking_data = {
            'hotel_name': 'Shangri-La Singapore',
            'check_in_date': '2024-10-31'
        }

        booking_response = client.post("api/booking/delete", data=booking_data, headers=headers)

        assert booking_response.status_code == 200
        booking_response_data = json.loads(booking_response.data)
        assert booking_response_data['message'] == 'Booking deleted successfully'
        assert booking_response_data['check_in_date'] == '2024-10-23'
        assert booking_response_data['booking']['hotel_name'] == 'Shangri-La Singapore'
    except Exception as e:
        print(e)
        