from fastapi import FastAPI
from .database import get_db
from .routers import auth, users, courses
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(
    title="ADDLearn"
)

print(get_db)

origins = ["http://localhost:5173", "http://localhost:3000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.get("/")
def home():
    return {
        "message": "Welcome to ADDLearn"
    }

app.include_router(auth.routers)
app.include_router(users.routers)
app.include_router(courses.routers)