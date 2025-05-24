import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from typing import Dict, Any, List, Optional 
from datetime import date 

from backend.app.models.user import User
from backend.app.models.student import Student
from backend.app.schemas.student import StudentCreate, StudentUpdate
from backend.app.auth import create_access_token, get_password_hash
# from backend.app.config import settings # Not strictly needed if not using API_V1_PREFIX here

# Helper to create a test user and get token
def get_authenticated_header(db: Session, client: TestClient, username: str = "testuser@example.com", password: str = "testpassword", is_superuser: bool = False) -> Dict[str, str]:
    user = db.query(User).filter(User.username == username).first()
    if not user:
        # Assuming User model requires: username, email, hashed_password, is_active, full_name
        # and is_superuser has a default or is optional.
        user = User(
            username=username,
            email=username, # Assuming email is same as username for test user simplicity
            hashed_password=get_password_hash(password),
            is_active=True,
            is_superuser=is_superuser,
            full_name=username.split('@')[0] # Example for full_name
        )
        db.add(user)
        db.commit()
        db.refresh(user)
    
    access_token = create_access_token(data={"sub": user.username, "user_id": user.id}) 
    return {"Authorization": f"Bearer {access_token}"}

# Helper to create a user directly in the DB, useful for foreign key relations
def create_user_in_db(db: Session, username: str = "defaultuser@example.com", password: str = "password", is_superuser: bool = False) -> User:
    user = db.query(User).filter(User.username == username).first()
    if not user:
        user = User(
            username=username,
            email=username,
            hashed_password=get_password_hash(password),
            is_active=True,
            is_superuser=is_superuser,
            full_name=username.split('@')[0]
        )
        db.add(user)
        db.commit()
        db.refresh(user)
    return user

# --- Test Cases for POST /students/ ---

def test_create_student_success(client: TestClient, db_session: Session):
    # User to be associated with the student
    student_owner_user = create_user_in_db(db_session, username="studentowner@example.com")
    # User performing the API request
    requesting_user_headers = get_authenticated_header(db_session, client, username="apioperator@example.com")

    student_data = {
        "user_id": student_owner_user.id,
        "student_number": "S00001",
        "first_name": "John",
        "last_name": "Doe",
        "date_of_birth": "2005-08-15",
        "gender": "Male",
        "address": "123 Main St",
        "phone_number": "555-1234",
        "email": "john.doe.student@example.com", # Student's own email
        "enrollment_date": "2023-09-01",
        "major": "Computer Science",
        "status": "Enrolled"
    }
    response = client.post("/students/", json=student_data, headers=requesting_user_headers)
    assert response.status_code == 201, response.text
    data = response.json()
    assert data["student_number"] == "S00001"
    assert data["first_name"] == "John"
    assert data["user_id"] == student_owner_user.id
    assert "id" in data

    db_student = db_session.query(Student).filter(Student.id == data["id"]).first()
    assert db_student is not None
    assert db_student.student_number == "S00001"
    assert db_student.user_id == student_owner_user.id

def test_create_student_non_existent_user_id(client: TestClient, db_session: Session):
    headers = get_authenticated_header(db_session, client, username="auth_user_for_nonexistent_fk@example.com")
    student_data = {
        "user_id": 99999, # Non-existent user ID
        "student_number": "S00002",
        "first_name": "Jane", "last_name": "Doe", "date_of_birth": "2006-01-01",
        "gender": "Female", "address": "456 Oak St", "phone_number": "555-5678",
        "email": "jane.doe.student@example.com", "enrollment_date": "2023-09-01",
        "major": "Biology", "status": "Enrolled"
    }
    response = client.post("/students/", json=student_data, headers=headers)
    assert response.status_code == 404, response.text # As per router logic for "Utilisateur non trouvé"
    assert "Utilisateur non trouvé" in response.json()["detail"]


def test_create_student_duplicate_student_number(client: TestClient, db_session: Session):
    student_owner_user = create_user_in_db(db_session, username="studentowner_dup_studnum@example.com")
    headers = get_authenticated_header(db_session, client, username="auth_user_dup_studnum@example.com")

    student_data_1 = {
        "user_id": student_owner_user.id, "student_number": "S00003", "first_name": "Alice", "last_name": "Smith",
        "date_of_birth": "2005-02-10", "gender": "Female", "address": "789 Pine St",
        "phone_number": "555-1111", "email": "alice.smith.student@example.com", "enrollment_date": "2023-09-01",
        "major": "Physics", "status": "Enrolled"
    }
    response1 = client.post("/students/", json=student_data_1, headers=headers)
    assert response1.status_code == 201, response1.text

    student_data_2 = { # Same student_number
        "user_id": student_owner_user.id, "student_number": "S00003", "first_name": "Bob", "last_name": "Brown",
        "date_of_birth": "2005-03-20", "gender": "Male", "address": "101 Maple St",
        "phone_number": "555-2222", "email": "bob.brown.student@example.com", "enrollment_date": "2023-09-01",
        "major": "Mathematics", "status": "Enrolled"
    }
    response2 = client.post("/students/", json=student_data_2, headers=headers)
    assert response2.status_code == 400, response2.text
    assert "Numéro d'étudiant déjà enregistré" in response2.json()["detail"]

