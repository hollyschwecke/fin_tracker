# Finance Tracker
A full-stack personal finance tracker built with Python, Flask, and PostgreSQL. The application is designed to help users manage their personal financial accounts, track transactions, and eventually visualize their spending and budgeting habits through a centralized dashboard.

### Project Status: In Development
User authentication and database integration are complete. Financial account and transaction features are currently being developed. 

## Overview
Finance Tracker is a web application that allows users to securely create an account and access their own personal financial dashboard.

The project began as a way to practice full-stack software development, database design, authentication, and CRUD operations. It is being developed incrementally with an emphasis on writing maintainable code and building features that could be useful in a real-world personal finance application.

The application currently includes a working user authentication system connected to a PostgreSQL database hosted through Render. 

## Current Features
### User Authentication
* User registration
* Username and email validation
* Duplicate username/email detection
* Password confirmation during registration
* Secure password hashing
* Login using username or email
* Password verification
* Flask session management
* Logout functionality
* Protected dashboard route
* Authentication error messages
* Validation for incorrect login credentials

### Database
The application uses PostgreSQL for persistent data storage

The database is hosted using Render and currently contains tables for the application's users and planned financial functionality.

### Web Application
* Flask backend
* HTML templates using Jinja
* Static CSS/Javascript structure
* User dashboard
* Registration page
* Login page
* Flash messages for user feedback
* Environment variables for sensitive configuration

## Technology Stack
| **Technology** | **Purpose** |
| -------------- | ----------- |
| Python | Backend programming language |
| Flask | Web application framework |
| PostgreSQL | Relational database |
| psycopg2 | PostgreSQL database connection |
| Jinja2 | HTML templating |
| HTML/CSS | Frontend structure and styling |
| JavaScript | Planned frontend interactivity |
| Render | PostgreSQL hosting |
| Git/GitHub | Version control and project management |
| VS Code | Development environment |

## Project Structure
```text
fin_tracker/
| 
|-- app.py
|-- database.py
|-- requirements.txt
|-- .env
|-- .gitignore
|
|-- templates/
|   |-- login.html
|   |-- register.html
|   |-- dashboard.html
|
|-- static/
|   |-- css/
|   |-- js/
```
The project structure will continue to evolve as additional financial features are implemented.

## Authentication Flow
```mermaid
flowchart TD
    A[Register] --> B[Validate Input]
    B --> C[Hash Password]
    C --> D[PostgreSQL Database]
    D --> E[Create Session]
    E --> F[Dashboard]
    F --> G[Logout]
    G --> H[Login Page]
```
Passwords are never stored as plain text. Passwords are hashed before being stored in PostgreSQL.

The application also uses Flask sessions to keep track of authenticated users and protect routes that should only be accessible after login.

## Database Design
The PostgreSQL database is being designed around a relational database structure that connects users to their financial information.

Planned relationships include:

```text
Users
|
|-- Accounts
|   |
|   |-- Transactions
|
|-- Categories
|
|-- Budgers
```
Each user's financial data will be associated with their `user_id`, ensuring that users can only acces their own financial information.

## Development Roadmap
The project is being developed in phases
#### Phase 1 - Database Setup (Complete)
- [x] Design initial database structure
- [x] Create PostgreSQL database
- [x] Connect Flask application to PostgreSQL
- [x] Configure Render database
- [x] Create database tables
- [x] Configure environment variables
- [x] Verify database connection

#### Phase 2 - User Authentication (Complete)
- [x] Create registration page
- [x] Create login page
- [x] Validate registration fields
- [x] Prevent duplicate usernames/emails
- [x] Hash user passwords
- [x] Store users in PostgreSQL
- [x] Create Flask sessions
- [x] Implement login
- [x] Implement logout
- [x] Protect dashboard
- [x] Add authentication error messages
- [x] Test successful and unsuccessful authentication scenarios

#### Phase 3 - Financial Accounts
The next stage is to allow users to manage their financial accounts

Planned functionality:
- [] Add a financial account
- [] View accounts
- [] Edit account information
- [] Delete accounts
- [] Track account balances
- [] Support different account types

Examples:
* Checking
* Savings
* Credit Card
* Cash
* Investments

