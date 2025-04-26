import struct
import os

def read_gguf_metadata(path):
    info = {}

    with open(path, 'rb') as f:
        magic = f.read(4)
        if magic != b'GGUF':
            raise ValueError("Not a valid GGUF file")

        version = struct.unpack('<I', f.read(4))[0]
        kv_data_offset = struct.unpack('<Q', f.read(8))[0]
        kv_count = struct.unpack('<Q', f.read(8))[0]

        info["gguf.version"] = version
        info["gguf.kv_count"] = kv_count

        for _ in range(kv_count):
            key_len = struct.unpack('<H', f.read(2))[0]
            key = f.read(key_len).decode('utf-8', errors='replace')

            value_type = struct.unpack('<B', f.read(1))[0]

            if value_type == 0:  # bool
                value = struct.unpack('<?', f.read(1))[0]
            elif value_type == 1:  # int
                value = struct.unpack('<q', f.read(8))[0]
            elif value_type == 2:  # float
                value = struct.unpack('<d', f.read(8))[0]
            elif value_type == 3:  # string
                str_len = struct.unpack('<I', f.read(4))[0]
                value = f.read(str_len).decode('utf-8', errors='replace')
            elif value_type == 4:  # array → skip for now
                arr_type = struct.unpack('<B', f.read(1))[0]
                arr_len = struct.unpack('<I', f.read(4))[0]
                # Skip based on type (approx): int/float = 8 bytes, string = variable
                if arr_type == 0:  # bool
                    f.read(arr_len)
                elif arr_type == 1:  # int
                    f.read(arr_len * 8)
                elif arr_type == 2:  # float
                    f.read(arr_len * 8)
                elif arr_type == 3:  # string
                    for _ in range(arr_len):
                        sl = struct.unpack('<I', f.read(4))[0]
                        f.read(sl)
                continue
            else:
                # Unknown type → skip 8 bytes
                f.read(8)
                continue

            info[key] = value

    return info

# def print_model_info(path, full=False):
#     try:
#         metadata = read_gguf_metadata(path)
#         print("\n📦 Model Metadata:")

#         if full:
#             for key in sorted(metadata):
#                 print(f"  {key}: {metadata[key]}")
#         else:
#             keys_to_show = [
#                 "general.name",
#                 "general.architecture",
#                 "quantization.type",
#                 "tokenizer.ggml.model",
#                 "tokenizer.ggml.vocab_size",
#                 "context_length",
#                 "gguf.version"
#             ]
#             for key in keys_to_show:
#                 value = metadata.get(key, "[not found]")
#                 print(f"  {key}: {value}")

#     except Exception as e:
#         print(f"❌ Failed to read model metadata: {e}")
def print_model_info(path, full=False):
    try:
        metadata = read_gguf_metadata(path)
        print("\n📦 Model Metadata:")

        for key in sorted(metadata):
            print(f"  {key}: {metadata[key]}")

    except Exception as e:
        print(f"❌ Failed to read model metadata: {e}")
