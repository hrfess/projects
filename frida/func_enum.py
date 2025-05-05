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

# Wait until the gadget becomes available (when the app starts)
device = frida.get_usb_device(timeout=5)

# Attach to the package by name — works with Frida Gadget/ZygiskFrida
print(f"[*] Waiting for {package_name} to be ready...")
while True:
    try:
        session = device.attach(package_name)
        break
    except frida.ProcessNotFoundError:
        time.sleep(1)

print(f"[*] Attached to {package_name}")

# Open and load the script
with open("trace_methods.js") as f:
    script = session.create_script(f.read())

script.on("message", on_message)

# Write header
with open(output_file, "w") as f:
    f.write(f"Tracing Java method calls for: {package_name}\n\n")

script.load()

print(f"[*] Tracing started. Output will be saved to {output_file}")
print("[*] Press Ctrl+C to stop.")

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("\n[*] Detaching...")
    session.detach()
