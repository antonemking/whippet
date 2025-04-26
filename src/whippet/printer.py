from rich.console import Console
from rich.panel import Panel
from rich import box
import time
import os

console = Console()

WHIPPET_ASCII = r"""
            __
           /  \
          / ..|\
         (_\  |_)
         /  \@' 
        /     \
    _  /  `   |
   \\_/  \____/
     \____|
"""

def print_whippet_intro():
    console.clear()
    console.print(Panel.fit(WHIPPET_ASCII, title="[bold cyan]Whippet AI Profiler 🐶", border_style="cyan", box=box.DOUBLE))
    console.print("[italic]Quantized Language Model Profiler for the Edge\n", style="dim")
    time.sleep(0.5)

def print_system_info(specs):
    console.print("[bold green]🔍 Detecting Hardware...\n")
    console.print(f"🧠 CPU: {specs['cpu']}")
    console.print(f"💾 RAM: {specs['ram_gb']} GB")
    console.print(f"🖥️  Cores: {specs['cores']}")
    console.print(f"🧠 OS: {specs['os']}\n")

def print_run_header(model_path, prompt):
    model_name = os.path.basename(model_path)
    console.print("[bold blue]🚀 Running")
    console.print(f"📦 Model: {model_name}")
    console.print(f"📝 Prompt: {prompt}\n")

def print_benchmark_results(bench):
    console.print("[bold magenta]🧪 Benchmark Results")
    console.print(f"🚀 Tokens/sec: {bench['tokens/sec']}")
    console.print(f"⏱️ Duration: {bench['duration']}s")
    console.print(f"📤 Output: {bench['output'][:200]}...\n")

def print_token_analysis(prompt_tokens, output_tokens, efficiency):
    total_tokens = prompt_tokens + output_tokens
    console.print("[bold yellow]📊 Token Analysis")
    console.print(f"🧾 Prompt Tokens: {prompt_tokens}")
    console.print(f"📨 Output Tokens: {output_tokens}")
    console.print(f"🧮 Total Tokens: {total_tokens}")
    console.print(f"⚙️ Tokens/sec/core: {efficiency:.2f}\n")

def print_resource_estimates(cost_per_token, carbon_per_token):
    console.print("[bold blue]♻️ Resource Efficiency")
    console.print(f"💸 Est. Cost per Token: ${cost_per_token:.8f}")
    console.print(f"🌱 Est. CO₂ per Token: {carbon_per_token:.8f} g\n")
