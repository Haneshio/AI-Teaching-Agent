"""创建和连接数据库"""
from sqlalchemy.ext.asyncio import create_async_engine,async_sessionmaker
from backend.config import MySqlConfig
from datetime import datetime
from backend.db.document_models import Base, FileMeta


"""建表"""
# 1、创建引擎
mysql_config = MySqlConfig()
print(mysql_config.database_url)
engine=create_async_engine(
    mysql_config.database_url,
    echo=True,
)


# 2、创建session工厂
AsyncSession=async_sessionmaker(
    bind=engine, # 绑定的数据库引擎
    expire_on_commit=False,
)

# 3、建表
async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


# 4、创建session
async def get_database():
    async with AsyncSession() as session:
        try:
            yield session
            await session.commit()
        except Exception as e:
            await session.rollback()
            raise e
        finally:
            await session.close()




