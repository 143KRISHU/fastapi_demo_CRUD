from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..Models import ManagerTable  # SQLAlchemy model for mngr_tb
from ..schemas import Managerbase  # Pydantic Schema
from .dbDependency import get_db_dependency

mngr_router = APIRouter(prefix="/manager", tags=["Manager Table"])

#show all department
@mngr_router.get('/')
def show_all_manager(db:Session=Depends(get_db_dependency)):
    managers = db.query(ManagerTable).all()
    return managers

#add department to Database
@mngr_router.post('/add')
def add_manager(department:Managerbase,db:Session=Depends(get_db_dependency)):
    if department.mngr_name == '' :
        raise HTTPException(
            status_code=400, detail="Provide Valid Manager Name")
    else:
      try:
          new_manager = ManagerTable(**department.model_dump())
          db.add(new_manager)
          db.commit()
          db.refresh(new_manager)
          return {"Message" : f"The New Department is added have DepartmentID = {new_manager.mngr_id}"}
      except Exception as e:
          db.rollback()
          raise HTTPException(status_code=500, detail=f"Unexpected error: {e}")