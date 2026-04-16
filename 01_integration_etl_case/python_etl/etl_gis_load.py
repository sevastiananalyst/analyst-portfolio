"""
ETL для загрузки геообъектов из Excel/CSV в PostgreSQL+PostGIS.
Поддерживает преобразование систем координат: WGS84 (4326) -> Web Mercator (3857).
Трансформер создаётся один раз для производительности.
"""

import pandas as pd
import psycopg2
from shapely import wkt
from shapely.validation import explain_validity
from shapely.ops import transform
import pyproj

# Константы SRID
SRID_SOURCE = 4326   # WGS84 (широта/долгота)
SRID_TARGET = 3857   # Web Mercator (метры)

# Создаём трансформер ОДИН РАЗ (вне функции apply)
transformer = pyproj.Transformer.from_crs(
    f"EPSG:{SRID_SOURCE}", f"EPSG:{SRID_TARGET}", 
    always_xy=True
)

def validate_and_transform_geometry(geom_wkt: str):
    """
    Проверяет геометрию, преобразует из source_srid в target_srid.
    Возвращает WKT в целевой SRID или None.
    """
    try:
        geom = wkt.loads(geom_wkt)
        if not geom.is_valid:
            print(f"Invalid geometry: {explain_validity(geom)}")
            return None
        # Используем глобальный трансформер
        geom_transformed = transform(transformer.transform, geom)
        return geom_transformed.wkt
    except Exception as e:
        print(f"Error processing geometry: {e}")
        return None

def main():
    # 1. Extract
    df = pd.read_excel('gis_objects.xlsx')
    
    # 2. Transform (apply использует предсозданный трансформер)
    df['geometry_wkt_target'] = df['wkt'].apply(validate_and_transform_geometry)
    df = df.dropna(subset=['geometry_wkt_target'])
    df = df.drop_duplicates(subset=['external_id'])
    
    # 3. Load
    conn = psycopg2.connect(
        host="localhost",
        database="gis_db",
        user="analyst",
        password="******"  # используйте переменные окружения!
    )
    cur = conn.cursor()
    
    # Создание таблицы с пространственным индексом
    cur.execute("""
        CREATE TABLE IF NOT EXISTS spatial_objects (
            id SERIAL PRIMARY KEY,
            external_id VARCHAR(100) UNIQUE,
            layer_id INTEGER,
            geometry GEOMETRY(Geometry, 3857),
            attributes JSONB,
            created_at TIMESTAMP DEFAULT NOW()
        );
        CREATE INDEX IF NOT EXISTS idx_geometry ON spatial_objects USING GIST (geometry);
    """)
    
    # Вставка с явным указанием SRID
    for _, row in df.iterrows():
        cur.execute("""
            INSERT INTO spatial_objects (external_id, layer_id, geometry, attributes)
            VALUES (%s, %s, ST_SetSRID(ST_GeomFromText(%s), %s), %s)
            ON CONFLICT (external_id) DO UPDATE
            SET geometry = EXCLUDED.geometry,
                attributes = EXCLUDED.attributes,
                created_at = NOW();
        """, (
            row['external_id'],
            row['layer_id'],
            row['geometry_wkt_target'],
            SRID_TARGET,
            row['attrs']
        ))
    
    conn.commit()
    cur.close()
    conn.close()
    print(f"Loaded {len(df)} objects with SRID conversion {SRID_SOURCE} -> {SRID_TARGET}")

if __name__ == "__main__":
    main()
