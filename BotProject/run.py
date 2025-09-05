# from booking.booking_module import Booking
# import time

# with Booking() as bot:
#     bot.land_first_page()
#     bot.change_currency('EGP')
#     # bot.select_place_to_go('Cairo')
#     # bot.select_dates(check_in_date="2025-12-20", check_out_date="2025-12-30")
#     bot.seat_booking(5, 2, 3)
#     time.sleep(10)

from booking.booking_module import get_plus_button

get_plus_button()