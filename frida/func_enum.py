import frida
import sys

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

print(f"[*] Waiting for {package_name} to spawn...")
pid = device.on("spawn-added", lambda p: print(f"[+] Spawned: {p}"))

# Intercept spawn
spawn = device.spawn([package_name])
print(f"[*] Spawn intercepted (PID {spawn})")

# Attach to the spawned process
session = device.attach(spawn)

# Load the script
with open("trace_methods.js") as f:
    script = session.create_script(f.read())

script.on("message", on_message)
script.load()

# Resume the process after script is loaded
device.resume(spawn)
print(f"[*] Tracing started for {package_name}. Output goes to {output_file}")
print("[*] Press Ctrl+C to stop.")

try:
    with open(output_file, "w") as f:
        f.write(f"Tracing Java method calls for: {package_name}\n\n")
    import time
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("\n[*] Detaching...")
    session.detach()
