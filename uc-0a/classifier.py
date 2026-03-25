"""
UC-0A — Complaint Classifier
Starter file. Build this using the RICE → agents.md → skills.md → CRAFT workflow.
"""
import argparse
import csv

def classify_complaint(row: dict) -> dict:
    """
    Classify a single complaint row using keyword-based heuristics.
    Adheres to rules in agents.md: strict taxonomy, priority keywords, and reason citation.
    """
    description = row.get("description", "").lower()
    complaint_id = row.get("complaint_id", "Unknown")
    
    # Priority Keywords
    severity_keywords = ["injury", "child", "school", "hospital", "ambulance", "fire", "hazard", "fell", "collapse"]
    priority = "Standard"
    if any(keyword in description for keyword in severity_keywords):
        priority = "Urgent"

    # Category Mapping (Heuristics)
    category_map = {
        "Pothole": ["pothole", "pit", "crater"],
        "Flooding": ["flood", "water logging", "submerged", "inundation", "water", "draining"],
        "Streetlight": [" streetlight", "street light", "lamp", "dark", "flickering", "lighting", "unlit"],
        "Waste": ["garbage", "trash", "litter", "dump", "waste", "debris", "bin", "animal", "health"],
        "Noise": ["noise", "loud", "sound", "music", "loudspeaker", "band", "wedding", "amplifiers"],
        "Road Damage": ["road crack", "broken road", "pavement", "asphalt", "cracked", "sinking", "footpath", "tiles", "buckled", "subsided", "paving"],
        "Heritage Damage": ["heritage", "monument", "historical", "statue", "historic", "stone"],
        "Heat Hazard": ["heat", "sunstroke", "hot", "shade", "dehydration", "melting", "tarmac", "temperature", "bubbling", "sun"],
        "Drain Blockage": ["drain", "sewage", "gutter", "blockage", "overflow", "manhole"]
    }

    found_category = "Other"
    matching_keywords = []
    
    for cat, keywords in category_map.items():
        matches = [k for k in keywords if k in description]
        if matches:
            found_category = cat
            matching_keywords.extend(matches)
            break # Take the first match for simplicity in this heuristic

    flag = ""
    if found_category == "Other":
        flag = "NEEDS_REVIEW"
        reason = "The description does not clearly match any specific category keywords."
    else:
        # Cited words for reason
        cited_words = ", ".join(matching_keywords)
        reason = f"Classified as {found_category} due to mentions of '{cited_words}' in the description."

    return {
        "complaint_id": complaint_id,
        "category": found_category,
        "priority": priority,
        "reason": reason,
        "flag": flag
    }


def batch_classify(input_path: str, output_path: str):
    """
    Read input CSV, classify each row, and write the results to a CSV.
    Ensures zero taxonomy drift and handles potentially malformed rows.
    """
    results = []
    try:
        with open(input_path, mode="r", encoding="utf-8") as infile:
            reader = csv.DictReader(infile)
            for row in reader:
                try:
                    classified = classify_complaint(row)
                    results.append(classified)
                except Exception as e:
                    print(f"Error processing row: {row}. Error: {e}")
                    # Create a default 'Other' row if classification fails
                    results.append({
                        "complaint_id": row.get("complaint_id", "Error"),
                        "category": "Other",
                        "priority": "Low",
                        "reason": f"System error during classification: {str(e)}",
                        "flag": "NEEDS_REVIEW"
                    })
    except FileNotFoundError:
        print(f"Error: Input file not found at {input_path}")
        return

    if not results:
        print("No results to write.")
        return

    fieldnames = ["complaint_id", "category", "priority", "reason", "flag"]
    with open(output_path, mode="w", encoding="utf-8", newline="") as outfile:
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="UC-0A Complaint Classifier")
    parser.add_argument("--input",  required=True, help="Path to test_[city].csv")
    parser.add_argument("--output", required=True, help="Path to write results CSV")
    args = parser.parse_args()
    batch_classify(args.input, args.output)
    print(f"Done. Results written to {args.output}")
