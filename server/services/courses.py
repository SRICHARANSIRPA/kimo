
from typing import List, Optional
from server.utils import SORT_OPTIONS,FILTER_OPTIONS
from server.database import get_Course as getCourse,get_Courses as get_Filtered_Courses

def get_courses(sort ,domain) -> List[dict]:
    if sort:
        sort_order = SORT_OPTIONS.get(sort.lower(), [("date", "DESCENDING")])
    query = {}
    if domain is not None:
        query["domain"] = domain

    return get_Filtered_Courses(query,sort_order)

def get_course(course_id)-> dict:
    return getCourse(course_id=course_id)
