import os
from database import connect, create_user, init_db
path=os.environ.get("SERVICE_REQUEST_DB", "instance/local_service_connect.db")
init_db(path)
email=os.environ.get("ADMIN_EMAIL", "admin@localservice.test")
password=os.environ.get("ADMIN_PASSWORD")
if not password:
    raise SystemExit("Set ADMIN_PASSWORD before running this script.")
with connect(path) as db:
    exists=db.execute("SELECT id FROM users WHERE email=?",(email.lower(),)).fetchone()
if exists: print("Administrator account already exists.")
else:
    create_user(path,"System Administrator",email,"0000000000",password,"admin")
    print(f"Administrator account created for {email}")
