import motor
from dotenv import dotenv_values
import pymongo
from bson.objectid import ObjectId

from server.models.Course import CourseSchema
from fastapi.encoders import jsonable_encoder
config = dotenv_values(".env")

MONGO_DETAILS = config["MONGODB_CONNECTION_URI"]
print(MONGO_DETAILS)
# client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS)
client = pymongo.MongoClient(MONGO_DETAILS)

database = client[config["DB_NAME"]]

if "courses" not in database.list_collection_names():
    database.create_collection("courses")

course_collection = database.get_collection("courses")

def course_helper(course) -> dict:
    return {
        "id": str(course["_id"]),
        "name": course["name"],
        "date": course["date"],
        "description": course["description"],
        "domain": course["domain"],
        "chapters": course["chapters"]
    }


async def add_course(course_data: CourseSchema) -> dict:
    course_data =  jsonable_encoder(course_data)
    course = await course_collection.insert_one(course_data)
    new_course = await course_collection.find_one({"_id": course.inserted_id})
    return course_helper(new_course)

async def get_Courses(query: dict,sort_order : list)->dict:
    courses = course_collection.find(query).sort(sort_order)
    courses_list = []
    for course in courses:
        courses_list.append(course_helper(course))
    return courses_list

def get_Course(course_id)->dict:
    course = course_collection.find_one({'_id': ObjectId(course_id)})
    return course_helper(course)