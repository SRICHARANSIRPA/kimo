
from datetime import datetime
import json
from server.database import course_collection
from dotenv import dotenv_values
from bson.objectid import ObjectId
config = dotenv_values(".env")

async def seed_courses() -> None:
    with open(config['COURSE_FILE'], "r") as file:
        courses = json.load(file)

    for course in courses:
        course["date"] = datetime.fromtimestamp(course["date"])
        course["domain"] = [domain.lower() for domain in course["domain"]]
        for chapter in course["chapters"]:
            chapter["name"] = chapter["name"].strip()
            chapter["text"] = chapter["text"].strip()
        print(course)
        course_collection.insert_one(course)
        