from fastapi import FastAPI, Request, UploadFile, File
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
import pandas as pd
import sqlite3
import os

app = FastAPI()
templates = Jinja2Templates(directory="templates")

DB_NAME = "mydatabase.db"


def get_users():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    rows = cursor.fetchall()
    column_names = [desc[0] for desc in cursor.description]
    conn.close()
    return [dict(zip(column_names, row)) for row in rows]


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    users = []
    if os.path.exists(DB_NAME):
        try:
            users = get_users()
        except:
            users = []
    return templates.TemplateResponse("users.html", {"request": request, "users": users})


@app.post("/upload")
async def upload_excel(file: UploadFile = File(...)):
    contents = await file.read()
    with open("temp.xlsx", "wb") as f:
        f.write(contents)

    df = pd.read_excel("temp.xlsx")
    conn = sqlite3.connect(DB_NAME)
    df.to_sql("users", conn, if_exists="replace", index=False)
    conn.close()

    os.remove("temp.xlsx")

    return RedirectResponse("/", status_code=303)


@app.get("/api/users")
def api_users():
    return get_users()