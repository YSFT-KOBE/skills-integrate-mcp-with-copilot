import getpass
import json
import os
from pathlib import Path

from auth import hash_password


accounts_path = Path(os.getenv(
    "TEACHER_ACCOUNTS_FILE", Path(__file__).with_name("teacher_accounts.json")
))
username = input("Teacher username: ").strip()
password = getpass.getpass("Teacher password: ")
confirmation = getpass.getpass("Confirm password: ")

if not username:
    raise SystemExit("Username cannot be empty")
if not password or password != confirmation:
    raise SystemExit("Passwords must be non-empty and match")

if accounts_path.exists():
    try:
        accounts = json.loads(accounts_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as error:
        raise SystemExit(f"Invalid account file: {error}") from error
else:
    accounts = {"teachers": []}

teachers = accounts.get("teachers") if isinstance(accounts, dict) else None
if not isinstance(teachers, list):
    raise SystemExit("Account file must contain a teachers list")
if any(teacher.get("username") == username for teacher in teachers
       if isinstance(teacher, dict)):
    raise SystemExit("That username already exists")

teachers.append({"username": username, "password_hash": hash_password(password)})
accounts_path.parent.mkdir(parents=True, exist_ok=True)
accounts_path.write_text(json.dumps(accounts, indent=2) + "\n", encoding="utf-8")
accounts_path.chmod(0o600)
print(f"Teacher account created in {accounts_path}")