from abc import ABC, abstractmethod

class Transport(ABC):
    def __init__(self, transport_id, capacity):
        self.id = transport_id
        self.capacity = capacity
        self.booked_seats = set()

    def book_seat(self, seat_number):
        if 1 <= seat_number <= self.capacity and seat_number not in self.booked_seats:
            self.booked_seats.add(seat_number)

    def get_available_seats(self):
        return [seat for seat in range(1, self.capacity + 1) if seat not in self.booked_seats]

    @abstractmethod
    def get_info(self):
        pass

    def __str__(self):
        return (f"{self.__class__.__name__} №{self.id}: мест {self.capacity}, "
                f"свободно {len(self.get_available_seats())} мест")

class Bus(Transport):
    def __init__(self, transport_id, capacity, itinerary):
        super().__init__(transport_id, capacity)
        self.itinerary = itinerary

    def get_info(self):
        return f"Автобус {self.id}, {self.capacity} мест, маршрут: {self.itinerary}"

class Train(Transport):
    def __init__(self, transport_id, capacity, wagon):
        super().__init__(transport_id, capacity)
        self.wagon = wagon

    def get_info(self):
        return f"Поезд {self.id}, {self.capacity} мест, вагоны: {self.wagon}"

class Plane(Transport):
    def __init__(self, transport_id, capacity, model):
        super().__init__(transport_id, capacity)
        self.model = model

    def get_info(self):
        return f"Самолёт {self.id}, {self.capacity} мест, модель: {self.model}"

class Passenger:
    def __init__(self, name, passport_number):
        self.name = name
        self.passport_number = passport_number

    def __str__(self):
        return f"Пассажир {self.name}, паспорт: {self.passport_number}"


class BookingSystem:
    def __init__(self):
        self.transports = {}
        self.bookings = []

    def add_transport(self, transport):
        self.transports[transport.id] = transport

    def make_booking(self, passenger, transport_id, seat_number):
        transport = self.transports.get(transport_id)
        if not transport:
            return f"Такой ID {transport_id} не найден"
        if seat_number not in transport.get_available_seats():
            return f"Место {seat_number} уже забронировано или недоступно"

        booking = Booking(passenger, transport, seat_number)
        transport.book_seat(seat_number)
        self.bookings.append(booking)
        return booking.confirm()

    def list_bookings(self):
        return [str(booking) for booking in self.bookings]


def main_menu():
    system = BookingSystem()

    while True:
        print("\n1. Добавить транспорт")
        print("2. Забронировать")
        print("3. Показ бронирования")
        print("0. Выход")

        choice = input("Выберите: ")

        if choice == "1":
            transport_type = input("Тип транспорта (Bus, Train, Plane): ")
            transport_id = input("ID транспорта: ")
            capacity = int(input("Мест: "))

            if transport_type.lower() == "bus":
                itinerary = input("Маршрут: ")
                transport = Bus(transport_id, capacity, itinerary)
            elif transport_type.lower() == "train":
                wagons = int(input("Вагоны: "))
                transport = Train(transport_id, capacity, wagons)
            elif transport_type.lower() == "plane":
                model = input("Модель: ")
                transport = Plane(transport_id, capacity, model)
            else:
                print("Ошибка, не найден тип транспорта")
                continue

            system.add_transport(transport)
            print(f"{transport_type} №{transport_id} добавлен")

        elif choice == "2":
            passenger_name = input("Имя: ")
            passport_number = input("Паспорт: ")
            transport_id = input("ID транспорта: ")
            seat_number = int(input("Место: "))
            passenger = Passenger(passenger_name, passport_number)
            print(system.make_booking(passenger, transport_id, seat_number))

        elif choice == "3":
            print("\nБронирования:")
            for booking in system.list_bookings():
                print(booking)

        elif choice == "0":
            break

main_menu()













