import os
import sys
import subprocess
import urllib.request

# Base URL for the model files hosted on GitHub Releases of the repository
BASE_RELEASE_URL = "https://github.com/vzn3114/Face-Detection/releases/download/v1.0.0/"

# Dict of weights: filename -> url
MODEL_WEIGHTS = {
    "mobilenet0.25_Final.onnx": BASE_RELEASE_URL + "mobilenet0.25_Final.onnx",
    "Resnet50_Final.onnx": BASE_RELEASE_URL + "Resnet50_Final.onnx",
    "unet_face_celeb.onnx": BASE_RELEASE_URL + "unet_face_celeb.onnx"
}

def check_and_download_weights():
    weights_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), 'backend', 'weights'))
    os.makedirs(weights_dir, exist_ok=True)
    
    missing_files = []
    for filename in MODEL_WEIGHTS:
        filepath = os.path.join(weights_dir, filename)
        if not os.path.exists(filepath) or os.path.getsize(filepath) == 0:
            missing_files.append(filename)
            
    if not missing_files:
        return
        
    print("=" * 70)
    print(" MISSING MODEL WEIGHTS DETECTED (ONNX WEIGHTS)")
    print(" System will automatically download required models from GitHub Releases.")
    print("=" * 70)
    
    for filename in missing_files:
        url = MODEL_WEIGHTS[filename]
        dest_path = os.path.join(weights_dir, filename)
        temp_dest_path = dest_path + ".tmp"
        
        print(f"\n[*] Downloading: {filename}...")
        
        try:
            def progress_hook(count, block_size, total_size):
                if total_size <= 0:
                    return
                percent = int(count * block_size * 100 / total_size)
                percent = min(100, percent)
                downloaded = (count * block_size) / (1024 * 1024)
                total_mb = total_size / (1024 * 1024)
                
                # Render neat CLI progress bar
                bar_length = 40
                filled_length = int(bar_length * percent // 100)
                bar = '=' * filled_length + '-' * (bar_length - filled_length)
                sys.stdout.write(f"\r    Progress: [{bar}] {percent}% ({downloaded:.1f} MB / {total_mb:.1f} MB)")
                sys.stdout.flush()
                
            urllib.request.urlretrieve(url, temp_dest_path, reporthook=progress_hook)
            sys.stdout.write("\n")
            
            # Rename temp file to actual file upon completion
            if os.path.exists(temp_dest_path):
                os.replace(temp_dest_path, dest_path)
                print(f"[+] Downloaded: {filename}")
        except Exception as e:
            if os.path.exists(temp_dest_path):
                try:
                    os.remove(temp_dest_path)
                except:
                    pass
            print(f"\n[-] Error downloading model {filename}: {e}")
            print("Please check your internet connection or download them manually.")
            sys.exit(1)
            
    print("\n" + "=" * 70)
    print(" [+] All models have been downloaded and prepared successfully!")
    print("=" * 70 + "\n")

if __name__ == "__main__":
    # Check and download weights if missing
    check_and_download_weights()

    backend_main = os.path.abspath(os.path.join(os.path.dirname(__file__), 'backend', 'main.py'))
    print(f"Starting AI Crowd Face Surveillance Console from {backend_main}...")
    try:
        subprocess.run([
            sys.executable,
            "-m",
            "backend.main"
        ], check=True)
    except KeyboardInterrupt:
        print("\nServer stopped by user.")
    except Exception as e:
        print(f"Error starting server: {e}")
