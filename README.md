# Hotelier - Hotel Reservation App

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
0. **Install pipenv**: For installing the pipenv use this command : 
    ```bash
    pip install pipenv
    ```
1. **Activate the virtual envirement**: Use the folowing command :
    ```bash
    pipenv shell
    ``` 
2. **Install the requirements**: Use this command for installing the requirements of the project:
    ```bash
    pipenv install -r requirements.txt
    ```
    
3. **Database Setup**: Create a PostgreSQL database and link it to the app in `settings.py`.

4. **Migrations**: Create initial migrations using the following command:
    ```bash
    py manage.py makemigrations
    ```
5. **Migrate**: Apply the migrations to the database:
    ```bash
    py manage.py migrate
    ```
6. **Run the server**: Start the local server (localhost) with the command:
    ```bash
    py manage.py runserver
    ```
## Redis and Celery Setup

1. **Run the redis Server**: Install Redis and start the server using the command:
    ```bash
    redis-server.exe
    ```

2. **Run the celery worker**: Start the Celery worker to handle background tasks:
    ```bash
    celery -A bookingProject worker -l info --pool=solo
    ```

3. **Run the celery beat**: Start the Celery beat scheduler:
    ```bash
    celery -A bookingProject beat -l info
    ```

4. **Run the celery inspect**: Check if tasks are registered with Celery:

    ```bash
    celery -A bookingProject inspect registered
    ```

# Front-End Template
The front-end template is based on designs from [HTML Codex](https://htmlcodex.com). Adjustments were made to fit the needs of this project.

# Contributing
Contributions to Hotelier are welcome! If you'd like to contribute, please get in touch.

# Contact 
If you have any questions or need further assistance, feel free to contact me at: youcefboutiche28@gmail.com