def test_create_student_no_auth(client: TestClient, db_session: Session):
    student_owner_user = create_user_in_db(db_session, username="studentowner_no_auth@example.com")
    student_data = {
        "user_id": student_owner_user.id, "student_number": "S00004", "first_name": "Charlie", "last_name": "Davis",
        "date_of_birth": "2005-04-05", "gender": "Male", "address": "222 Birch St",
        "phone_number": "555-3333", "email": "charlie.davis.student@example.com", "enrollment_date": "2023-09-01",
        "major": "Chemistry", "status": "Enrolled"
    }
    response = client.post("/students/", json=student_data) # No headers
    assert response.status_code == 401, response.text 
    assert response.json()["detail"] == "Not authenticated"


# --- Test Cases for GET /students/ ---

def test_read_students_empty(client: TestClient, db_session: Session):
    headers = get_authenticated_header(db_session, client, username="list_empty_user@example.com")
    response = client.get("/students/", headers=headers)
    assert response.status_code == 200, response.text
    assert response.json() == []

def test_read_students_with_data(client: TestClient, db_session: Session):
    user1 = create_user_in_db(db_session, username="user_for_student_A@example.com")
    user2 = create_user_in_db(db_session, username="user_for_student_B@example.com")
    headers = get_authenticated_header(db_session, client, username="list_data_user@example.com")

    common_fields = {"date_of_birth": "2000-01-01", "gender": "Other", "address": "Addr", "phone_number": "000", "enrollment_date": "2020-01-01", "status": "Enrolled"}
    student_data_1 = {"user_id": user1.id, "student_number": "S00010", "first_name": "Test", "last_name": "StudentA", "email":"tsa.student@example.com", "major": "MajorA", **common_fields}
    student_data_2 = {"user_id": user2.id, "student_number": "S00011", "first_name": "Test", "last_name": "StudentB", "email":"tsb.student@example.com", "major": "MajorB", **common_fields}
    
    client.post("/students/", json=student_data_1, headers=headers)
    client.post("/students/", json=student_data_2, headers=headers)

    response = client.get("/students/", headers=headers)
    assert response.status_code == 200, response.text
    data = response.json()
    assert len(data) == 2
    student_numbers = {s["student_number"] for s in data}
    assert "S00010" in student_numbers
    assert "S00011" in student_numbers


def test_read_students_pagination(client: TestClient, db_session: Session):
    user = create_user_in_db(db_session, username="user_for_pagination_students@example.com")
    headers = get_authenticated_header(db_session, client, username="pagination_test_user@example.com")
    
    base_data = {"gender": "Male", "address": "Street", "phone_number": "555-000", "enrollment_date": "2021-01-01", "major": "Pagination Studies", "status": "Enrolled"}
    for i in range(5): # Create 5 students
        student_data = {
            "user_id": user.id, "student_number": f"S0002{i}", "first_name": f"PageTest{i}", "last_name": "User",
            "date_of_birth": f"2000-01-{i+1:02d}", "email": f"pt{i}.student@example.com", **base_data
        }
        post_response = client.post("/students/", json=student_data, headers=headers)
        assert post_response.status_code == 201, post_response.text


    # Test limit
    response_limit = client.get("/students/?limit=2", headers=headers)
    assert response_limit.status_code == 200, response_limit.text
    data_limit = response_limit.json()
    assert len(data_limit) == 2
    assert data_limit[0]["student_number"] == "S00020"
    assert data_limit[1]["student_number"] == "S00021"

    # Test skip
    response_skip = client.get("/students/?skip=2&limit=2", headers=headers)
    assert response_skip.status_code == 200, response_skip.text
    data_skip = response_skip.json()
    assert len(data_skip) == 2
    assert data_skip[0]["student_number"] == "S00022"
    assert data_skip[1]["student_number"] == "S00023"

# --- Test Cases for GET /students/{student_id} ---

def test_read_student_by_id_success(client: TestClient, db_session: Session):
    user = create_user_in_db(db_session, username="user_for_get_one_student@example.com")
    headers = get_authenticated_header(db_session, client, username="get_one_student_user@example.com")
    student_data = {
        "user_id": user.id, "student_number": "S00030", "first_name": "Fetch", "last_name": "Me",
        "date_of_birth": "2002-06-15", "gender": "Female", "address": "Someplace",
        "phone_number": "555-FETCH", "email": "fetchme.student@example.com", "enrollment_date": "2022-09-01",
        "major": "History", "status": "Enrolled"
    }
    post_response = client.post("/students/", json=student_data, headers=headers)
    assert post_response.status_code == 201
    student_id = post_response.json()["id"]

    response = client.get(f"/students/{student_id}", headers=headers)
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["id"] == student_id
    assert data["student_number"] == "S00030"
    assert data["first_name"] == "Fetch"

