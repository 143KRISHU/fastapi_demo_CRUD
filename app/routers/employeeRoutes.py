from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .dbDependency import get_db_dependency
from ..Models import EmployeeTable  # SQLAlchemy model for emp_tb
from ..schemas import EmployeeBase, EmployeeUpdate  # Pydantic Schema

emp_router = APIRouter(prefix="/employee", tags=["Employee Table"])

#show all employee
@emp_router.get('/')
def show_all_employee(db:Session=Depends(get_db_dependency)):
    employees = db.query(EmployeeTable).all()
    return employees

# adding new Employee In the Database
@emp_router.post("/add")
def add_employee(employee: EmployeeBase, db: Session = Depends(get_db_dependency)):
    if employee.dept_id == 0:
        raise HTTPException(
            status_code=400, detail="Department Id Should not be 0")
    elif employee.emp_email == '':
        raise HTTPException(status_code=400, detail="Enter the Valid E-Mail")
    elif employee.emp_name == '':
        raise HTTPException(status_code=400, detail="Enter the Valid Name")
    elif employee.emp_mobile == '':
        raise HTTPException(
            status_code=400, detail="Enter the Valid Mobile Number")
    elif len(str(employee.emp_mobile)) == 0 | len(str(employee.emp_mobile)) < 10:
        raise HTTPException(
            status_code=400, detail="Enter the Valid 10 digit Mobile Number")
    else:
        try:
            new_employee = EmployeeTable(**employee.model_dump())
            db.add(new_employee)
            db.commit()
            db.refresh(new_employee)
            return {"Message" : f"The New Employee IS added have employee ID = {new_employee.emp_id}"}
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=500, detail=f"Unexpected error: {e}")

# Reading the Employee Via Employee ID
@emp_router.get("/{emp_id}")
def get_employee(emp_id: int, db: Session = Depends(get_db_dependency)):
    employee = db.query(EmployeeTable).filter(
        EmployeeTable.emp_id == emp_id).first()
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    return employee

# Updating the Employee Detail
@emp_router.put("/{emp_id}")
def update_employee(emp_id: int, employee: EmployeeUpdate, db: Session = Depends(get_db_dependency)):
    if employee.dept_id == 0:
        raise HTTPException(
            status_code=400, detail="Department Id Should not be 0")
    elif employee.emp_email == '':
        raise HTTPException(status_code=400, detail="Enter the Valid E-Mail")
    elif employee.emp_name == '':
        raise HTTPException(status_code=400, detail="Enter the Valid Name")
    elif employee.emp_mobile == '':
        raise HTTPException(
            status_code=400, detail="Enter the Valid Mobile Number")
    elif len(str(employee.emp_mobile)) == 0 | len(str(employee.emp_mobile)) < 10:
        raise HTTPException(
            status_code=400, detail="Enter the Valid 10 digit Mobile Number")
    else:
        existing_employee = db.query(EmployeeTable).filter(
            EmployeeTable.emp_id == emp_id).first()
        if not existing_employee:
            raise HTTPException(status_code=404, detail="Employee not found")
        for key, value in employee.dict(exclude_unset=True).items():
            setattr(existing_employee, key, value)
        db.commit()
        db.refresh(existing_employee)
        return existing_employee
