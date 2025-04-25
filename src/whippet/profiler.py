import platform
import time
import psutil
import subprocess
import os
from rich.console import Console
from shutil import which

console = Console()

def detect_hardware():
    console.print("[bold]🔍 Detecting Hardware...")
    return {
        "cpu": platform.processor(),
        "cores": psutil.cpu_count(logical=False),
        "ram_gb": round(psutil.virtual_memory().total / 1e9, 2),
        "os": platform.system()
    }

def get_llama_bin(cli_path=None):
    # 1. CLI flag overrides everything
    if cli_path and os.path.isfile(cli_path):
        return cli_path

    # 2. Environment variable
    env_path = os.environ.get("LLAMA_BIN")
    if env_path and os.path.isfile(env_path):
        return env_path

    # 3. Try to find it on PATH
    found = which("llama")
    if found:
        return found

    # 4. Default fallback (optional, your build path)
    default_path = "./llama.cpp/build/bin/llama"
    if os.path.isfile(default_path):
        return default_path

    raise FileNotFoundError("❌ Could not locate `llama` binary. Set it via --llama-bin or LLAMA_BIN env variable.")

def run_inference(model_path, prompt, simulate_cores=None, llama_bin_path=None):
    llama_bin = get_llama_bin(llama_bin_path)
    
    cmd = [
        llama_bin,
        f"file://{model_path}",
        prompt
    ]

    env = os.environ.copy()
    if simulate_cores:
        env["OMP_NUM_THREADS"] = str(simulate_cores)

    print("🚀 Running:", " ".join(cmd))
    
    start = time.perf_counter()
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=env)
    end = time.perf_counter()

    output = result.stdout.decode()
    errors = result.stderr.decode()

    if not output.strip():
        print("⚠️ llama-run returned no output.")
        print("🔧 STDERR:\n", errors)

    tokens = len(output.split())
    tps = tokens / (end - start) if end > start else 0

    return {
        "output": output,
        "tokens/sec": round(tps, 2),
        "duration": round(end - start, 2)
    }



def profile_model(model_path, prompt, simulate_cores=None, llama_bin_path=None):
    specs = detect_hardware()
    bench = run_inference(model_path, prompt, simulate_cores, llama_bin_path)

    console.print("\n[bold green]🧪 Benchmark Results")
    console.print(f"🧠 CPU: {specs['cpu']}")
    console.print(f"💾 RAM: {specs['ram_gb']} GB")
    console.print(f"🚀 Tokens/sec: {bench['tokens/sec']}")
    console.print(f"⏱️ Duration: {bench['duration']}s")
    console.print(f"📤 Output: {bench['output'][:200]}...")

    return bench

