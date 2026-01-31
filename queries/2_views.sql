DROP VIEW IF EXISTS v_full_data;
DROP VIEW IF EXISTS v_brand_analytics;

CREATE OR REPLACE VIEW v_full_data AS
SELECT 
    l.id,
    b.brand_name,
    m.model_name,
    l.year,
    l.price,
    l.title,
    l.link
FROM listings l
JOIN models m ON l.model_id = m.model_id
JOIN brands b ON m.brand_id = b.brand_id;

CREATE OR REPLACE VIEW v_brand_analytics AS
WITH brand_metrics AS (
    SELECT 
        b.brand_name,
        COUNT(l.id) as total_ads,
        AVG(l.price) as avg_price,
        MAX(l.price) as max_price
    FROM listings l
    JOIN models m ON l.model_id = m.model_id
    JOIN brands b ON m.brand_id = b.brand_id
    GROUP BY b.brand_name
)
SELECT 
    brand_name,
    total_ads,
    CAST(avg_price AS INTEGER) as avg_price,
    max_price,
    DENSE_RANK() OVER (ORDER BY total_ads DESC) as rank_by_popularity
FROM brand_metrics;