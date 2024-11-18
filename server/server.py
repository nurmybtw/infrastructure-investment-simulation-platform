from fastapi import FastAPI
from routes import real_estate_investments
from routes import rating
from routes import data
from routes import ranking
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Allows specific origins
    allow_credentials=True,  # Allows cookies and credentials
    allow_methods=["*"],  # Allows all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers
)

app.include_router(
    real_estate_investments.router, 
    prefix="/real-estate-investments", 
    tags=["real-estate-investments"]
)

app.include_router(
    rating.router, 
    prefix="/rating", 
    tags=["rating"]
)

app.include_router(
    data.router, 
    prefix="/data", 
    tags=["data"]
)

app.include_router(
    ranking.router, 
    prefix="/ranking", 
    tags=["ranking"]
)