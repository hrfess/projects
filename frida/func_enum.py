import frida
import sys

output_file = "method_trace.txt"

def on_message(message, data):
    if message["type"] == "send":
        print(message["payload"])
        with open(output_file, "a") as f:
            f.write(message["payload"] + "\n")
    elif message["type"] == "error":
        print("[!] Error:", message["stack"])

package_name = sys.argv[1]

device = frida.get_usb_device()
pid = device.spawn([package_name])
session = device.attach(pid)

with open(output_file, "w") as f:
    f.write("Tracing method calls for: {}\n\n".format(package_name))

with open("trace_methods.js") as f:
    script = session.create_script(f.read())

script.on("message", on_message)
script.load()
device.resume(pid)

print(f"[*] Tracing started. Output will be saved to {output_file}")
sys.stdin.read()
