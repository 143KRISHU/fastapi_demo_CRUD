# automap_base is use to map the exixting table autmatically
from sqlalchemy.ext.automap import automap_base 
from ..db import engine

Base = automap_base()
Base.prepare(engine, reflect=True)

# Access tables as classes
EmployeeTable = Base.classes.emp_tb
DepartmentTable = Base.classes.dept_tb
ManagerTable = Base.classes.mngr_tb