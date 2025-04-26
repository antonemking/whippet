import platform
import time
import psutil
import subprocess
import os
from rich.console import Console
from shutil import which
from whippet.metrics import count_tokens, estimate_cost_per_token, estimate_carbon_per_token
from whippet.logger import save_benchmark_log

console = Console()

import platform
import subprocess

def detect_hardware():
    try:
        cpu = subprocess.check_output(["sysctl", "-n", "machdep.cpu.brand_string"]).decode().strip()
    except:
        cpu = platform.processor()

    try:
        # Get macOS version name (e.g., macOS 14.4)
        os_version = subprocess.check_output(["sw_vers", "-productVersion"]).decode().strip()
        os_name = f"macOS {os_version}"
    except:
        os_name = platform.system()

    return {
        "cpu": cpu,
        "cores": os.cpu_count(),
        "ram_gb": round(psutil.virtual_memory().total / 1e9, 2),
        "os": os_name
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

from whippet.printer import (
    print_whippet_intro,
    print_system_info,
    print_benchmark_results,
    print_token_analysis,
    print_resource_estimates,
    print_run_header
)


def profile_model(model_path, prompt, simulate_cores=None, llama_bin_path=None, enable_logging=False):

    print_whippet_intro()

    specs = detect_hardware()
    print_system_info(specs)

    print_run_header(model_path, prompt)

    bench = run_inference(model_path, prompt, simulate_cores, llama_bin_path)
    print_benchmark_results(bench)

    output = bench['output']
    prompt_tokens = count_tokens(prompt)
    output_tokens = count_tokens(output)
    efficiency = bench['tokens/sec'] / specs['cores']
    print_token_analysis(prompt_tokens, output_tokens, efficiency)

    watts = 20  # Estimated for this CPU
    cost = estimate_cost_per_token(watts, bench['duration'], 0.14, output_tokens)
    carbon = estimate_carbon_per_token(watts, bench['duration'], 417, output_tokens)
    print_resource_estimates(cost, carbon)

    log_path = save_benchmark_log(
        model_name=os.path.basename(model_path),
        prompt=prompt,
        specs=specs,
        bench=bench,
        prompt_tokens=prompt_tokens,
        output_tokens=output_tokens,
        cost=cost,
        carbon=carbon,
        enable_logging=enable_logging
    )

    if log_path:
        console.print(f"[dim]📁 Log saved to: {log_path}")

    return bench

