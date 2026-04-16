-- 1. Удаление дублей геометрий в одном слое
WITH duplicates AS (
    SELECT 
        id,
        ROW_NUMBER() OVER (
            PARTITION BY layer_id, ST_AsBinary(geometry) 
            ORDER BY created_at
        ) AS rn
    FROM spatial_objects
    WHERE geometry IS NOT NULL
)
DELETE FROM spatial_objects
WHERE id IN (SELECT id FROM duplicates WHERE rn > 1);

-- 2. Пространственный запрос: найти объекты в радиусе 500 м от точки
SELECT 
    so.id,
    l.name AS layer_name,
    ST_Distance(so.geometry, ST_SetSRID(ST_MakePoint(30.3, 59.95), 3857)) AS distance
FROM spatial_objects so
JOIN layers l ON so.layer_id = l.id
WHERE ST_DWithin(so.geometry, ST_SetSRID(ST_MakePoint(30.3, 59.95), 3857), 500)
ORDER BY distance;

-- 3. Агрегация: количество объектов по слоям
SELECT 
    l.name,
    COUNT(so.id) AS obj_count,
    SUM(ST_Area(so.geometry)) AS total_area
FROM spatial_objects so
JOIN layers l ON so.layer_id = l.id
WHERE so.is_deleted = false
GROUP BY l.id;
