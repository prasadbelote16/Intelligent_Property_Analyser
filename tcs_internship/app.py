from flask import Flask, render_template, request, redirect, url_for, flash,session
import mysql.connector
import os
import pickle
secret_key = os.urandom(24)

app = Flask(__name__)
# app.secret_key = "your_secret_key"
app.secret_key = secret_key


model=pickle.load(open("model.pkl","rb"))

# MySQL Configuration
db_config = {
    "host": "localhost",
    "user": "root",
    "password": "Prasad@123",
    "database": "demo"
}

# Function to establish a database connection
def get_db_connection():
    return mysql.connector.connect(**db_config)

# Routes
@app.route('/')
def index():
    return render_template('index.html')

# @app.route('/login', methods=['POST'])
# def login():
#     username = request.form['username']
#     password = request.form['password']

#     connection = get_db_connection()
#     cursor = connection.cursor()

#     cursor.execute("SELECT * FROM users_data WHERE username = %s AND password = %s", (username, password))
#     user = cursor.fetchone()

#     cursor.close()
#     connection.close()

#     if user:
#         session['authenticated'] = True
#         flash("Login successful!", 'success')
#         return redirect(url_for('index'))
#     else:
#         flash("Login failed. Please check your username and password.", 'error')
#         return render_template('signup.html')


# @app.route('/signup', methods=['POST'])
# def signup():
#     username = request.form['username']
#     email = request.form['email']
#     contact = request.form['contact']
#     address = request.form['address']
#     password = request.form['password']

#     connection = get_db_connection()
#     cursor = connection.cursor()

#     try:
#         cursor.execute("INSERT INTO users_data (username, email, contact, address, password) VALUES (%s, %s, %s, %s, %s)",
#                        (username, email, contact, address,password))
#         connection.commit()
#     except mysql.connector.Error as err:
#         print("Error:", err)
#         connection.rollback()
#         flash("Signup failed. Please try again.", 'error')
#         print("MySQL Error:", err.msg)  # Print the error message
#         print("MySQL Error Code:", err.errno)  # Print the error code

    
#     cursor.close()
#     connection.close()

#     return redirect(url_for('login'))


@app.route('/predict', methods=['GET', 'POST'])
def predict():
    # Retrieve form data
    area = float(request.form['area'])
    bedrooms = int(request.form['bedrooms'])
    bathrooms = int(request.form['bathrooms'])
    stories = int(request.form['stories'])
    mainroad = int(request.form['mainroad'])
    parking = int(request.form['parking'])
    furnishingstatus = int(request.form['furnishingstatus'])
    price_per_sqft = float(request.form['price_per_sqft'])

    # Perform prediction
    prediction = model.predict([[area, bedrooms, bathrooms, stories, mainroad, parking, furnishingstatus, price_per_sqft]])
    output = round(prediction[0], 2)
    output = float(output) 

    # Save input data and prediction to the database
    connection = get_db_connection()
    cursor = connection.cursor()

    try:
        cursor.execute("INSERT INTO prediction_data (area, bedrooms, bathrooms, stories, mainroad, parking, furnishingstatus, Price_per_sqft,price) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
                       (area, bedrooms, bathrooms, stories, mainroad, parking, furnishingstatus, price_per_sqft, output))
        connection.commit()
    except mysql.connector.Error as err:
        print("Error:", err)
        connection.rollback()
        print("MySQL Error:", err.msg)  # Print the error message
        print("MySQL Error Code:", err.errno)  # Print the error code

    cursor.close()
    connection.close()

    return render_template('index.html', prediction_text=f'Total Price of house is :{output}/-')


if __name__ == '__main__':
    app.run(debug=True)
    