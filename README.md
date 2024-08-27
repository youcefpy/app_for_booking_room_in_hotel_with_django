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
![index-hotelier-before-auth](https://github.com/user-attachments/assets/c0cefce9-6613-4034-896c-7d8a41e3b42e)
![index-hotelier](https://github.com/user-attachments/assets/5a37d119-e70e-4856-a609-ef6ab5942ae3)
![rooms-page](https://github.com/user-attachments/assets/b4c2b01c-1948-4310-849b-ba599953d6f4)
![booking-room](https://github.com/user-attachments/assets/a5594d64-e857-4632-ad9b-2ae7a488f838)
![validation-booking](https://github.com/user-attachments/assets/92173775-93e4-441b-93ea-790bcea15d66)
![pdf-booking](https://github.com/user-attachments/assets/f14685b6-f374-4b50-bc4b-fda8b1381f0c)
![comment-room](https://github.com/user-attachments/assets/35bbde87-3555-410c-81bf-b0027460a985)
![contact-page](https://github.com/user-attachments/assets/7309c169-1b85-44cf-8505-dd181797e459)


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
