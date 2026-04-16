"""
ETL для загрузки геообъектов из Excel/CSV в PostgreSQL+PostGIS.
Очистка координат, валидация геометрии, дедупликация.
"""

import pandas as pd
import psycopg2
from shapely import wkt
from shapely.validation import explain_validity

def validate_geometry(geom_wkt):
    try:
        geom = wkt.loads(geom_wkt)
        if geom.is_valid:
            return geom.wkt
        else:
            print(f"Invalid geometry: {explain_validity(geom)}")
            return None
    except:
        return None

def main():
    df = pd.read_excel('gis_objects.xlsx')
    
    # Очистка
    df['geometry_wkt'] = df['wkt'].apply(validate_geometry)
    df = df.dropna(subset=['geometry_wkt'])
    df = df.drop_duplicates(subset=['external_id'])
    
    conn = psycopg2.connect("dbname=gis user=analyst")
    cur = conn.cursor()
    
    for _, row in df.iterrows():
        cur.execute("""
            INSERT INTO spatial_objects (object_guid, layer_id, geometry, attributes)
            VALUES (%s, %s, ST_GeomFromText(%s, 3857), %s)
            ON CONFLICT (object_guid) DO UPDATE
            SET geometry = EXCLUDED.geometry, updated_at = NOW()
        """, (row['guid'], row['layer_id'], row['geometry_wkt'], row['attrs']))
    
    conn.commit()
    cur.close()
    conn.close()
    print(f"Loaded {len(df)} objects")

if __name__ == "__main__":
    main()
