from fastapi import APIRouter

router = APIRouter()


@router.post("/")
def create_feedback():
    feedback = ...
    if feedback is None:
        pass
