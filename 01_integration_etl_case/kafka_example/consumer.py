from kafka import KafkaConsumer
import json

consumer = KafkaConsumer(
    'construction_docs',
    bootstrap_servers='localhost:9092',
    auto_offset_reset='earliest',
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

for msg in consumer:
    event = msg.value
    print(f"Получено событие: {event['event_type']} для документа {event['document_id']}")
    # Здесь можно добавить логику обновления статуса в БД
