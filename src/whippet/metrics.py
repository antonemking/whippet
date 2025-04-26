def count_tokens(text: str) -> int:
    return len(text.split())

def estimate_cost_per_token(watts: float, duration: float, price_per_kwh: float, output_tokens: int) -> float:
    kwh_used = (watts * duration) / (3600 * 1000)
    cost = kwh_used * price_per_kwh
    return cost / output_tokens if output_tokens > 0 else 0.0

def estimate_carbon_per_token(watts: float, duration: float, carbon_intensity: float, output_tokens: int) -> float:
    kwh_used = (watts * duration) / (3600 * 1000)
    carbon = kwh_used * carbon_intensity
    return carbon / output_tokens if output_tokens > 0 else 0.0
