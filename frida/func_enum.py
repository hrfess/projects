import frida
import sys
import time

output_file = "method_trace.txt"
package_name = "com.android.vending"

def on_message(message, data):
    if message["type"] == "send":
        print(message["payload"])
        with open(output_file, "a") as f:
            f.write(message["payload"] + "\n")
    elif message["type"] == "error":
        print("[!] Error:", message["stack"])

device = frida.get_usb_device(timeout=5)
device.enable_spawn_gating()

print(f"[*] Waiting for spawn of {package_name}...")

def on_spawn_added(spawn):
    if spawn.identifier == package_name:
        print(f"[+] Spawn detected: {spawn.identifier}")
        pid = device.attach(spawn.pid)
        print(f"[+] Attached to {package_name} (PID: {spawn.pid})")

        with open(output_file, "w") as f:
            f.write(f"Tracing Java method calls for: {package_name}\n\n")

        with open("trace_methods.js") as f:
            script = pid.create_script(f.read())

        script.on("message", on_message)
        script.load()
        device.resume(spawn.pid)
        print("[*] Tracing started. Press Ctrl+C to stop.")

device.on("spawn-added", on_spawn_added)

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("\n[*] Exiting...")
