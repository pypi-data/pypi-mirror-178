# Django Api Tools

A collection of apps that support basic django functionality over api

Caveat enptor, very early days, still being tested in it's first project

# Use

- `pip install ...`
- add `'django_accounts_api',` to INSTALLED_APPS
- add `path('/accounts_api/', include('django_accounts_api.urls'))` to your urls

## Features

### API endpoints

Scenario to support is a compiled javascript capable frontend needing to provide authentication features over api
Frontend should be able to:

Optionally get api endpoints from api.

| Task | How |
|-----|-----|
| find api endpoints | GET `/manifest` |
| Detect auth | GET `/login-check` |
| show user name | json parse GET `/login-check` response |
| render a login form | GET `/login` body returns partial HTML |
| submit a login form | wrap partial form above in a form, `new FormData(...)` it and POST to `/login |
| render form errors | render partial HTML returned from POST `/login` |
| login | POST `/login` returns 201 |
| logout | POST `/logout` |


## Development
1. Install Poetry https://python-poetry.org/docs/#installation

2. Use a virtual environment https://python-poetry.org/docs/basic-usage/#using-your-virtual-environment

3. `poetry install --with test,dev --no-root`

4. `pytest`
