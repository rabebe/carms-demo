import os
import re

# Path to data folder
BASE_DATA_DIR = os.path.join("data", "program_descriptions")

def extract_metadata_from_md(file_path):
    """Parses a single .md file for key CaRMS data points."""
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Extracting using the format from sample
    # Title line: # University - Specialty - Site
    title_pattern = r"#\s*(?P<uni>.*?) - (?P<spec>.*?) - (?P<site>.*)"
    match = re.search(title_pattern, content)
    
    metadata = {
        "university": match.group("uni").strip() if match else "Unknown",
        "specialty": match.group("spec").strip() if match else "Unknown",
        "site": match.group("site").strip() if match else "Unknown",
        "quota": 0,
        "file_path": file_path
    }

    # Extract Quota: ## Approximate Quota: 3
    quota_match = re.search(r"Approximate Quota:\s*(\d+)", content)
    if quota_match:
        metadata["quota"] = int(quota_match.group(1))

    return metadata

def get_all_program_metadata():
    all_programs = []
    if not os.path.exists(BASE_DATA_DIR):
        print(f"Error: {BASE_DATA_DIR} not found!")
        return []

    for filename in os.listdir(BASE_DATA_DIR):
        if filename.endswith(".md"):
            full_path = os.path.join(BASE_DATA_DIR, filename)
            all_programs.append(extract_metadata_from_md(full_path))
    
    return all_programs

if __name__ == "__main__":
    # Test print to see if it works
    programs = get_all_program_metadata()
    for p in programs[:2]: # Just show first two
        print(f"Found: {p['university']} in {p['site']} (Quota: {p['quota']})")