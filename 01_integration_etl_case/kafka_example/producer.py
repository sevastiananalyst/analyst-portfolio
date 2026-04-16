from kafka import KafkaProducer
import json
import uuid
from datetime import datetime

# Настройка producer (адрес брокера, сериализация JSON)
producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    value_serializer=lambda v: json.dumps(v, default=str).encode('utf-8')
)

# Топик, в который будем отправлять события
TOPIC = 'gis_events'

def send_object_event(event_type, object_id, layer_id, geometry_centroid, user):
    """
    Отправить событие об изменении геообъекта.
    event_type: 'created', 'updated', 'deleted'
    """
    event = {
        "event_id": str(uuid.uuid4()),
        "event_type": f"spatial_object_{event_type}",
        "object_id": object_id,
        "layer_id": layer_id,
        "geometry_centroid": geometry_centroid,  # [lon, lat]
        "user": user,
        "timestamp": datetime.utcnow().isoformat()
    }
    future = producer.send(TOPIC, value=event)
    # Дожидаемся подтверждения (для синхронной отправки)
    record_metadata = future.get()
    print(f"Sent event {event['event_id']} to partition {record_metadata.partition} at offset {record_metadata.offset}")

# Примеры вызовов
if __name__ == "__main__":
    send_object_event('created', 1001, 5, [30.3, 59.95], 'sevastian')
    send_object_event('updated', 1002, 3, [30.4, 59.96], 'analyst')
    send_object_event('deleted', 1003, 7, [30.5, 59.97], 'integrator')
