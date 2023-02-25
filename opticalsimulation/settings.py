from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

path = 'sqlite:///test.db'
 
# Engine の作成
Engine = create_engine(
  path,
  echo=False
)
Base = declarative_base()