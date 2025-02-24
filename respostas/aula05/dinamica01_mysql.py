import sqlalchemy
from sqlalchemy_utils import create_database, database_exists

DATABASE_URL = 'mysql+pymysql://root:next@localhost:3307/next2025'

engine = sqlalchemy.create_engine(DATABASE_URL)

if not database_exists(engine.url):
    create_database(engine.url)

with engine.connect() as conn:
    table_exists = conn.exec_driver_sql("""
        SELECT EXISTS (
            SELECT 1
            FROM information_schema.tables
            WHERE table_name = 'students'
        );
    """).scalar()

    if not table_exists:
        print("Creating table 'students'")
        conn.exec_driver_sql("""
            CREATE TABLE students (
                name VARCHAR(255),
                age INT
            );
        """)
        conn.commit()

inspection = sqlalchemy.inspect(engine)
print(inspection.get_table_names())
