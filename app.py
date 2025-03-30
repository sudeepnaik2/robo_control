from flask import Flask, render_template, request, jsonify
import re
import requests

API_URL = "http://c23d6504-d0b7-485a-8f96-85aa01261ad7.centralindia.azurecontainer.io/score"

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/send_to_robot', methods=['POST'])
def send_to_robot():
    parsed_command_list = request.json  # Expecting a list of dicts
    print("📤 Sending to robot API:", parsed_command_list)

    try:
        response = requests.post(API_URL, json={
            "method": "POST",
            "body": {
                "command": parsed_command_list  # 👈 Wrap the list inside 'command'
            }
        })

        print("🤖 Robot API Response:", response.status_code, response.text)

        return jsonify({
            "message": "✅ Command sent to robot.",
            "status_code": response.status_code,
            "robot_response": response.json()
        })

    except Exception as e:
        print("❌ Error sending to robot:", str(e))
        return jsonify({
            "message": "❌ Failed to send command to robot.",
            "error": str(e)
        }), 500

@app.route('/send_command', methods=['POST'])
def send_command():
    user_text = request.json.get("command", "").lower()
    print("🎙️ Raw text:", user_text)

    # Split by "then" or ","
    steps = re.split(r'\bthen\b|,', user_text)
    result = []

    for step in steps:
        step = step.strip()
        cmd = {}

        if "move forward" in step:
            cmd["command"] = "move_forward"
            match = re.search(r'(\d+)\s*mm', step)
            if match:
                cmd["distance"] = int(match.group(1))

        elif "move backward" in step:
            cmd["command"] = "move_backward"
            match = re.search(r'(\d+)\s*mm', step)
            if match:
                cmd["distance"] = int(match.group(1))

        elif "turn left" in step or "take left" in step:
            cmd["command"] = "turn_left"

        elif "turn right" in step or "take right" in step:
            cmd["command"] = "turn_right"

        elif "rotate" in step:
            cmd["command"] = "rotate"

        elif "stop" in step:
            cmd["command"] = "stop"

        if cmd:  # Add only if valid
            result.append(cmd)

    print("🤖 Parsed commands:", result)

    return jsonify({"status": "success", "parsed": result})


if __name__ == '__main__':
    app.run(debug=False)
