# auth.py (or wherever you keep your auth utilities in App B)
from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt
from typing import Dict
from datetime import datetime
from config import SERVICE_AUTH_KEY, SERVICE_AUTH_ALGORITHM  # Make sure this is consistent with App A

security = HTTPBearer()

def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)) -> Dict:
    token = credentials.credentials
    try:
        payload = jwt.decode(token, SERVICE_AUTH_KEY, algorithms=[SERVICE_AUTH_ALGORITHM])
        
        # Optional: check expiration manually (jwt does this too)
        exp = payload.get("exp")
        if exp and datetime.utcfromtimestamp(exp) < datetime.utcnow():
            raise HTTPException(status_code=401, detail="Token expired")

        return payload  # contains 'sub', 'role', etc.

    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")
