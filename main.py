from typing import Optional
from fastapi import FastAPI, HTTPException, Request, WebSocket
from fastapi.responses import HTMLResponse, JSONResponse, PlainTextResponse
from exception import StoryException
from templates import templates
from router import blog_get, blog_post, user, article, product, file, dependencies
from auth import authentication
from db import models
from db.database import engine
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from time import time
from client import html


app = FastAPI()
app.include_router(dependencies.router)
app.include_router(templates.router)
app.include_router(file.router)
app.include_router(authentication.router)
app.include_router(user.router)
app.include_router(article.router)
app.include_router(product.router)
app.include_router(blog_get.router)
app.include_router(blog_post.router)


# @app.get('/')
# def index():
#   return {'message': 'Hello dunia!'}

@app.exception_handler(StoryException)
def story_exception_handler(request: Request, exc: StoryException):
  return JSONResponse(
    status_code=418,
    content = {'detail':exc.name}
  )

@app.get("/")
async def get():
  return HTMLResponse(html)

clients = []

@app.websocket("/chat")
async def websocket_endpoint(websocket: WebSocket):
  await websocket.accept()
  clients.append(websocket)
  while True:
    data = await websocket.receive_text()
    for client in clients:
      await client.send_text(data)

# @app.exception_handler(HTTPException)
# def custom_handler(request: Request, exc: HTTPException):
#   return PlainTextResponse(status_code=400, content=exc.detail)

models.Base.metadata.create_all(engine)

@app.middleware("http")
async def add_middleware(request: Request, call_next):
  start_time = time()
  response = await call_next(request)
  duration = time() - start_time
  response.headers['duration'] = str(duration)
  return response

app.add_middleware(
  CORSMiddleware,
  allow_origins = ['http://localhost:3000'],
  allow_credentials = True,
  allow_methods = ['*'],
  allow_headers = ['*']
)

app.mount('/files', StaticFiles(directory="files"), name='files')
app.mount('/files', StaticFiles(directory="files"), name='files')
app.mount('/templates/static', 
      StaticFiles(directory="templates/static"),
      name="static"
)