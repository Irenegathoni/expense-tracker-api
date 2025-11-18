import psycopg2
from psycopg2.extras import RealDictCursor
import os
from dotenv import load_dotenv

#loading the environment variables
load_dotenv(override=True)

def get_db_connection():
   conn= psycopg2.connect(
      host=os.getenv("PGHOST"),
      database=os.getenv("PGDATABASE"),
      user=os.getenv("PGUSER"),
      password=os.getenv("PGPASSWORD"),
      cursor_factory=RealDictCursor
   )
   return conn
    