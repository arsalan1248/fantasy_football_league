
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