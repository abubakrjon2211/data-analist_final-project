import pandas as pd
import os
from sqlalchemy import create_engine, text
import config

def init_database():
    """Initializes PostgreSQL database and loads data."""
    csv_path = 'source/cars_raw.csv'

    if not os.path.exists(csv_path):
        return

    db_url = f"postgresql://{config.DB_USER}:{config.DB_PASS}@{config.DB_HOST}:{config.DB_PORT}/{config.DB_NAME}"
    engine = create_engine(db_url)

    raw_df = pd.read_csv(csv_path)

    with engine.connect() as conn:
        with open('queries/1_schema.sql', 'r') as f:
            commands = f.read().split(';')
            for cmd in commands:
                if cmd.strip():
                    conn.execute(text(cmd))
            conn.commit()

    df_brands = raw_df[['brand']].drop_duplicates().reset_index(drop=True)
    df_brands['brand_id'] = df_brands.index + 1
    df_brands = df_brands.rename(columns={'brand': 'brand_name'})
    
    df_models = raw_df[['brand', 'model']].drop_duplicates().reset_index(drop=True)
    df_models = df_models.merge(df_brands, left_on='brand', right_on='brand_name', how='left')
    df_models['model_id'] = df_models.index + 1
    df_models = df_models.rename(columns={'model': 'model_name'})

    temp_df = raw_df.merge(df_brands, left_on='brand', right_on='brand_name', how='left')
    df_listings = temp_df.merge(df_models, left_on=['brand_id', 'model'], right_on=['brand_id', 'model_name'], how='left')
    df_listings['id'] = df_listings.index + 1
    
    df_brands[['brand_id', 'brand_name']].to_sql('brands', engine, if_exists='append', index=False)
    df_models[['model_id', 'brand_id', 'model_name']].to_sql('models', engine, if_exists='append', index=False)
    df_listings[['id', 'model_id', 'year', 'price', 'title', 'link']].to_sql('listings', engine, if_exists='append', index=False)

    with engine.connect() as conn:
        with open('queries/2_views.sql', 'r') as f:
            commands = f.read().split(';')
            for cmd in commands:
                if cmd.strip():
                    conn.execute(text(cmd))
            conn.commit()

    print("PostgreSQL Database initialized successfully.")

if __name__ == "__main__":
    init_database()