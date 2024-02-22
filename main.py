from fastapi import FastAPI
import uvicorn
from create_tables import CreateTables
from database import connect_base
from employees_router import router as employees_router


cur = connect_base()

create_tables = CreateTables()
create_tables.create_tables()

app = FastAPI()
app.include_router(employees_router)


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
