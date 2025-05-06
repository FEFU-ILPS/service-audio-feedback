import uvicorn

from configs import configs

if __name__ == "__main__":
    uvicorn.run(
        "app:service",
        host="0.0.0.0",
        port=8067,
        reload=configs.DEBUG_MODE,
        date_header=True,
        use_colors=True,
    )
