from flask import Flask, request

class SmartMockInterview:
    def __init__(self):
        self.app = Flask(__name__)
        self.setup_routes()

    def setup_routes(self):
        @self.app.route("/message", methods=["GET","POST"])

        def receive_input():
            message = self.get_input_from_request()
            print(f"Received message: {message}")

    def get_input_from_request(self):
        if request.is_json:
            data =  request.get_json()
            return data.get("message", "")
        elif "message" in request.values:
            return request.values["message"]
        elif request.data:
            return request.data.decode("utf-8")
            return ""
        
    def run(self):
        self.app.run(debug=True)

if __name__ == "__main__":
    app = SmartMockInterview()
    app.run()
