import uvicorn

from api import app as application


if __name__ == '__main__':
    uvicorn.run('asgi:application', reload=True)
