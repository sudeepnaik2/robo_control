from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

# Set this to your ESP32's IP and endpoint
ESP32_API = "http://192.168.1.123:80/command"  # Replace with actual ESP32 IP

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/send_command', methods=['POST'])
def send_command():
    data = request.json
    print("Sending to ESP32:", data)

    try:
        response = requests.post(ESP32_API, json=data)
        return jsonify({"status": "success", "esp_response": response.text})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

if __name__ == '__main__':
    app.run(debug=True)
