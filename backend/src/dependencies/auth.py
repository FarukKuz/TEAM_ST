from fastapi import Header, HTTPException, status
from backend.src.core.firebase_admin import verify_token

def get_current_user(authorization: str = Header(...)):
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Geçersiz token formatı.")

    token = authorization.split(" ")[1]
    decoded_token = verify_token(token)

    if decoded_token is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token doğrulanamadı.")

    return decoded_token 

