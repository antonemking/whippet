import os
from whippet.profiler import run_inference, detect_hardware
from rich.console import Console
from rich.table import Table

console = Console()

def compare_models(model_dir, prompt, simulate_cores):
    models = [f for f in os.listdir(model_dir) if f.endswith(".bin")]

    if not models:
        console.print("[red]No .bin quantized models found in the directory.")
        return

    specs = detect_hardware()
    table = Table(title="Whippet Quantization Comparison")
    table.add_column("Model", justify="left")
    table.add_column("Size (MB)", justify="right")
    table.add_column("Speed (t/s)", justify="right")
    table.add_column("Duration (s)", justify="right")
    table.add_column("Tokens", justify="right")

    for model in models:
        path = os.path.join(model_dir, model)
        size_mb = round(os.path.getsize(path) / 1e6, 1)

        console.print(f"\n[bold]🧪 Profiling {model}...")
        bench = run_inference(path, prompt, simulate_cores)

        table.add_row(
            model,
            str(size_mb),
            str(bench["tokens/sec"]),
            str(bench["duration"]),
            str(len(bench["output"].split()))
        )

    console.print("\n[bold green]📊 Comparison Results:\n")
    console.print(table)
