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
    profile_cmd.add_argument("--log", action="store_true", default=False, help="Save benchmark log to disk")

    compare_cmd = subparsers.add_parser("compare", help="Compare multiple quantized models")
    compare_cmd.add_argument("--model-dir", required=True, help="Directory containing .gguf models")
    compare_cmd.add_argument("--prompt", default="Explain gravity.", help="Prompt to use for benchmarking")
    compare_cmd.add_argument("--simulate-cores", type=int, help="Simulate a low-core environment")
    compare_cmd.add_argument("--llama-bin", help="Path to custom llama.cpp binary")


    model_info_cmd = subparsers.add_parser("model-info", help="Print model metadata from a .gguf file")
    model_info_cmd.add_argument("--model", required=True, help="Path to the .gguf model")
    model_info_cmd.add_argument("--full", action="store_true", help="Print all raw metadata fields")


    args = parser.parse_args()

    if args.command == "profile":
        from whippet.profiler import profile_model
        profile_model(
            model_path=args.model,
            prompt=args.prompt,
            simulate_cores=args.simulate_cores,
            llama_bin_path=args.llama_bin,
            enable_logging=args.log
        )

    elif args.command == "compare":
        from whippet.compare import compare_models
        compare_models(
            model_dir=args.model_dir,
            prompt=args.prompt,
            simulate_cores=args.simulate_cores,
            llama_bin_path=args.llama_bin
        )


    elif args.command == "model-info":
        from whippet.model_info import print_model_info
        print_model_info(args.model, full=args.full)



if __name__ == "__main__":
    main()
