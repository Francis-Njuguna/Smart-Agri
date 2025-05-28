# Smart Agri

A Smart Agriculture system for crop and livestock recommendations, weather, and market information, now powered by PostgreSQL.

## Prerequisites
- Python 3.8+
- PostgreSQL (download from https://www.postgresql.org/download/)

## Setup Instructions

### 1. Clone the Repository
```sh
# Clone this repository and navigate into the project directory
cd path/to/Smart-Agri
```

### 2. Install Python Dependencies
```sh
pip install -r requirements.txt
```

### 3. Set Up PostgreSQL Database
- Open **SQL Shell (psql)** or your preferred PostgreSQL client.
- Connect as the `postgres` user:
  ```sh
  psql -U postgres
  ```
- Create the database:
  ```sql
  CREATE DATABASE smart_agri;
  \q
  ```
- (Optional) Create a new user and grant privileges if you don't want to use the default `postgres` user.

### 4. Configure Database Connection
- Edit `config/database.py` and set your actual PostgreSQL password:
  ```python
  'password': 'your_actual_password'
  ```

### 5. Initialize the Database Tables
```sh
python init_db.py
```
This will create all required tables in your PostgreSQL database.

### 6. Test the Database Connection (Optional)
```sh
python test_db.py
```
This script will test the connection, insert test data, and print out the results.

### 7. Run the Application
- Start your main application as per your project (e.g., Flask, FastAPI, or other entry point):
```sh
python app.py
```
- Or, if you have a different entry point, adjust accordingly.

## Troubleshooting
- If you get `ModuleNotFoundError: No module named 'config.database'`, make sure `config/__init__.py` and `utils/__init__.py` exist.
- If you get database connection errors, check your credentials and ensure PostgreSQL is running.
- If you get duplicate key errors when running test scripts, delete the test data or use a different test value.

## Project Structure
```
Smart-Agri/
├── config/
│   ├── __init__.py
│   └── database.py
├── data/
│   └── kiambu_locations.py
├── services/
│   ├── crop_manager.py
│   ├── sms.py
│   └── ...
├── utils/
│   ├── __init__.py
│   └── db.py
├── requirements.txt
├── init_db.py
├── test_db.py
├── README.md
└── ...
```

## Contact
For any issues, please open an issue on the repository or contact the maintainer. 