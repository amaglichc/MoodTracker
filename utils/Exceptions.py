from fastapi import HTTPException

UserNotFoundException = HTTPException(status_code=404,detail="User not found")
