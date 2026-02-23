import asyncpg
from typing import Optional
from config import POSTGRES_HOST, POSTGRES_PORT, POSTGRES_DB, POSTGRES_USER, POSTGRES_PASSWORD

# Global connection pool
pool: Optional[asyncpg.pool.Pool] = None

async def create_pool() -> asyncpg.pool.Pool:
    """Create a global asyncpg pool if it doesn't exist and return it."""
    global pool
    if pool is None:
        pool = await asyncpg.create_pool(
            host=POSTGRES_HOST,
            port=POSTGRES_PORT,
            database=POSTGRES_DB,
            user=POSTGRES_USER,
            password=POSTGRES_PASSWORD,
            min_size=1,
            max_size=5,
        )
    return pool

async def init_db(pool: asyncpg.pool.Pool) -> None:
    """Ensure the check_requests table exists."""
    async with pool.acquire() as conn:
        await conn.execute(
            """
            CREATE TABLE IF NOT EXISTS check_requests (
                id SERIAL PRIMARY KEY,
                query TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT NOW()
            )
            """
        )

async def log_request(pool: asyncpg.pool.Pool, query: str) -> None:
    """Insert a query record into the check_requests table."""
    async with pool.acquire() as conn:
        await conn.execute(
            "INSERT INTO check_requests (query) VALUES ($1)",
            query,
        )
