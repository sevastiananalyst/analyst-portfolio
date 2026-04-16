from kafka import KafkaProducer
import json

producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

# Отправка события о новом акте
event = {
    "event_type": "doc_created",
    "document_id": 12345,
    "act_number": "КС-2-001",
    "status": "pending_pto"
}

producer.send('construction_docs', value=event)
producer.flush()
print("Событие отправлено")
