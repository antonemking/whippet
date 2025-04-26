import json
import os
from datetime import datetime

def ensure_log_dir(path=".whippet_logs"):
    os.makedirs(path, exist_ok=True)
    return path

def save_benchmark_log(model_name: str, prompt: str, specs: dict, bench: dict, 
                        prompt_tokens: int, output_tokens: int,
                        cost: float, carbon: float, log_dir=".whippet_logs", enable_logging=True):

    if not enable_logging:
        return None

    log_path = ensure_log_dir(log_dir)

    filename = f"{model_name.replace('.gguf', '').replace('/', '_')}_{datetime.now().strftime('%Y%m%d-%H%M%S')}.json"
    full_path = os.path.join(log_path, filename)

    log_data = {
        "model": model_name,
        "prompt": prompt,
        "hardware": specs,
        "metrics": {
            "duration_sec": bench['duration'],
            "tokens_per_sec": bench['tokens/sec'],
            "prompt_tokens": prompt_tokens,
            "output_tokens": output_tokens,
            "total_tokens": prompt_tokens + output_tokens,
            "tokens_per_sec_per_core": round(bench['tokens/sec'] / specs['cores'], 2),
            "cost_per_token": cost,
            "carbon_per_token": carbon,
        },
        "output_preview": bench['output'][:300],
        "timestamp": datetime.now().isoformat()
    }

    with open(full_path, "w") as f:
        json.dump(log_data, f, indent=2)

    return full_path
