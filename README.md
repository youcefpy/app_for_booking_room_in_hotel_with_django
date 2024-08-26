 Hotelier - Hotel Reservation App

**Hotelier** is a web application designed to streamline the process of reserving a room in a hotel. This app offers a user-friendly interface, robust data storage, secure authentication, and a variety of payment options to provide a seamless experience for both hotel guests and administrators.

## Features

- **User-Friendly Interface**: Easy to navigate, with a clean and responsive design.
- **Web Application**: Accessible from any device with an internet connection.
- **Data Storage with PostgreSQL**: Reliable and efficient database management.
- **Authentication System**: Secure login and registration powered by Django Allauth.
- **Friendly Reservation Form**: Simple and intuitive form for booking a room.
- **PDF File Generation**: Automatically generates a PDF file of the reservation details.
- **Payment Options**: Pay with PayPal or upon arrival at the hotel.

## Application Screenshots

_Add screenshots of the application here._

## Demo

_Add a link to the demo video here._

## Setup and Installation

1. **Install Dependencies**: 
    ```bash
    pipenv install shell
    ```

2. **Database Setup**: Create a PostgreSQL database and link it to the app in `settings.py`.

3. **Migrations**: Run the following command :
    ```bash
    py manage.py makemigrations
    ```
4. **Migrate**: Run the following command for migrate:
    ```bash
    py manage.py migrate
    ```
5. **Run the server**: Run the following command for runing the localserver (localhost):
    ```bash
    py manage.py runserver
    ```
## Redis For lanching the celery and make the task

1. **Run the redis Server**: you should install redis-server and run the command : 
    ```bash
    redis-server.exe
    ```

## Run celery worker and beat

1. **Run the celery worker**: Run the following command for celery worker:
    ```bash
    celery -A bookingProject worker -l info --pool=solo
    ```

2. **Run the celery beat**: Run the following command for celery beat:
    ```bash
    celery -A bookingProject beat -l info
    ```

3. **Run the celery inspect**: Run the celery instecy for checking if the task is linked to the celery

    ```bash
    celery -A bookingProject inspect registered
    ```