
def print_errors(content):
    lines = content.splitlines()
    for i, line in enumerate(lines):
        if "FAILED" in line or "ERROR" in line or "Error" in line:
            print(line)
            for j in range(1, 10):
                if i + j < len(lines):
                    print(lines[i + j])

try:
    with open("test_log_final.txt", "r", encoding="utf-16le") as f:
        print_errors(f.read())
except Exception as e:
    # print(f"Error reading utf-16: {e}")
    try:
        with open("test_log_final.txt", "r", encoding="utf-8") as f:
            print_errors(f.read())
    except Exception as e2:
        print(f"Error reading utf-8: {e2}")
