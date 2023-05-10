from typing import List, Optional
from pydantic import BaseModel, Field


class ChapterSchema(BaseModel):
    title: str = Field(...)
    contents: str = Field(...)


class CourseSchema(BaseModel):
    name: str = Field(...)
    date: int = Field(...)
    description: str = Field(...)
    domain: List[str] = Field(...)
    chapters: List[ChapterSchema] = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "name": "Introduction to Data Science",
                "date": 1643635200,
                "description": "This course covers the basics of data science and machine learning.",
                "domain": ["Data Science", "Machine Learning"],
                "chapters": [
                    {
                        "title": "Chapter 1: Introduction",
                        "contents": "In this chapter, we'll discuss the basics of data science and machine learning."
                    },
                    {
                        "title": "Chapter 2: Data Cleaning",
                        "contents": "In this chapter, we'll learn how to clean and preprocess data for analysis."
                    }
                ]
            }
        }

def ResponseModel(data, message):
    return {
        "data": [data],
        "code": 200,
        "message": message,
    }


def ErrorResponseModel(error, code, message):
    return {"error": error, "code": code, "message": message}