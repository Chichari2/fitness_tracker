# Fitness Tracker Application

Fitness Tracker is a Python-based application designed to track fitness activities and goals. It allows users to register, log in, create activities such as running or swimming, and monitor their progress toward personal goals.

## Features

- **User Registration & Authentication**: Securely register users and log them in using JWT tokens.
- **Track Activities**: Log activities like running, swimming, with details such as duration, distance, and time.
- **Set Goals**: Users can create fitness goals and track their progress.
- **Connect Activities with Goals**: Activities can be linked to specific goals, providing automatic progress updates.

## Table of Contents

1. [Installation](#installation)
2. [Usage](#usage)
   - [Register a User](#register-a-user)
   - [Log In](#log-in)
   - [Create an Activity](#create-an-activity)
   - [Set a Goal](#set-a-goal)
3. [API Endpoints](#api-endpoints)
4. [Contributing](#contributing)
5. [License](#license)

---

## Installation

To set up the project locally, follow these steps:

1. Clone the repository:
   ```bash
   git clone https://github.com/YourUsername/fitness_tracker.git
   cd fitness_tracker

2. Create and activate a virtual environment:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   
4. Set up the database:
   ```bash
   flask db init
   flask db migrate
   flask db upgrade
   
5. Run the application:
   ```bash
   flask run
   
## Usage

### **Register a User**

Send a POST request to `/api/register` with the following JSON body:
   ```json
   {
     "username": "your_username",
     "email": "your_email@example.com",
     "password": "your_password"
   }
   ```
## Log In
Send a POST request to /api/login with the following JSON body:

   ```json
   {
      "email": "your_email@example.com",
      "password": "your_password"
   }
   ```
On success, you'll receive a JWT token to authenticate further requests.

## Create an Activity
After logging in, use the token to create an activity by sending a POST request to /api/users/<user_id>/activities:

   ```json
   {
      "activity_type": "running",
      "duration_seconds": 1800,
      "distance_meters": 5000,
      "start_date": "2024-10-14T10:00:00"
   }
   ```
## Set a Goal
To create a goal, send a POST request to /api/users/<user_id>/goals:

   ```json
   {
      "name": "Run 10 km",
      "value": 10000,
      "start_date": "2024-10-14",
      "end_date": "2024-11-14"
   }
   ```

## API Endpoints

- **Register a new user**
  - `POST /api/register`
  - Description: Creates a new user account by providing a username, email, and password.

- **Log in and retrieve a JWT token**
  - `POST /api/login`
  - Description: Logs in with email and password, returns a JWT token to authenticate further requests.

- **Create a new activity**
  - `POST /api/users/<user_id>/activities`
  - Description: Creates a new activity for a specific user. You need to provide details such as activity type, duration, and start date.

- **Retrieve all activities for the user**
  - `GET /api/users/<user_id>/activities`
  - Description: Returns all activities created by the user.

- **Create a new goal**
  - `POST /api/users/<user_id>/goals`
  - Description: Allows the user to set a new goal with a name, target value, and start/end dates.

- **Retrieve all goals for the user**
  - `GET /api/users/<user_id>/goals`
  - Description: Fetches all goals set by the user.


## Contributing

We welcome contributions! To contribute, follow these steps:

1. **Fork the repository**  
   - Go to the repository page and click the "Fork" button.

2. **Create a new branch**  
   - Run the following command:  
     ```bash
     git checkout -b feature-branch-name
     ```

3. **Make your changes**  
   - Implement your changes or new features.

4. **Commit your changes**  
   - Run the following command:  
     ```bash
     git commit -m 'Add some feature'
     ```

5. **Push to the branch**  
   - Run the following command:  
     ```bash
     git push origin feature-branch-name
     ```

6. **Submit a pull request**  
   - Open a pull request to the main repository, describing your changes.

---

## License

This project is licensed under the **MIT License**. You are free to use, modify, and distribute the code under the terms of the license.

For more details, check the [LICENSE](LICENSE) file in the repository.
