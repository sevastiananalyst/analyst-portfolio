"""
Пример Kafka Consumer для ГИС.
Слушает события и имитирует обновление статуса в БД или вызов API.
"""

from kafka import KafkaConsumer
import json

# Настройка consumer (адрес брокера, топик, десериализация)
consumer = KafkaConsumer(
    'gis_events',
    bootstrap_servers=['localhost:9092'],
    auto_offset_reset='earliest',   # начать с самого старого сообщения
    enable_auto_commit=True,
    group_id='gis_analytics_group',
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

def process_event(event):
    """Обработка события: логирование + имитация записи в БД."""
    event_type = event.get('event_type')
    object_id = event.get('object_id')
    print(f"[{event['timestamp']}] {event_type} for object {object_id}, layer {event['layer_id']}")
    
    # Здесь можно добавить вызов API для обновления статуса в ГИС
    # requests.post('http://gis-api/objects/sync', json=event)
    # или запись в БД через SQLAlchemy

if __name__ == "__main__":
    print("Starting Kafka consumer for GIS events...")
    for msg in consumer:
        event = msg.value
        process_event(event)
