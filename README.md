
MotoRiders BG
MotoRiders BG is a Django web application for motorcycle riders and motorcycle enthusiasts in Bulgaria.
The platform allows users to register accounts, create Rider profiles, organize and join motorcycle rides, publish Ride Reviews, request roadside assistance, discover motorcycle garages and services, and submit Garage Reviews and ratings.


Features
Authentication and User Accounts

- Custom Django user model based on AbstractUser
- User registration
- User login and logout
- Authentication-aware navigation
- Private My Profile page for authenticated users
- Automatic assignment of newly registered users to the Registered Users group
- Automatic assignment to the Riders group after successful Rider profile creation
- Group-based permissions
- Permission checks using PermissionRequiredMixin
- Permission checks for function-based views using permission_required
- Owner-restricted editing and deletion
User Groups
The application uses two Django Groups with distinct permissions.
Registered Users
Newly registered accounts are automatically assigned to this group.
Registered users can:

- Browse Riders
- Browse Rides and Ride Reviews
- Browse Road Assistance requests
- Browse Garages and Services
- Browse Garage Reviews
- Create a Rider profile
- Create and manage their own Garages
- Create and manage their own Garage Reviews
Riders
When a registered user creates a Rider profile, the account is additionally assigned to the Riders group.
Riders receive additional permissions to:

- Manage their Rider profile
- Create and manage Rides
- Join and leave planned Rides
- Create and manage Ride Reviews
- Create and manage Road Assistance requests
Group permissions determine whether a user may perform a category of operation, while view querysets additionally enforce ownership of individual objects.


Rider Profiles

- Create, view, edit, and delete Rider profiles
- One Rider profile per registered account
- Rider ownership is automatically assigned to the authenticated AppUser
- Search Riders by: 
- First name
- Last name
- Nickname
- Store: 
- Nickname
- City
- Custom city or village
- Motorcycle brand
- Motorcycle model
- Motorcycle type
- Riding experience
- Phone number
- Optional profile photo
- Optional biography
- Select Bulgarian cities from predefined choices
- Support a custom city or village when Other is selected
- Display Rider activity information
- Owner-only Rider editing and deletion


Rides

- Create, view, edit, and delete motorcycle Rides
- Only users with Rider permissions can create Rides
- Ride organizer is assigned automatically from the authenticated Rider
- Organizer cannot be selected manually from the form
- Rides can be edited only while their status is Planned
- Owner-only Ride editing and deletion
- Search Rides by: 
- Title
- Organizer first name
- Organizer last name
- Organizer nickname
- Participant first name
- Participant last name
- Participant nickname
- Meeting point
- Destination
- Road type
- Road difficulty
- Description
- Filter Rides by status
- Sort Rides by creation date
- Store: 
- Organizer
- Meeting point
- Starting city
- Destination
- Departure date and time
- Estimated duration
- Distance
- Multiple road types
- Road difficulty
- Status
- Maximum participant capacity
- Description
- Display current participant count
- Display remaining participant capacity
- Custom template filters for Ride status presentation
Ride Participation

- Riders can join planned Rides
- Riders can leave planned Rides
- Rider identity is determined from the authenticated account
- Users cannot select another Rider when joining
- Organizer cannot join as a participant
- Duplicate participation is prevented
- Completed or cancelled Rides cannot be joined
- Capacity limits are enforced
- Join and Leave operations are permission-protected
The Ride-participant relationship is implemented as a Many-to-Many relationship between Ride and Rider.


Ride Reviews

- Create, view, edit, and delete Ride Reviews
- Reviewer is assigned automatically from the authenticated Rider
- Reviewer cannot be selected manually
- Search by Ride title or reviewer information
- Reviews are restricted to: 
- The Ride organizer
- Riders who participated in the Ride
- Reviews are allowed only for Rides with Completed status
- One Rider can review a particular Ride only once
- Duplicate Reviews are prevented using a database UniqueConstraint
- Review authors can edit and delete only their own Reviews
- Rating fields include: 
- Overall Ride experience
- Road conditions
- Scenery
- Riding difficulty
- Custom template filters provide rating descriptions


Road Assistance

- Create, view, edit, and delete Road Assistance requests
- Only Riders can create Help Requests
- Rider is assigned automatically from the authenticated account
- Rider cannot be selected manually from the form
- Requests can be edited only while their status is Open
- Owner-only editing and deletion
- Store: 
- Rider
- Request title
- Issue description
- Urgency
- Location
- Status
- Filter Help Requests by Open or Closed


