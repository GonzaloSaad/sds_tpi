from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from app.endpoints import calendar, oauth2

app = FastAPI()
app.include_router(oauth2.router)
app.include_router(calendar.router)


@app.get("/", response_class=HTMLResponse)
def index():
    return """
    <html>
        <head>
            <title>SDS App</title>
        </head>
        <body>
            <h1>Hello! Thanks for visiting SDS App!</h1>
        </body>
    </html>
    """


if __name__ == '__main__':
    from uvicorn import run

    run(app, port=8080)
