from pydantic import BaseModel, EmailStr, Field

# Base Schema for shared attributes
class EmployeeBase(BaseModel):
    emp_name: str = Field(..., max_length=100, description="Name of the employee")
    emp_email: EmailStr = Field(..., description="Email of the employee")
    emp_mobile: int = Field(..., description="Mobile number of the employee")
    dept_id: int | None = Field(None, description="Department ID")


# Base Schema for department attributes
class DepartmentBase(BaseModel):
    dept_name : str = Field(..., max_length=100, description="Name of the Department")
    mngr_id: int | None = Field(None, description="Manager ID")

# Base Schema for Manager Atrribute
class Managerbase(BaseModel):
    mngr_name : str = Field(..., max_length=100, description="Name of the Manager")
