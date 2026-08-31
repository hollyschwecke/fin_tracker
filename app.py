import os 

from flask import Flask, render_template, request, redirect, url_for, session, flash
from dotenv import load_dotenv
from werkzeug.security import generate_password_hash, check_password_hash

from database import get_connection

# load environment variables from .env file
# this allows us to keep sensitive information like database credentials and 
# secret keys out of the source code
load_dotenv()

# create Flask application
app = Flask(__name__)

# Flask uses the secret key to securely sign session data
# actual secret key is stored in the .env file and loaded into the application at runtime
app.secret_key = os.getenv('SECRET_KEY')

@app.route('/')
def home():
    ''' 
    Home page 
    If the user is logged in (i.e., "user_id" is in the session), redirect to the dashboard.
    '''
    
    # user_id in the session indicates the user is logged in
    if "user_id" in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    '''
    Register a new user account
    
    GET:
        Display the registration form.
        
    POST:
        Process the registration form submission.
        Validate the input, hash the password, and store the new user in the database.
    '''
    
    # only process form data when the user submits the form (i.e., when the request method is POST)
    if request.method == 'POST':
        # Get form data
        # strip() removes leading and trailing whitespace from the username and email
        username = request.form['username'].strip()
        email = request.form['email'].strip()
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        
        # make sure required fields are filled out and passwords match
        if not username or not email or not password or not confirm_password:
            flash('Please fill out all fields.')
            return redirect(url_for('register'))
        
        if password != confirm_password:
            flash('Passwords do not match.')
            return redirect(url_for('register'))

        # Connect to the database
        conn = get_connection()
        
        # if the connection fails, redirect back to the registration page with an error message
        if conn is None:
            flash('Database connection failed. Please try again later.')
            return redirect(url_for('register'))
        
        # create cursor to execute SQL commands
        cursor = conn.cursor()

        try: 
            # check whether the username and email are already taken
            # %s is a placeholder protected against SQL injection attacks
            cursor.execute('''
                SELECT * 
                FROM users 
                WHERE username = %s OR email = %s''', 
                (username, email))
            
            existing_user = cursor.fetchone()
            
            # don't allow registration if the username or email is already taken
            if existing_user:
                flash('Username or email already taken.')
                return redirect(url_for('register'))
            
            # never store plain text passwords in the database; always store a hashed version
            # generate_password_hash() uses a secure hashing algorithm to hash the 
            # password before storing it
            password_hash = generate_password_hash(password)

            # Insert the new user into the database
            cursor.execute('''
                INSERT INTO users (username, email, password_hash) 
                VALUES (%s, %s, %s)
                RETURNING user_id
            ''',(username, email, password_hash))
            
            # retrieve the user_id of the newly created user
            user_id = cursor.fetchone()[0]
            
            # save the new record permanently in to the database
            conn.commit()
            
            # store the basic user information in the Flask session
            # allows the application to remember that the user is logged in across different pages
            session['user_id'] = user_id
            session['username'] = username
            
            flash("Account created successfully! You are now logged in.")
            
            # send the newly registered user to the dashboard page
            return redirect(url_for('dashboard'))
        
        except Exception as e:
            # if an error occurs, rollback any changes made during this transaction
            conn.rollback()
            print("Registration error:", e)  # log the error for debugging purposes
            flash(f"An error occurred while creating your account: {e}")
            return redirect(url_for('register'))
        
        finally:
            # Close the database connection
            cursor.close()
            conn.close()

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    '''
    Log in an existing user account
    
    GET:
        Display the login form.
        
    POST:
        Process the login form submission.
        Validate the input, check the credentials, and log the user in if valid.
    '''
    
    # only process form data when the user submits the form (i.e., when the request method is POST)
    if request.method == 'POST':
        
        # Get form data
        username_or_email = request.form['username_or_email'].strip()
        password = request.form['password']
        
        # make sure required fields are filled out
        if not username_or_email or not password:
            flash('Please fill out all fields.')
            return redirect(url_for('login'))

        # Connect to the database
        conn = get_connection()
        
        # if the connection fails, redirect back to the login page with an error message
        if conn is None:
            flash('Database connection failed. Please try again later.')
            return redirect(url_for('login'))
        
        # create cursor to execute SQL commands
        cursor = conn.cursor()

        try: 
            # check whether the username or email exists in the database
            cursor.execute('''
                SELECT user_id, username, password_hash 
                FROM users 
                WHERE email = %s OR username = %s
            ''', (username_or_email, username_or_email))
            
            user = cursor.fetchone()
            
            # if no user is found with that username or email, show an error message
            if not user:
                flash('Invalid username/email or password.')
                return redirect(url_for('login'))
            
            # separate the values returned from the database
            user_id, username, password_hash = user
            
            # check whether the provided password matches the stored hashed password
            # check_password_hash() securely compares the hashed password in the
            # database with the password provided by the user
            if not check_password_hash(password_hash, password):
                flash('Invalid username/email or password.')
                return redirect(url_for('login'))
            
            # store the basic user information in the Flask session
            session['user_id'] = user_id
            session['username'] = username
            
            flash("Logged in successfully!")
            
            # send the logged-in user to the dashboard page
            return redirect(url_for('dashboard'))
        
        except Exception as e:
            print("Login error:", e)  # log the error for debugging purposes
            flash(f"An error occurred while logging in: {e}")
            return redirect(url_for('login'))
        
        finally:
            # Close the database connection
            cursor.close()
            conn.close()

    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    '''
    Display the user's dashboard.
    
    The dashboard is only accessible to logged-in users. If the user is not logged in,
    they are redirected to the login page.
    '''
    
    # temp debugging print statements to trace the flow of execution
    print("Current session:", dict(session))
    # check if the user is logged in by looking for "user_id" in the session
    if "user_id" not in session:
        print("User not logged in. Redirecting to login page.")
        return redirect(url_for('login'))
    
    print("User is logged in. Displaying dashboard.")
    
    # retrieve the username from the session to display on the dashboard
    return render_template('dashboard.html', username=session.get('username'))

@app.route('/logout')
def logout():
    '''
    Log the user out by removing their information from the Flask session.
    '''
    print("LOGOUT ROUTE REACHED")
    print("Session before logout:", dict(session))
    
    session.clear()  # clear all session data
    
    print("Session after logout:", dict(session))
    
    flash('You have been logged out.', 'success')
    return redirect(url_for('login'))

# only run the Flask application if this script is executed directly (not imported as a module)
if __name__ == '__main__':
    app.run(debug=True, port=5001)  # run the app in debug mode on port 5001