
import sys
import os

# Add the parent directory to sys.path to import app modules
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

# Set env var for sqlite to avoid postgres driver requirement during import
os.environ["SQLALCHEMY_DATABASE_URI"] = "sqlite:///./test_auth_v2.db"

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient
from app.main import app
from app.db.base_class import Base
from app.api import deps

# Use SQLite for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///./test_auth_v2.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Override get_db dependency
def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[deps.get_db] = override_get_db

# Create tables
Base.metadata.create_all(bind=engine)

client = TestClient(app)

def test_auth_flow():
    email = "test@example.com"
    password = "password123"
    new_password = "newpassword123"

    print("1. Testing Signup...")
    response = client.post(
        "/api/v1/signup",
        json={"email": email, "password": password, "full_name": "Test User"},
    )
    if response.status_code == 200:
        print("   Signup Successful")
    else:
        print(f"   Signup Failed: {response.json()}")
        return

    print("2. Testing Login...")
    response = client.post(
        "/api/v1/login/access-token",
        data={"username": email, "password": password},
    )
    if response.status_code == 200:
        token = response.json()["access_token"]
        print("   Login Successful")
    else:
        print(f"   Login Failed: {response.json()}")
        return

    print("3. Testing Password Recovery...")
    response = client.post(f"/api/v1/password-recovery/{email}")
    if response.status_code == 200:
        print("   Recovery Email Sent")
    else:
        print(f"   Recovery Failed: {response.json()}")
        return

    # For testing reset, we need a valid token. 
    # In a real scenario, this comes from the email. 
    # Here we generate one manually using the same logic as the endpoint.
    from app.core import security
    from datetime import timedelta
    reset_token = security.create_access_token(email, expires_delta=timedelta(hours=1))

    print("4. Testing Password Reset...")
    response = client.post(
        "/api/v1/reset-password",
        json={"token": reset_token, "new_password": new_password},
    )
    if response.status_code == 200:
        print("   Password Reset Successful")
    else:
        print(f"   Password Reset Failed: {response.json()}")
        return

    print("5. Testing Login with New Password...")
    response = client.post(
        "/api/v1/login/access-token",
        data={"username": email, "password": new_password},
    )
    if response.status_code == 200:
        print("   Login with New Password Successful")
    else:
        print(f"   Login with New Password Failed: {response.json()}")

if __name__ == "__main__":
    if os.path.exists("./test_auth_v2.db"):
        try:
             os.remove("./test_auth_v2.db")
        except PermissionError:
             pass
    
    try:
        test_auth_flow()
    finally:
        engine.dispose()
        
    if os.path.exists("./test_auth_v2.db"):
        try:
            os.remove("./test_auth_v2.db")
        except PermissionError:
            print("Could not remove test_auth_v2.db, it might be in use.")
