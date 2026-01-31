import pandas as pd
from sqlalchemy import create_engine
import config

def get_engine():
    """Returns SQLAlchemy engine for PostgreSQL."""
    db_url = f"postgresql://{config.DB_USER}:{config.DB_PASS}@{config.DB_HOST}:{config.DB_PORT}/{config.DB_NAME}"
    return create_engine(db_url)

def get_all_cars():
    """Fetches all car data from the view."""
    engine = get_engine()
    df = pd.read_sql("SELECT * FROM v_full_data", engine)
    return df

def get_brand_stats():
    """Fetches aggregated brand statistics."""
    engine = get_engine()
    df = pd.read_sql("SELECT * FROM v_brand_analytics ORDER BY total_ads DESC", engine)
    return df