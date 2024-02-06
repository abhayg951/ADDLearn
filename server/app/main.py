from fastapi import FastAPI
from .routers import auth, users, courses, categories, chapters
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.staticfiles import StaticFiles


app = FastAPI(docs_url=None, title="AddLearn")


@app.get("/", include_in_schema=False)
async def swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url="/openapi.json",
        title="ADDLearn",
        swagger_favicon_url="https://res.cloudinary.com/dnlomsnxb/image/upload/v1706818037/favicon/xth5pjxoazxn3yi2lhjn.ico"
    )

origins = ["http://localhost:5173", "http://localhost:3000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# @app.get("/")
# def home():
#     return {
#         "message": "Welcome to ADDLearn"
#     }

app.include_router(auth.routers)
app.include_router(users.routers)
app.include_router(courses.routers)
app.include_router(categories.routers)
app.include_router(chapters.routers)

if __name__ == "__main__":
    uvicorn.run("app.main:app", reload=True)