Motorcycle Garages and Services
The services application provides a directory of motorcycle garages and the Services they offer.
Service Catalogue
Service is a database model containing a controlled catalogue of motorcycle workshop Services.
The initial catalogue is populated automatically using a Django data migration and currently includes Services such as:

- Brake Service
- Chain and Sprocket Service
- Clutch Repair and Replacement
- Cooling System Service
- Electrical Diagnostics and Repair
- Engine Diagnostics
- Engine Repair
- Fuel System and Injection Service
- Motorcycle Customization
- Motorcycle Transport and Recovery
- Oil and Filter Service
- Painting and Bodywork
- Suspension Service
- Transmission and Gearbox Repair
- Tyre Service
Garage owners select existing Services instead of entering arbitrary Service names.
Garages

- Create, view, edit, and delete Garages
- Garage owner is automatically assigned from the authenticated AppUser
- Owner cannot be selected manually
- Registered users can create Garages
- Only the Garage owner can edit or delete a Garage
- Store: 
- Garage name
- Owner
- Description
- Bulgarian city
- Address
- Phone number
- Email
- Services offered
- Garage city uses predefined Bulgarian city choices
- Search Garages by: 
- Garage name
- City
- Service name
- A Garage can offer multiple Services
- The same Service can be offered by multiple Garages
Garage and Service therefore form the application's second major Many-to-Many relationship.


Garage Reviews and Ratings

- Any registered user can submit a Garage Review
- Reviewer is automatically assigned from the authenticated AppUser
- Reviewer cannot be selected manually
- A Garage owner cannot review their own Garage
- One user can submit only one Review for a particular Garage
- Duplicate Reviews are prevented with a database UniqueConstraint
- Review authors can edit and delete only their own Reviews
- Other users can view Reviews but cannot modify them
- Ratings use a 1-to-5 scale
- Garage average rating is calculated dynamically using Django ORM Avg()
- Average rating is not stored redundantly in the database
- Average rating is displayed numerically
- A custom template filter renders visual star ratings
- Bootstrap styling displays the stars in a highlighted color


My Profile
Authenticated users have access to a private My Profile page.
The page uses the currently authenticated AppUser and existing reverse model relationships.
For all registered users it can display:

- Account information
- Garages owned by the account
- Garage Reviews submitted by the account
For accounts with a Rider profile it additionally displays:

- Rider profile information
- Organized Rides
- Joined Rides
- Ride Reviews
- Road Assistance requests
No additional database model is required for My Profile.


Public and Private Sections
Anonymous visitors can browse the public application content, including:

- Rider profiles
- Rides
- Ride Reviews
- Road Assistance requests
- Garages
- Garage Reviews
Authentication and permissions are required for actions that modify application data.
User-interface controls are displayed according to the current user's permissions. Backend permission checks and owner-restricted querysets remain in place even when action buttons are hidden.


Forms and Validation
The project includes extensive Django form customization:

- ModelForms
- Customized labels
- Help texts
- Placeholders
- Widgets
- Custom validation messages
- Field-specific cleaning
- Cross-field validation with clean()
- Model-level validators
- CSRF protection for POST forms
- Disabled fields on deletion confirmation forms
- Dedicated delete confirmation pages
- Multiple-selection widgets for Many-to-Many relationships
- Server-controlled ownership fields
Sensitive ownership fields such as Rider owner, Ride organizer, Help Request Rider, Garage owner, and Review author are not exposed as user-selectable form fields.


Database Architecture
The project uses PostgreSQL.
Main Models

- AppUser
- Rider
- Ride
- RideReview
- HelpRequest
- Service
- Garage
- GarageReview
AppUser and Rider form the custom user/profile architecture through a One-to-One relationship.
Many-to-One Relationships
Examples include:

- One Rider can organize many Rides
- One Ride can have many Ride Reviews
- One Rider can write many Ride Reviews
- One Rider can create many Help Requests
- One AppUser can own many Garages
- One Garage can receive many Garage Reviews
- One AppUser can write many Garage Reviews
Many-to-Many Relationships
Ride Participants

- One Ride can contain multiple Riders
- One Rider can participate in multiple Rides
Garage Services

- One Garage can offer multiple Services
- One Service can be offered by multiple Garages


Groups and Permissions
Required application Groups and permissions are created through Django data migrations.
Current Groups:

- Registered Users
- Riders
The application uses:

- LoginRequiredMixin
- PermissionRequiredMixin
- permission_required
- Group permissions
- Owner-restricted QuerySets
Permissions determine whether an account may perform an operation, while ownership filtering determines which specific objects the account may modify.


