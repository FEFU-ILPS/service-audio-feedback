from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
import platform
import socket
import datetime

router = APIRouter(prefix="/health")


@router.get(path="", summary="Health Check", tags=["Health"])
async def health_check() -> JSONResponse:
    """Подтверждает работоспособность сервиса, отправляя данные о текущей хост-системе."""
    try:
        health_status = {
            "status": "healthy",
            "system": {
                "hostname": socket.gethostname(),
                "os": platform.system(),
                "os_version": platform.version(),
            },
            "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        }

        return JSONResponse(content=health_status)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Health check failed: {str(e)}")
