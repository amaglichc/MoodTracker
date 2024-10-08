from fastapi import HTTPException

UserNotFoundException = HTTPException(status_code=404, detail="User not found")
UserAlreadyExistException = HTTPException(
    status_code=409, detail="User with this email or username already created"
)
TokenException = HTTPException(status_code=403, detail="Your token has wrong")
WrongCredentialsException = HTTPException(
    status_code=404, detail="Email or Password are wrong"
)
InActiveUserException = HTTPException(status_code=403, detail="User is not active")
