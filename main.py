from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

import models
from database import engine, sessionLocal
from models import Todos
from routers import auth, todos, admin, users


# init Application function

@asynccontextmanager
async def lifespan(app: FastAPI):
    models.Base.metadata.create_all(engine)
    yield
    # with sessionLocal() as session:
    #     todoObj1 = Todos(title="Feed the Dog", description="He is hungry", priority=2, complete=False)
    #     todoObj2 = Todos(title="cut the lawn", description="grass is getting long", priority=1, complete=False)
    #     todoObj3 = Todos(title="Buy groceries", description="Buy milk and bread", priority=4, complete=False)
    #     session.add_all([todoObj1, todoObj2, todoObj3])
    #     session.commit()
    # yield
    # #  clean up
    # models.Base.metadata.drop_all(bind=engine)


app = FastAPI(lifespan=lifespan)

app.include_router(auth.router)
app.include_router(todos.router)
app.include_router(admin.router)
app.include_router(users.router)

# Debugging purpose
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
