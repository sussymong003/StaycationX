from app.models.users import User
from app.models.package import Package
from app.models.book import Booking
from werkzeug.security import generate_password_hash
from datetime import date
import unittest

def test_new_user():
    """
    GIVEN a User model
    WHEN a new User is created
    THEN check the email, password_hashed, authenticated, and active fields are defined correctly
    """
    hashpass = generate_password_hash("12345", method='sha256')
    user = User.createUser(email="jack@fgh.com",password=hashpass, name="Jack Chen")
    assert user.email == 'jack@fgh.com'
    assert user.password == hashpass

class test_new_user_methods(unittest.TestCase):
    
    def test_create_user(self):
        """
        GIVEN a User model
        WHEN a new User is created
        THEN check the email, password_hashed, authenticated, and active fields are defined correctly
        """
        hashpass = generate_password_hash("12345", method='sha256')
        user = User.createUser(email="jack@fgh.com", password=hashpass, name="Jack Chen")
        self.assertEqual(user.email, 'jack@fgh.com')
        self.assertEqual(user.password, hashpass)

class test_booking_methods(unittest.TestCase):

    # 3bi
    def test_create_booking(self):
        """
        GIVEN a Booking model
        WHEN a new Booking is created
        THEN check that the check-in date, user, and package are correctly assigned
        """
        check_in_date = '2024-10-23'
        test_user = User.getUser(email='jakek@test.com')
        test_package = Package.getPackage(hotel_name='Shangri-La Singapore')
        # Create booking
        booking = Booking.createBooking(check_in_date, test_user, test_package)
        
        # Validate the booking details
        self.assertEqual(booking.check_in_date, '2024-10-23')
        self.assertEqual(booking.customer.email, 'jake@test.com')
        self.assertEqual(booking.package.hotel_name, 'Shangri-La Singapore')

    # 3bii
    def test_manage_booking(self):
        """
        GIVEN a Booking model
        WHEN getting a Booking list
        THEN check that the hotel is in the list being pulled
        """
        from_date = date.today()+timedelta(days = -2000)
        test_user = User.getUser(email='jake@test.com')
        # Get booking
        bookingList = Booking.getUserBookingsFromDate(test_user)
        
        # Validate the booking details
        assert b"Shangri-La Singapore" in bookingList

    # 3biii
    def test_update_booking(self):
        """
        GIVEN a Booking model
        WHEN updating a Booking
        THEN check that the check-in date, user, and package are correctly updated
        """

        old_check_in_date = '2024-10-24'
        new_check_in_date = '2024-10-31'
        test_user = User.getUser(email='jake@test.com')
        # Get booking
        booking = Booking.updateBooking(old_check_in_date, new_check_in_date, test_user, 'Shangri-La Singapore')

        self.assertEqual(booking.check_in_date, '2024-10-31')
        self.assertEqual(booking.customer.email, 'jake@test.com')
        self.assertEqual(booking.package.hotel_name, 'Shangri-La Singapore')

    # 3biv
    def test_delete_booking(self):
        """
        GIVEN a Booking model
        WHEN deleting a Booking
        THEN check that the check-in date, user, and package are correctly deleted
        """

        check_in_date = '2024-10-31'
        test_user = User.getUser(email='jake@test.com')
        # Get booking
        booking = Booking.deleteBooking(old_check_in_date, new_check_in_date, test_user, 'Shangri-La Singapore')

        self.assertEqual(booking.check_in_date, '2024-10-31')
        self.assertEqual(booking.customer.email, 'jake@test.com')
        self.assertEqual(booking.package.hotel_name, 'Shangri-La Singapore')