def test_read_student_by_id_not_found(client: TestClient, db_session: Session):
    headers = get_authenticated_header(db_session, client, username="get_non_existent_student_user@example.com")
    response = client.get("/students/99999", headers=headers) 
    assert response.status_code == 404, response.text
    assert response.json()["detail"] == "Étudiant non trouvé"

# --- Test Cases for PUT /students/{student_id} ---

def test_update_student_success(client: TestClient, db_session: Session):
    user = create_user_in_db(db_session, username="user_for_update_student_op@example.com")
    headers = get_authenticated_header(db_session, client, username="update_student_op_user@example.com")
    student_data = {
        "user_id": user.id, "student_number": "S00040", "first_name": "Original", "last_name": "Name",
        "date_of_birth": "2003-03-03", "gender": "Male", "address": "Old Address",
        "phone_number": "555-OLD", "email": "original.student@example.com", "enrollment_date": "2021-09-01",
        "major": "Old Major", "status": "Enrolled"
    }
    post_response = client.post("/students/", json=student_data, headers=headers)
    assert post_response.status_code == 201
    student_id = post_response.json()["id"]

    update_payload = {"first_name": "Updated", "major": "New Major", "phone_number": "555-NEW"}
    response = client.put(f"/students/{student_id}", json=update_payload, headers=headers)
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["id"] == student_id
    assert data["student_number"] == "S00040" # student_number is not updated here
    assert data["first_name"] == "Updated"
    assert data["major"] == "New Major"
    assert data["phone_number"] == "555-NEW"
    assert data["last_name"] == "Name" # Should remain from original

    db_session.expire_all() # Ensure fresh read from DB
    db_student = db_session.query(Student).filter(Student.id == student_id).first()
    assert db_student.first_name == "Updated"
    assert db_student.major == "New Major"

def test_update_student_partial_update(client: TestClient, db_session: Session):
    user = create_user_in_db(db_session, username="user_for_partial_update_op@example.com")
    headers = get_authenticated_header(db_session, client, username="partial_update_op_user@example.com")
    student_data = {
        "user_id": user.id, "student_number": "S00041", "first_name": "Partial", "last_name": "UpdateTest",
        "date_of_birth": "2004-04-04", "gender": "Female", "address": "Initial Address",
        "phone_number": "555-INITIAL", "email": "partial.student@example.com", "enrollment_date": "2022-01-01",
        "major": "Initial Major", "status": "Enrolled"
    }
    post_response = client.post("/students/", json=student_data, headers=headers)
    assert post_response.status_code == 201
    student_id = post_response.json()["id"]

    update_payload = {"address": "Completely New Address"} 
    response = client.put(f"/students/{student_id}", json=update_payload, headers=headers)
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["id"] == student_id
    assert data["address"] == "Completely New Address"
    assert data["first_name"] == "Partial" # Should remain unchanged
    assert data["major"] == "Initial Major" # Should remain unchanged

    db_session.expire_all() # Ensure fresh read from DB
    db_student = db_session.query(Student).filter(Student.id == student_id).first()
    assert db_student.address == "Completely New Address"
    assert db_student.first_name == "Partial"


def test_update_student_not_found(client: TestClient, db_session: Session):
    headers = get_authenticated_header(db_session, client, username="update_non_existent_student_user@example.com")
    update_payload = {"first_name": "Ghost"}
    response = client.put("/students/99999", json=update_payload, headers=headers) 
    assert response.status_code == 404, response.text
    assert response.json()["detail"] == "Étudiant non trouvé"

# --- Test Cases for DELETE /students/{student_id} ---

def test_delete_student_success(client: TestClient, db_session: Session):
    user = create_user_in_db(db_session, username="user_for_delete_student_op@example.com")
    headers = get_authenticated_header(db_session, client, username="delete_student_op_user@example.com")
    student_data = {
        "user_id": user.id, "student_number": "S00050", "first_name": "ToDelete", "last_name": "Soon",
        "date_of_birth": "1999-12-31", "gender": "Other", "address": "Temporary Place",
        "phone_number": "555-DELETE", "email": "deleteme.student@example.com", "enrollment_date": "2020-01-01",
        "major": "Ephemeral Studies", "status": "Enrolled"
    }
    post_response = client.post("/students/", json=student_data, headers=headers)
    assert post_response.status_code == 201
    student_id = post_response.json()["id"]

    delete_response = client.delete(f"/students/{student_id}", headers=headers)
    # The router now returns status 204 No Content
    assert delete_response.status_code == 204, delete_response.text
    # There should be no JSON body to parse for a 204 response
    assert delete_response.content == b""

    db_student = db_session.query(Student).filter(Student.id == student_id).first()
    assert db_student is None

def test_delete_student_not_found(client: TestClient, db_session: Session):
    headers = get_authenticated_header(db_session, client, username="delete_non_existent_student_user@example.com")
    response = client.delete("/students/99999", headers=headers) 
    assert response.status_code == 404, response.text
    assert response.json()["detail"] == "Étudiant non trouvé"
