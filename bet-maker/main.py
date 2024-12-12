from config.config import settings
from fastapi import FastAPI
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis.asyncio import Redis
from src.interfaces.auth import router_auth
from src.interfaces.bet import router_bet

app = FastAPI()


@app.on_event("startup")
async def startup():
    redis = await Redis.from_url(settings.redis.REDIS_URL)
    FastAPICache.init(RedisBackend(redis), prefix="cache")


app.include_router(router_auth, prefix="/api/v1", tags=["users"])
app.include_router(router_bet, prefix="/api/v1", tags=["bet"])
