from sqlalchemy import create_engine


engine = create_engine('mysql+pymysql://root:password@127.0.0.1:42469/',
        pool_pre_ping=True,
        pool_recycle=280,
        connect_args={
        'connect_timeout': 60,
        'read_timeout': 60,
        'write_timeout': 60,
        'autocommit': True
    })
with engine.connect() as connection:
    connection.execute("BEGIN")
    connection.execute("CREATE DATABASE IF NOT EXISTS test_db;")
    connection.execute("COMMIT")
    print("Database created successfully!")
    
print("Connection successful!")
connection.close()


