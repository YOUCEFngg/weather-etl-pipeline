import time
import os
from sqlalchemy import create_engine

print("Waiting for PostgreSQL to be ready...")

engine = create_engine(
    f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}"
    f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
)

for i in range(30):
    try:
        with engine.connect() as conn:
            print("PostgreSQL is ready!")
            exit(0)
    except Exception:
        print(f"Attempt {i+1}/30... PostgreSQL not ready yet")
        time.sleep(2)

print("Failed to connect to PostgreSQL")
exit(1)
