skills:
  - name: "classify_complaint"
    description: "Categorizes a single complaint into a predefined taxonomy, assigns priority based on severity keywords, and provides a reason citing the source text."
    input: "Dictionary with 'description' field containing citizen-provided text."
    output: "Dictionary containing 'category' (one of 10 taxonomy types), 'priority' (one of 3 severity levels), 'reason' (one-sentence justification), and 'flag' (NEEDS_REVIEW or blank)."
    error_handling: "If input is ambiguous, returns category: 'Other' and flag: 'NEEDS_REVIEW'."

  - name: "batch_classify"
    description: "Automates the classification of multiple complaints by reading an input CSV, applying classify_complaint to each row, and writing the results to a specified output CSV."
    input: "Input CSV file path containing 'description' column."
    output: "Output CSV file containing columns: 'category', 'priority', 'reason', and 'flag'."
    error_handling: "Validates input file existence and CSV format before processing; logs rows that fail to process."
