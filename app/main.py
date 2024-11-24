from fastapi import FastAPI
from .core import settings
from .routers import emp_router,dept_router,mngr_router


app = FastAPI()

#Employee Router
app.include_router(emp_router)

# Department Router
app.include_router(dept_router)

#Manager Router
app.include_router(mngr_router)


@app.get('/')
def root():
    return {
        "App_Name": f'{settings.APP_NAME}',
        "Message":"This is the Folder Structure FastAPI App"}