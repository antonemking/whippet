import argparse

def main():
    parser = argparse.ArgumentParser(description="Whippet CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # `whippet profile` command
    profile_cmd = subparsers.add_parser("profile", help="Profile model on current hardware")
    profile_cmd.add_argument("--model", required=True, help="Path to quantized model file")
    profile_cmd.add_argument("--prompt", default="Explain what a black hole is.", help="Prompt for inference")
    profile_cmd.add_argument("--simulate-cores", type=int, help="Simulate low-core device")
    profile_cmd.add_argument("--llama-bin", help="Path to llama.cpp binary if not in PATH or default location")

    compare_cmd = subparsers.add_parser("compare", help="Compare multiple quantized models")
    compare_cmd.add_argument("--model-dir", required=True, help="Directory with quantized models")
    compare_cmd.add_argument("--prompt", default="Explain gravity.", help="Prompt to test")
    compare_cmd.add_argument("--simulate-cores", type=int, help="Simulate lower-core environment")

    args = parser.parse_args()

    if args.command == "profile":
        from whippet.profiler import profile_model
        profile_model(
            model_path=args.model,
            prompt=args.prompt,
            simulate_cores=args.simulate_cores,
            llama_bin_path=args.llama_bin
        )

    elif args.command == "compare":
        from whippet.compare import compare_models
        compare_models(args.model_dir, args.prompt, args.simulate_cores)

if __name__ == "__main__":
    main()