#### Phase 4 - Transaction Management
Users will be able to record and manage individual financial transactions

Planned functionality:
- [] Add transactions
- [] Edit transactions
- [] Delete transactions
- [] Assign transactions to accounts
- [] Assign transactions to categories
- [] Record income and expenses
- [] Store transaction dates
- [] Add transaction descriptions
- [] View transaction history
- [] Filter transactions

Example:

Account:    Checking 
Category:   Groceries
Amount:     -$72.45
Date:       09/08/2026
Description: Weekly grocery shopping

#### Phase 5 - Categories and Budgeting
The application will eventually allow users to organize spending and create budgets

Planned functionality:
- [] Create expense categories
- [] Create income categories 
- [] Edit categories
- [] Delete categories 
- [] Create monthly budgets
- [] Set spending limits in category
- [] Track spending against budgets
- [] Display remaining budget amounts

Example:

Monthly Budget

Housing         $1500 / $1800
Groceries       $400 / $600
Transportation  $180 / $300
Entertainment   $125 / $200

#### Phase 6 - Dashboard and Data Visualization
The dashboard will eventually provide users with an overview of their financial activity.

Planned functionality:

- [] Total account balance
- [] Monthly income
- [] Monthly expenses 
- [] Net income
- [] Spending by category
- [] Budget progress
- [] Recent transactions
- [] Monthly spending trends
- [] Interactive charts and visualizations

The goal is to turn raw transaction data into information that is easy for users to understand.

#### Phase 7 - UI/UX Improvements
Once the core functionality is complete, the applications interface with be improved

Planned improvements:
- [] Responsive design
- [] Consistent navigation
- [] Improved forms
- [] Better error and success messages
- [] Dashboard cards
- [] Data visualization styling
- [] Mobile-friendly layout
- [] Accessibility improvements

#### Phase 8 - Testing and Deployment
The final phase will focus on making the application more reliable and portfolio-ready.

Planned improvements:
- [] Add automated tests
- [] Test database operations
- [] Test authentication
- [] Test transaction functionality
- [] Improve error handling
- [] Review database security
- [] Deploy the Flask application
- [] Connect the deployed application to PostgreSQL
- [] Add application screenshots
- [] Document deployment instructions 

## Security Considerations
Security is being incorporated throughout development

Current security measures include:
* Password hashing
* Parameterized SQL queries
* Environment variables for sensitive configuration
* Protected Flask routes
* Session-based authentication
* User-specific database queries

Future security improvements will include additional validation, improved session configuration, and further protection of user financial data.

## Running the Project Locally
1. Clone the repository
`git clone https://github.com/hollyschwecke/fin_tracker.git`
`cd fin_tracker`

2. Create the virtual environment
`python3 -m venv venv`
Activate on macOS/Linux:
`source venv/bin/activate`

3. Install dependencies
`pip install -r requirements.txt`

4. Configure environment variables
create a `.env` file in the project root:
`DATABASE_URL=postgresql://finance_tracker_tkxs_user:tP5om78VyKvw1EqKoLJGtzGtAoSzXxut@dpg-da1pdk2jnfac739v7q4g-a.oregon-postgres.render.com/finance_tracker_tkxs`
`SECRET_KEY=a20e7eb5b5144f24739e54470ccd5578609f73214ffc7240cf3922810d388813`
Do not commit the `.env` file to GitHub

5. Run the application
`python3 app.py`
The application should be available at:
`http://127.0.0.1:5001`

## Future Improvements
Potential future features include:
* Recurring transactions
* Monthly financial reports
* Export transactions to CSV
* Search and advanced filtering
* Savings goals
* Multiple budgeting periods
* Financial trend analysis
* Improved data visualizations
* Deployment to a production environment

## Project Goals
This project is being developed to strength practical experience with:
* Full-stack web development
* RESTful application design
* Relational database design
* SQL and PostgreSQL
* Authentication and authorization
* Backend development with Python
* Frontend development
* CRUD operations
* Data visualization
* Version control with Git
* Application deployment
* Software testing

The long-term goal is to create a complete, polished finance application while demonstrating the software engineering and data management skills used throughout its development.  