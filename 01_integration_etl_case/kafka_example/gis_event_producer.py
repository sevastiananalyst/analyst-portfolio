from kafka import KafkaProducer
import json

producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

# Событие при добавлении нового объекта
event = {
    "event_type": "spatial_object_created",
    "object_id": 123456,
    "layer_id": 5,
    "geometry_centroid": [30.3, 59.95],
    "timestamp": "2025-10-01T12:00:00"
}
producer.send('gis_events', value=event)
producer.flush()
