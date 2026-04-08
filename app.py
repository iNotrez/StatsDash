from flask import Flask, jsonify, render_template
import psutil
import time

app = Flask(__name__)
_net_last = {"bytes_sent": 0, "bytes_recv": 0, "time": time.time()}


def get_net_speed():
    global _net_last
    counters = psutil.net_io_counters()
    now = time.time()
    elapsed = now - _net_last["time"]
    if elapsed <= 0:
        return 0, 0
    sent_speed = (counters.bytes_sent - _net_last["bytes_sent"]) / elapsed
    recv_speed = (counters.bytes_recv - _net_last["bytes_recv"]) / elapsed
    _net_last = {
        "bytes_sent": counters.bytes_sent,
        "bytes_recv": counters.bytes_recv,
        "time": now,
    }
    return sent_speed, recv_speed


def fmt_bytes(b):
    for unit in ["B", "KB", "MB", "GB"]:
        if b < 1024:
            return f"{b:.1f} {unit}/s"
        b /= 1024
    return f"{b:.1f} TB/s"


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/stats")
def stats():
    cpu = psutil.cpu_percent(interval=None)
    ram = psutil.virtual_memory()
    disk = psutil.disk_usage("/")
    sent, recv = get_net_speed()
    return jsonify(
        {
            "cpu": {"percent": cpu, "label": f"{cpu:.1f}%"},
            "ram": {
                "percent": ram.percent,
                "used": f"{ram.used / 1e9:.1f} GB",
                "total": f"{ram.total / 1e9:.1f} GB",
                "label": f"{ram.percent:.1f}%",
            },
            "disk": {
                "percent": disk.percent,
                "used": f"{disk.used / 1e9:.1f} GB",
                "total": f"{disk.total / 1e9:.1f} GB",
                "label": f"{disk.percent:.1f}%",
            },
            "net": {"sent": fmt_bytes(sent), "recv": fmt_bytes(recv)},
        }
    )


if __name__ == "__main__":
    # Pre-warm net stats
    psutil.net_io_counters()
    _net_last["bytes_sent"] = psutil.net_io_counters().bytes_sent
    _net_last["bytes_recv"] = psutil.net_io_counters().bytes_recv
    print("[StatsDash] Running at http://localhost:5000")
    app.run(debug=False, host="0.0.0.0", port=5000)
