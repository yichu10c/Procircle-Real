from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.schema import MetaData

metadata = MetaData()
Base = declarative_base(metadata=metadata)
