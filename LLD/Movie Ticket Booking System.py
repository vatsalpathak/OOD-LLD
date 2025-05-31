# Question:
# Design a Movie Booking System that supports:
# - Adding movies with duration
# - Scheduling multiple showtimes for each movie with seat management
# - Displaying available movies and available seats for showtimes
# - Booking seats for users, marking seats as booked, and storing bookings
# - Showing all bookings with user, movie, showtime, and seat details


import uuid
import random

class Movie:
    def __init__(self, movie_title,duration) -> None:
        self.movie_id = uuid.uuid4()
        self.movie_title = movie_title
        self.duration = duration
    
    def __str__(self):
        return f"{self.movie_title} ({self.duration} min)"


class Seat:
    def __init__(self, seat_number, is_booked= False) -> None:
        self.seat_number = seat_number
        self.is_booked = is_booked

class ShowTime:
    def __init__(self,movie,start_time) -> None:
        self.movie = movie
        self.start_time = start_time
        self.end_time = start_time + self.movie.duration
        self.seats = []

    def add_seats(self,seat):
        self.seats.append(seat)

class UserBooking:
    def __init__(self,user_name,movie,showtime,selected_seat,total_price) -> None:
        self.user_name = user_name
        self.movie = movie
        self.showtime = showtime
        self.selected_seat = selected_seat
        self.total_price =  total_price

class BookingSystem:
    def __init__(self) -> None:
        self.movie_list = []
        self.showtimes = []
        self.bookings = []
        self.price = 200

    def add_movie(self,title,duration):
        movie = Movie(title,duration)
        self.movie_list.append(movie)

    def add_showtime(self,movie,start_time,total_seats):
        showtime = ShowTime(movie,start_time)
        self.showtimes.append(showtime)
        for i in range(total_seats):
            seat_number = i + 1
            seat = Seat(seat_number)
            showtime.add_seats(seat)

    def show_available_movie(self):
        return self.movie_list
    
    def show_available_showtimes(self,movie):
        available_showtime = {}
        for showtime in self.showtimes:
            if showtime.movie.movie_id == movie.movie_id:
                available_seats = []
                for seat in showtime.seats:
                    if not seat.is_booked:
                        available_seats.append(seat)
                available_showtime[showtime] = available_seats
        return available_showtime
    
    def book_seat(self,user_name,movie,showtime,selected_seat):
        selected_seat.is_booked = True
        booking = UserBooking(user_name,movie,showtime,selected_seat,self.price)
        self.bookings.append(booking)
        print(f"{booking.user_name} booked '{booking.movie.movie_title}' "
        f"at {booking.showtime.start_time} - Seat {booking.selected_seat.seat_number}")
        return booking
    
    def show_all_bookings(self):
        for booking in self.bookings:
            print(f"{booking.user_name} → {booking.movie.movie_title} @ {booking.showtime.start_time} → Seat {booking.selected_seat.seat_number}")



if __name__ == "__main__":
    # Setup Booking System
    system = BookingSystem()

    # Add a movie
    system.add_movie("Interstellar", 180)
    movie = system.movie_list[0]  # Get the movie we just added

    # Add showtime with 5 seats
    system.add_showtime(movie, start_time=1400, total_seats=5)
    showtime = system.showtimes[0]

    # Show all available movies
    print("\nAvailable Movies:")
    for m in system.show_available_movie():
        print(f"- {m.movie_title} ({m.duration} min)")

    # Show available showtimes and seats
    print("\nShowtimes and Available Seats:")
    availability = system.show_available_showtimes(movie)
    for st, seats in availability.items():
        print(f"Showtime @ {st.start_time}:")
        for s in seats:
            print(f" - Seat {s.seat_number}")

    # Book a seat
    seat_to_book = availability[showtime][0]  # Book the first available
    booking = system.book_seat("Alice", movie, showtime, seat_to_book)

    system.show_all_bookings()