from fastapi import FastAPI
from api.auth import router as auth_router
from api.operations import router
from api.reports import router as reports_router

app = FastAPI(
    title='Budget App',
    version='1.0'
)
app.include_router(auth_router)
app.include_router(router)
app.include_router(reports_router)



