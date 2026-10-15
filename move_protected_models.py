from pathlib import Path
import shutil


def move_model_files():
    # Define source and destination base directories
    source_base = Path("outputs/default_app")
    dest_dir = Path("gr00t_trt_deployment/onnx/protected")

    # Create the destination directory (and any parent directories) if it doesn't exist
    dest_dir.mkdir(parents=True, exist_ok=True)

    # Check if the source directory exists
    if not source_base.exists():
        print(f"Error: Source directory '{source_base}' does not exist.")
        return

    # Move export_metadata.json if it exists in the base source directory
    metadata_file = source_base / "export_metadata.json"
    if metadata_file.exists():
        shutil.move(str(metadata_file), str(dest_dir / metadata_file.name))
        print(f"Moved {metadata_file.name}")
    else:
        print(f"Warning: {metadata_file.name} not found in '{source_base}'!")

    # Iterate through all subdirectories (each representing a model_name)
    for model_dir in source_base.iterdir():
        if model_dir.is_dir():
            model_name = model_dir.name
            print(f"Processing model: {model_name}")

            # 1. Move the .onnx file
            onnx_file = model_dir / f"{model_name}.onnx"
            if onnx_file.exists():
                # Providing the full destination path allows overwriting if the file already exists
                shutil.move(str(onnx_file), str(dest_dir / onnx_file.name))
                print(f"  -> Moved {onnx_file.name}")
            else:
                print(f"  -> Warning: {onnx_file.name} not found!")

            # 2. Move any .data files associated with the model
            data_files = list(model_dir.glob("*.data"))
            if data_files:
                for data_file in data_files:
                    shutil.move(str(data_file), str(dest_dir / data_file.name))
                    print(f"  -> Moved {data_file.name}")
            else:
                print(f"  -> Note: No .data file found for {model_name}")


if __name__ == "__main__":
    move_model_files()
    print("\nMove operation completed!")
