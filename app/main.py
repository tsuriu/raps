from fastapi import FastAPI

from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.routers import auth, user, raffle, purchase, noauth, hooks, payment, parameters

app = FastAPI()

origins = [
    settings.CLIENT_ORIGIN,
]
#
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(auth.router, tags=['Auth'], prefix='/api/auth')
app.include_router(user.router, tags=['Users'], prefix='/api/users')
app.include_router(purchase.router, tags=['Purchases'], prefix='/api/purchases')
app.include_router(raffle.router, tags=['Raffles'], prefix='/api/raffles')
app.include_router(noauth.router, tags=['NoAuth'], prefix='/api/noauth')
app.include_router(hooks.router, tags=["Hooks"], prefix='/api/hook')
app.include_router(payment.router, tags=["Payments"], prefix='/api/payment')
app.include_router(parameters.router, tags=["Parameters"], prefix="/api/config")


@app.get("/api/healthchecker")
def root():
    return {"message": "Welcome to FastAPI with MongoDB"}