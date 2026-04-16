-- 1. Поиск дублей геометрий с использованием оконной функции
WITH duplicates AS (
    SELECT 
        id,
        layer_id,
        ST_AsText(geometry) AS geom_text,
        ROW_NUMBER() OVER (
            PARTITION BY layer_id, ST_Equals(geometry, geometry) 
            ORDER BY created_at
        ) AS rn
    FROM spatial_objects
)
DELETE FROM spatial_objects
WHERE id IN (SELECT id FROM duplicates WHERE rn > 1);

-- 2. Пространственный запрос: найти все объекты в радиусе 500 м от точки
SELECT 
    so.id,
    l.name AS layer_name,
    ST_Distance(so.geometry, ST_SetSRID(ST_MakePoint(30.3, 59.95), 3857)) AS distance
FROM spatial_objects so
JOIN layers l ON so.layer_id = l.id
WHERE ST_DWithin(so.geometry, ST_SetSRID(ST_MakePoint(30.3, 59.95), 3857), 500)
ORDER BY distance;

-- 3. Агрегация: количество объектов по слоям с динамической атрибутикой
SELECT 
    l.name,
    COUNT(so.id) AS obj_count,
    SUM(so.area) AS total_area
FROM spatial_objects so
JOIN layers l ON so.layer_id = l.id
WHERE so.is_deleted = false
GROUP BY l.id;
