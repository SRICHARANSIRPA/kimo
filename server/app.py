from fastapi import FastAPI, Query
from typing import List, Optional
from server.services.courses import get_course as get_particular_course,get_courses as get_Filtered_Courses
from fastapi.middleware.cors import CORSMiddleware
from database import course_collection
from server.courses_seed import seed_courses
from bson.objectid import ObjectId
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins= ["*"] ,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Welcome to this fantastic Courses App!"}

@app.get("/courses/")
def get_Courses(sort: Optional[str] = Query(default=None, description="Sort the courses by one of the following options: alphabetical, date, rating"),
                domain: Optional[str] = Query(default=None, description="Filter the courses by domain")) -> List[dict]:
    return get_Filtered_Courses(sort,domain)


@app.get('/courses/{course_id}')
async def get_course(course_id: str):
    course = get_particular_course(course_id=course_id)
    if course is None:
        return {'message': 'Course not found'}
    return course


@app.get('/courses/{course_id}/chapters/{chapter_index}')
async def get_chapter(course_id: str, chapter_index: int):
    course = course_collection.find_one({'_id': ObjectId(course_id)})
    if course is None:
        return {'message': 'Course not found'}
    if chapter_index >= len(course['chapters']):
        return {'message': 'Chapter not found'}
    chapter = course['chapters'][chapter_index]
    return {'title': chapter['title'], 'contents': chapter['contents']}



@app.on_event("startup")
async def startup_db_client():
    await seed_courses()
    print("Seeding Done")
