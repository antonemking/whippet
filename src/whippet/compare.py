import os
from whippet.profiler import run_inference, detect_hardware
from whippet.metrics import estimate_cost_per_token, estimate_carbon_per_token
from rich.console import Console
from rich.table import Table

console = Console()

def compare_models(model_dir, prompt, simulate_cores=None, llama_bin_path=None):
    models = [f for f in os.listdir(model_dir) if f.endswith(".gguf")]

    if not models:
        console.print("[red]❌ No .gguf quantized models found in the directory.")
        return

    specs = detect_hardware()
    watts = 20  # Estimated for a typical MacBook / Edge CPU
    price_per_kwh = 0.14  # Average US electricity cost
    carbon_intensity = 417  # g CO₂ per kWh

    results = []

    for model in models:
        path = os.path.join(model_dir, model)
        size_mb = round(os.path.getsize(path) / 1e6, 1)

        console.print(f"\n[bold]🧪 Profiling {model}...")
        bench = run_inference(path, prompt, simulate_cores, llama_bin_path)

        output_tokens = len(bench["output"].split())
        cost_per_token = estimate_cost_per_token(watts, bench["duration"], price_per_kwh, output_tokens)
        carbon_per_token = estimate_carbon_per_token(watts, bench["duration"], carbon_intensity, output_tokens)

        results.append({
            "model": model,
            "size_mb": size_mb,
            "tokens_per_sec": bench["tokens/sec"],
            "duration": bench["duration"],
            "output_tokens": output_tokens,
            "cost_per_token": cost_per_token,
            "carbon_per_token": carbon_per_token
        })

    # Sort models by highest tokens/sec first
    results = sorted(results, key=lambda x: -x["tokens_per_sec"])

    table = Table(title="Whippet Quantization Comparison 📊")
    table.add_column("Model", justify="left")
    table.add_column("Size (MB)", justify="right")
    table.add_column("Speed (t/s)", justify="right")
    table.add_column("Duration (s)", justify="right")
    table.add_column("Tokens", justify="right")
    table.add_column("Cost/Token ($)", justify="right")
    table.add_column("CO₂/Token (g)", justify="right")

    for r in results:
        table.add_row(
            r["model"],
            str(r["size_mb"]),
            f"{r['tokens_per_sec']:.2f}",
            f"{r['duration']:.2f}",
            str(r["output_tokens"]),
            f"{r['cost_per_token']:.8f}",
            f"{r['carbon_per_token']:.5f}"
        )

    console.print("\n[bold green]📊 Comparison Results\n")
    console.print(table)
