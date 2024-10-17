from flask import Flask, request
from kafka import KafkaProducer, KafkaConsumer
import threading

app = Flask(__name__)

producer = KafkaProducer(bootstrap_servers='kafka:9092')

def consume_messages():
    consumer = KafkaConsumer('service-b-topic', bootstrap_servers='kafka:9092', auto_offset_reset='earliest', group_id='group_id')
    for message in consumer:
        print(f"Received message from Service B: {message.value.decode('utf-8')}")

threading.Thread(target=consume_messages, daemon=True).start()

@app.route('/send', methods=['POST'])
def send_message():
    message = request.json.get('message')
    producer.send('service-a-topic', value=message.encode('utf-8'))
    return {"status": "Message sent to Service A"}, 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
