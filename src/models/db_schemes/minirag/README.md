## Run Alembic Migrations

## Configrations
```bash
cp alembic.ini.example alembic.ini
```
- Update the `alembic.ini` with your database credentials(`sqlalchemy.url`)

## (Optional) Create a new migration
```bash
cd /src/models/db_schemes/minirag
alembic revision --autogenerate -m"Add...."
```
## Upgrade the database 
```bash
alembic upgrade head
```
