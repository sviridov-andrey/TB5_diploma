from fastapi import FastAPI
import uvicorn
from create_tables import CreateTables
from employees_router import router as employees_router
from tasks_router import router as tasks_router


create_tables = CreateTables()
create_tables.create_tables()

app = FastAPI()
app.include_router(employees_router)
app.include_router(tasks_router)


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
