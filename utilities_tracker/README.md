## Installation
### 1. Cloning a repository:
```bash
git clone git clone git clone https://github.com/AnnaKilimova/python_testing_portfolio.git
cd python_testing_portfolio
```
### 2. Creating and activating of a virtual environment:
#### For MacOS/Linux:
```bash
python3 -m venv venv
source venv/bin/activate    
```  
### For Windows:
```bash
venv\Scripts\activate    
```
### 3. Installing dependencies:
```bash
pip install -r requirements.txt    
```
---

## Technical specifications
#### Project: Utilities Tracker
#### Project type: Web application on Flask with SQLite database
#### Purpose: Keeping track of utilities, their measurements, and reminders. 

## 1. Main entities
### 1.1. Service
- Attributes:
    * Service name (e.g., ‘Electricity,’ ‘Water,’ ‘Internet’)
    * Unit of measurement (kWh, m³, GB)
    * Additional description (optional)
- Relationships:
    * One service ↔ Many measurements
    * Many services ↔ Many reminder templates
### 1.2. Measurement
- Attributes:
    * Date
    * Value (meter reading)
    * Note (optional)
- Relationships:
    * Many measurements ↔ One service  
- Validation:
    * foreign key for service
### 1.3. ReminderTemplate
- Attributes:
    * Day of the month when readings should be entered
    * Reminder time (optional)
    * Note (optional)
- Relationships:
    * One service ↔ Many measurements
    * Many reminder templates ↔ Many services  
- Validation:
    * association table ‘service_reminder’.
## 2. Functional requirements
### 2.1. CRUD for services
- Adding, editing, deleting a service
- Viewing a list of all services
### 2.2. CRUD for measurements
- Adding a new measurement manually
- Deleting measurements
- Measurement history for each service
### 2.3. CRUD for reminders
- Adding a new reminder manually
- Editing and deleting reminders
- The system should check the date and notify users of the need to enter new data
- For MVP: the reminder can be implemented as a display on the main page saying ‘Today you need to enter your readings’
### 2.4. Calendar
- Display of readings on the calendar with the dates of entry marked
### 2.5. Calculate consumption
- Automatically calculate the difference between the current and previous readings for each service
- Show monthly consumption
## 3. Interface
### 3.1. The main layout template used by all other pages
* Contains the navigation bar with links to the home page, add measurement, reminders, and calendar
* Includes Bootstrap styling and a container for flash messages
### 3.2. Main dashboard page
* Displays a list of all services with their latest measurement value and date
* “Add Service” button at the top
* Section showing today’s reminders: time, note, and associated services
* Links to service detail pages for more information
### 3.3. Service detail page
* Shows the service name and unit
* Buttons to edit or delete the service.
* Table with the history of measurements (date, value, note)
* Delete button for individual measurements
* Placeholder for future features such as consumption and charts
### 3.4. Add new service page
* Form with fields for service name, unit, and description
* Server-side validation with error messages
* Submit and cancel buttons
### 3.5. Edit existing service page
* Pre-filled form with name, unit, and description
* “Save changes” and “Cancel” buttons
### 3.6. Add measurement page. Form with fields:
* Service (dropdown)
* Date
* Value
* Note (optional)
* Validation error handling
* Submit button
### 3.7. Reminder templates management page. Form to create a new reminder template:
* Day of month
* Time
* Note
* Multiple services selection
* Table listing existing reminders: Columns: Day, Time, Note, Services, Actions
* Buttons to edit or remove reminders
### 3.8. Edit reminder page. Form for modifying an existing reminder template:
* Day of month
* Time
* Note
* Services (multi-select)
* Save and cancel actions.
### 3.9. Calendar / events overview page.
* Displays all recorded measurements as a simple table with:
* Date
* Service name

## 4. Implementation features
* Flask + SQLAlchemy.
* SQLite (default).
* The table is created automatically when the application is launched (db.create_all()).
* Bootstrap 5 is used for styling.

### Test execution
```bash
# ---------------- pytest ----------------
pytest utilities_tracker -v
```

## Launching the application
```bash
python -m utilities_tracker.app
```