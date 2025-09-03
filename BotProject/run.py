from booking.booking_module import Booking
import time

with Booking() as bot:
    bot.land_first_page()
    bot.change_currency('EGP')
    bot.select_place_to_go('Cairo')
    bot.select_dates(check_in_date="2025-09-20", check_out_date="2025-09-30")
    time.sleep(10)