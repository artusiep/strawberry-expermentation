from sqlalchemy import MetaData
from sqlalchemy.orm import declarative_base

SCHEMA = "siep"
metadata_ = MetaData(schema=SCHEMA)
Base = declarative_base(metadata=metadata_)
