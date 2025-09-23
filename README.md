
# Project Title

A Django REST API-based fantasy football platform that allows users to manage virtual teams, trade players, and participate in a dynamic transfer market system.


# Installation


### 1. Installation
```bash
git clone https://github.com/arsalan1248/fantasy_football_league.git
cd fantasy-football-league
```

### 2. Set up environment variables
```bash
copy .env.example .env
# Edit .env file with your configurations
```

### 3. Build and start the application
```bash
docker-compose up --build
```
### 4. Create superuser
```bash
docker-compose exec web python manage.py createsuperuser
```

### 5. Run the application
```bash
API: http://localhost:8000/api/v1/
Admin Panel: http://localhost:8000/admin/
```

### 6. Run tests
```bash
chmod +x run_test.sh 
docker-compose exec web ./run_tests.sh
```


## For Local Developement
```bash
# Activate virtual environment
venv/Scripts/activate (for windows)
source/bin/activate (for mac/linux)

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Start development server
python manage.py runserver
```
# Project Structure

```
fantasy_football_league

├─ core
│  ├─ admin.py
│  ├─ apps.py
│  ├─ exceptions.py
│  ├─ jwt_utils.py
│  ├─ migrations
│  │  ├─ __init__.py
│  ├─ models.py
│  ├─ tests
│  │  ├─ conftest.py
│  │  ├─ test_models.py
│  │  ├─ __init__.py
│  ├─ views.py
│  ├─ __init__.py
├─ docker-compose.prod.yaml
├─ docker-compose.yaml
├─ Dockerfile
├─ entrypoint.sh
├─ fantasy_football_league
│  ├─ asgi.py
│  ├─ settings.py
│  ├─ urls.py
│  ├─ wsgi.py
│  ├─ __init__.py
├─ league
│  ├─ admin.py
│  ├─ apps.py
│  ├─ filters.py
│  ├─ management
│  │  ├─ commands
│  │  │  ├─ create_team_players.py
│  │  │  ├─ __init__.py
│  │  ├─ __init__.py
│  ├─ managers.py
│  ├─ migrations
│  │  ├─ 0001_initial.py
│  │  ├─ 0002_alter_player_team.py
│  │  ├─ 0003_alter_player_options_and_more.py
│  │  ├─ 0004_alter_team_name.py
│  │  ├─ __init__.py
│  ├─ models.py
│  ├─ serializers.py
│  ├─ signals.py
│  ├─ tests
│  │  ├─ factories.py
│  │  ├─ test_league_management.py
│  │  ├─ test_team_management.py
│  │  ├─ __init__.py
│  ├─ tests.py
│  ├─ urls.py
│  ├─ views.py
│  ├─ __init__.py
├─ manage.py
├─ pytest.ini
├─ README.md
├─ requirements.txt
├─ transactions
│  ├─ admin.py
│  ├─ apps.py
│  ├─ migrations
│  │  ├─ 0001_initial.py
│  │  ├─ 0002_playertransaction_transactionrecord_and_more.py
│  │  ├─ __init__.py
│  ├─ models.py
│  ├─ tests
│  │  ├─ test_player_transactions.py
│  │  ├─ __init__.py
│  ├─ tests.py
│  ├─ utils.py
│  ├─ views.py
│  ├─ __init__.py
└─ users
   ├─ admin.py
   ├─ apps.py
   ├─ managers.py
   ├─ migrations
   │  ├─ 0001_initial.py
   │  ├─ 0002_alter_customuser_email_alter_customuser_first_name_and_more.py
   │  ├─ 0003_userprofile.py
   │  ├─ 0004_alter_customuser_managers.py
   │  ├─ __init__.py
   ├─ models.py
   ├─ serializers.py
   ├─ tests
   │  ├─ factories.py
   │  ├─ test_models.py
   │  ├─ test_user_management.py
   │  ├─ __init__.py
   ├─ tests.py
   ├─ urls.py
   ├─ views.py
   ├─ __init__.py
```
# Environment Variables
```
DEBUG=True
SECRET_KEY=secret-key

#DB CONFIGURATIONS
DB_NAME={database-name}
DB_USER={db_user}
DB_PASSWORD={db_password}
DB_HOST={db_host}
DB_PORT={db_port}
```
## API Reference

#### Register User

```http
POST /api/v1/register/

payload = {
  "email": "",
  "first_name": "",
  "last_name": "",
  "password": ""
}
```

#### Login User

```http
POST /api/v1/token/

payload = {
  "email": "",
  "password": ""
}
```

#### Refresh Token

```http
POST /api/v1/token/refresh

payload = {
  "refresh": "",
}
```

#### reset Password

```http
POST /api/v1/reset-password

{
  "email": "",
  "current_password": ""
  "new_password": ""
  "confirm_new_password": ""
}
```

#### Get Profile Details

```http
GET /api/v1/profile/me/

Access Token: **Required**
```

#### Update Profile

```http
PATCH /api/v1/profile/me/

{
    "first_name": ""
}
```

#### Create Team

```http
POST /api/v1/team/

{
  "name": "",
}
Access Token: **Required**
```

#### Get Team Details

```http
GET /api/v1/team/

Access Token: **Required**
```

#### Update Team

```http
PATCH /api/v1/team/{id}/

{
    "name": ""
}
Access Token: **Required**
```

#### List all active players

```http
GET /api/v1/players/

Filter:
 - is_for_sale
 - position
 - name

Access Token: **Required**
```

#### Update Player

```http
PATCH /api/v1/players/{id}/

{
    "position": "",
    "is_for_sale": 
}
Access Token: **Required**
```

#### buy Player

```http
POST /api/v1/players/{player-id}/buy/

{
  "name": "",
}
Access Token: **Required**
```