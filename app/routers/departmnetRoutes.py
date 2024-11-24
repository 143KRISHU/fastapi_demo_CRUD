from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..Models import DepartmentTable  # SQLAlchemy model for emp_tb
from ..schemas import DepartmentBase  # Pydantic Schema
from .dbDependency import get_db_dependency

dept_router = APIRouter(prefix="/department", tags=["Department Table"])

#show all department
@dept_router.get('/')
def show_all_department(db:Session=Depends(get_db_dependency)):
    departments = db.query(DepartmentTable).all()
    return departments

#add department to Database
@dept_router.post('/add')
def add_department(department:DepartmentBase,db:Session=Depends(get_db_dependency)):
    if department.mngr_id == 0 :
        raise HTTPException(
            status_code=400, detail="Department Id Should not be 0")
    elif department.dept_name == '':
        raise HTTPException(
            status_code=400, detail="Department Name can't be Emplty or Null")
    else:
      try:
          new_department = DepartmentTable(**department.model_dump())
          db.add(new_department)
          db.commit()
          db.refresh(new_department)
          return {"Message" : f"The New Department is added have DepartmentID = {new_department.dept_id}"}
      except Exception as e:
          db.rollback()
          raise HTTPException(status_code=500, detail=f"Unexpected error: {e}")
        
#get specific deaprtment data
@dept_router.get('/{dept_id}')
def get_department(dept_id:int,db:Session=Depends(get_db_dependency)):
    department = db.query(DepartmentTable).filter(
        DepartmentTable.dept_id == dept_id).first()
    if not department:
        raise HTTPException(status_code=404, detail=f"Departmnet with specific ID = {dept_id} not found")
    return department