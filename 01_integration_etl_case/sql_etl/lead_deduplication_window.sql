-- Задача: из таблицы сырых лидов удалить дубли по номеру телефона,
-- оставив только самую свежую запись (с максимальным created_at).
-- Используем оконную функцию ROW_NUMBER().

WITH ranked_leads AS (
    SELECT 
        id,
        phone,
        created_at,
        ROW_NUMBER() OVER (
            PARTITION BY phone 
            ORDER BY created_at DESC
        ) AS rn
    FROM raw_leads
    WHERE phone IS NOT NULL AND phone != ''
)
DELETE FROM raw_leads
WHERE id IN (
    SELECT id FROM ranked_leads WHERE rn > 1
);

-- Дополнительно: показать статистику по дублям до удаления
-- SELECT phone, COUNT(*) FROM raw_leads GROUP BY phone HAVING COUNT(*) > 1;
