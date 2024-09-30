import subprocess
import sys

def run_script(script, args=None):
    """Run script and return its output."""
    cmd = [sys.executable, script]
    if args:
        cmd.extend(args)
    result = subprocess.run(cmd, text=True, capture_output=True)
    if result.returncode != 0:
        print(f"Error running {script}: {result.stderr}")
        sys.exit(1)
    return result.stdout.strip()

def main():
    num_files = 50  # Number of JSON files to generate and process

    for i in range(num_files):
        # Generate a JSON file with iteration index
        json_filename = run_script('generate_json.py', [str(i + 1)])
        print(f"Generated JSON file: {json_filename}")
        
        # uncomment the below line if you already have the JSON files
        # json_filename = f"gr_{i + 1}.json"
        
        # Process the JSON file with an additional argument
        run_script('reportlab_doc.py', [json_filename, str(i + 1)])
        print(f"Processed JSON file: {json_filename}")

if __name__ == "__main__":
    main()
