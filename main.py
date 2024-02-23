from fastapi import FastAPI
import uvicorn
from create_tables import CreateTables
from routers.employees_router import router as employees_router
from routers.tasks_router import router as tasks_router
from routers.queries_router import router as queries_router


create_tables = CreateTables()
create_tables.create_tables()

app = FastAPI()
app.include_router(employees_router)
app.include_router(tasks_router)
app.include_router(queries_router)


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
