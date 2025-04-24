import platform
import time
import psutil
import subprocess
import os
from rich.console import Console

console = Console()

def detect_hardware():
    console.print("[bold]🔍 Detecting Hardware...")
    return {
        "cpu": platform.processor(),
        "cores": psutil.cpu_count(logical=False),
        "ram_gb": round(psutil.virtual_memory().total / 1e9, 2),
        "os": platform.system()
    }

def run_inference(model_path, prompt, simulate_cores=None):
    cmd = ["./llama.cpp/main", "-m", model_path, "-p", prompt]

    # Optional: simulate low-core device
    env = os.environ.copy()
    if simulate_cores:
        env["OMP_NUM_THREADS"] = str(simulate_cores)

    start = time.perf_counter()
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=env)
    end = time.perf_counter()

    output = result.stdout.decode()
    duration = end - start
    tokens = len(output.split())
    tps = tokens / duration if duration else 0

    return {
        "output": output,
        "tokens/sec": round(tps, 2),
        "duration": round(duration, 2)
    }

def profile_model(model_path, prompt, simulate_cores=None):
    specs = detect_hardware()
    bench = run_inference(model_path, prompt, simulate_cores)

    console.print("\n[bold green]🧪 Benchmark Results")
    console.print(f"🧠 CPU: {specs['cpu']}")
    console.print(f"💾 RAM: {specs['ram_gb']} GB")
    console.print(f"🚀 Tokens/sec: {bench['tokens/sec']}")
    console.print(f"⏱️ Duration: {bench['duration']}s")
    console.print(f"📤 Output: {bench['output'][:200]}...")

    return bench

