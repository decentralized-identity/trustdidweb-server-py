import uvicorn
import asyncio
from app.plugins import AskarStorage

if __name__ == "__main__":
    asyncio.run(AskarStorage().provision())
    uvicorn.run(
        "app.api:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        # workers=4,
    )