Data Migrations
The project uses custom Django data migrations for required initial application data.
These migrations create:

- The initial motorcycle Service catalogue
- Registered Users Group
- Riders Group
- Group permissions
- Updated Garage Review permissions
This makes the required initial application configuration reproducible across local, evaluator, and production databases.


Templates
The project uses:

- Shared base template
- Template inheritance
- Shared navigation
- Shared footer
- Reusable card templates
- Django built-in template tags and filters
- Custom template tags
- Custom template filters
- Custom Garage star-rating filter
- Custom 404 page
- Bootstrap 5 styling
- Dark motorcycle-themed interface


Technologies

- Python
- Django
- PostgreSQL
- HTML
- CSS
- Bootstrap 5
- Django Template Language
- Django ORM
- Pillow
- python-dotenv
- psycopg
Exact dependency versions are available in requirements.txt.


Project Structure
motoriders_bg_advanced/
├── motoriders_bg/        # Project settings and root URLs
├── accounts/             # Custom AppUser, authentication, Groups and My Profile
├── common/               # Shared choices, validators, mixins and home page
├── riders/               # Rider profiles
├── rides/                # Rides, Ride Reviews and Ride participation
├── assistance/           # Road Assistance requests
├── services/             # Service catalogue, Garages and Garage Reviews
├── templates/            # Application templates and reusable partials
├── media/                # Uploaded files during local development
├── manage.py
├── requirements.txt
└── README.md


Installation
1. Clone the repository
git clone https://github.com/DragomirZhelev/motoriders_bg_advanced
cd motoriders_bg_advanced
2. Create a virtual environment
On Windows:
py -m venv .venv
On systems where python is available globally:
python -m venv .venv
3. Activate the virtual environment
Windows PowerShell:
.\.venv\Scripts\Activate.ps1
Windows Command Prompt:
.venv\Scripts\activate
macOS/Linux:
source .venv/bin/activate
4. Install dependencies
python -m pip install -r requirements.txt
5. Configure environment variables
Create a .env file in the project root.
The application expects configuration for values including:
SECRET_KEY
DB_NAME
DB_USER
DB_PASSWORD
DB_HOST
DB_PORT
The real .env file is excluded from version control.
6. Configure PostgreSQL
Create a PostgreSQL database and provide its connection information through .env.
The application is configured to use:
django.db.backends.postgresql
7. Apply migrations
python manage.py migrate
Migrations create the database structure and required initial application data, including:

- Service catalogue
- Registered Users Group
- Riders Group
- Group permissions
8. Optional: create a superuser
python manage.py createsuperuser
9. Start the development server
python manage.py runserver
10. Open the application
http://127.0.0.1:8000/


Environment Variables and Credentials
Sensitive values are loaded from environment variables with python-dotenv.
The .env file is excluded through .gitignore and must not be committed.
Production and local environments can therefore use different:

- Secret keys
- Database names
- Database users
- Database passwords
- Database hosts
- Database ports
without modifying application source code.


Main Pages

- / - Home
- /accounts/register/ - Registration
- /accounts/login/ - Login
- /accounts/my-profile/ - Private My Profile
- /riders/list/ - Riders
- /rides/list/ - Rides
- /rides/ride-review/list/ - Ride Reviews
- /assistance/list/ - Road Assistance
- /services/garage/list/ - Garages
- /services/garage-review/list/ - Garage Reviews


Security and Ownership
The application uses several authorization layers:

1. Authentication verifies that the user is logged in.
2. Group permissions determine whether the user may perform a category of operation.
3. View querysets restrict access to objects owned by the authenticated user.
4. Server-side ownership assignment prevents users from selecting another owner/reviewer through forms.
5. CSRF protection is enabled on POST operations.
6. Database constraints enforce uniqueness rules such as one Ride Review per Rider/Ride and one Garage Review per user/Garage.


Current Development Status
Implemented so far:

- Custom authentication
- Registration/login/logout
- User Groups and permissions
- Rider profiles
- Rides and participation
- Ride Reviews
- Road Assistance
- Service catalogue
- Garages
- Garage Reviews
- Garage average ratings
- Custom star-rating filter
- PostgreSQL configuration
- Environment-variable configuration
- My Profile account dashboard
Additional advanced requirements such as REST API endpoints, asynchronous/background processing, automated test coverage, and production deployment are planned as subsequent implementation stages.


Author
Dragomir Zhelev
