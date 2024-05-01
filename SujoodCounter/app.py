from flask import Flask, render_template, jsonify
from zeroconf import Zeroconf, ServiceInfo
import socket
import sujood_counter

app = Flask(__name__)

# Define Zeroconf and service info at a global scope
zeroconf = Zeroconf()
service_type = "_http._tcp.local."
service_name = "SujoodCounter1._http._tcp.local."
service_port = 5001
desc = {'path': '/'}

# You need to compute the address and server outside of the function to ensure it is available when unregistered.
hostname = socket.gethostname()
addresses = [socket.inet_aton(socket.gethostbyname(hostname))]
info = ServiceInfo(
    type_=service_type,
    name=service_name,
    addresses=addresses,
    port=service_port,
    properties=desc,
    server=hostname + "."
)

def register_service():
    zeroconf.register_service(info)
    print("Service registered")

def unregister_service():
    zeroconf.unregister_service(info)
    zeroconf.close()
    print("Service unregistered")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/count')
def count():
    return jsonify(rakat_count=sujood_counter.get_rakat_count())

@app.route('/reset', methods=['POST'])
def reset():
    sujood_counter.reset_counter()
    return jsonify(message="Counter reset successfully"), 200

if __name__ == '__main__':
    try:
        register_service()
        sujood_counter.start_counter()
        app.run(host='0.0.0.0', port=5001, use_reloader=False)
    finally:
        unregister_service()
