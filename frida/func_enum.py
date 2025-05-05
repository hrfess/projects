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

# Wait until the app is running
device = frida.get_usb_device(timeout=5)

# Find running process
print(f"[*] Waiting for {package_name} to appear...")
while True:
    try:
        pid = device.get_process(package_name).pid
        break
    except frida.ProcessNotFoundError:
        time.sleep(1)

# Attach to the process
session = device.attach(pid)
print(f"[*] Attached to {package_name} (PID: {pid})")

# Write header to the output file
with open(output_file, "w") as f:
    f.write(f"Tracing Java method calls for: {package_name}\n\n")

# Load JavaScript tracing script
with open("trace_methods.js") as f:
    script = session.create_script(f.read())

script.on("message", on_message)
script.load()

print(f"[*] Tracing started. Output will be saved to {output_file}")
print("[*] Press Ctrl+C to stop.")

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("\n[*] Stopped by user.")
    session.detach()
