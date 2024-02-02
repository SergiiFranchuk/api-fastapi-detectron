from typing import Optional

from pydantic import BaseModel, Field


class TaskOut(BaseModel):
    task_id: str


class TaskResultOut(BaseModel):
    success: bool
    ready: bool
    result: Optional[list[dict[str, float]]] = Field(
        None,
        description="list of objects contained in the video with their probabilities for each of the frames.",
    )
    error: Optional[str]
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "success": True,
                    "ready": True,
                    "result": [
                        {"dog": 0.95, "cat": 0.85},
                        {"dog": 0.92, "cat": 0.89, "person": 0.97},
                    ],
                    "error": None,
                },
            ]
        }
    }
