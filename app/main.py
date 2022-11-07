import uvicorn
from fastapi import FastAPI, Request, Response
from app.endpoints.home import home
from app.endpoints.users import profile, users, auth
from app.endpoints.notes import notes
from app.endpoints.posts import posts
from app.endpoints.admin import admin
from app.db.database import SessionLocal


tags_metadata = [
    {
        "name": "authorization",
        "description": "User registration, authentication and authorization",
    },
    {
        "name": "users",
        "description": "Operation with users",
    },
    {
        "name": "notes",
        "descriprion": "Operation with users's notes.",
    },
    {
        "name": "posts",
        "description": "Operation with posts",
    },
    {
        "name": "admin",
        "description": "Admin-panel",
    },
]


description = """
This API service provides the ability to create personal notes with the ability to edit them, public posts visible to 
other users of the platform, as well as a system for subscribing to users and adding them to friends (whose posts will 
be displayed on the home page).

**Main functionality:**
* **Registration and authorization of users**
* **Create personal notes and public posts**
* **Editing private notes and public posts**
* **System of subscriptions and friends**
* **Demo admin-panel (refinement of table links in the database is required)**
"""


app = FastAPI(
        openapi_url="/api/v1/openapi.json",
        redoc_url=None,
        title="Pet-project on Fast-API: notes | posts",
        description=description,
        version='0.0.1',
        contact={
            "name": "ZRR",
            "url": "https://github.com/ZRR1498",
        }
)


app.include_router(router=auth.router)
app.include_router(router=home.router)
app.include_router(router=profile.router)
app.include_router(router=users.router)
app.include_router(router=notes.router)
app.include_router(router=posts.router)
app.include_router(router=admin.router)


@app.middleware("http")
async def db_session_middleware(request: Request, call_next):
    try:
        request.state.db = SessionLocal()
        response = await call_next(request)
    except ConnectionError as e:
        response = Response("Internal server error" + str(e), status_code=500)
    finally:
        request.state.db.close()
    return response


def get_db(request: Request):
    return request.state.db


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
