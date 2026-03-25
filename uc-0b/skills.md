skills:
  - name: retrieve_policy
    description: Parses a .txt policy document into structured sections indexed by clause numbers.
    input: Absolute path to the policy .txt file.
    output: A data structure mapping clause numbers (e.g., "5.2") to their text content.
    error_handling: Refuses if the file is unreadable, missing, or lacks the required numbered clause structure.

  - name: summarize_policy
    description: Generates a high-fidelity summary of policy sections, ensuring all 10 target clauses are preserved with full conditions.
    input: Structured policy sections where clause numbers are explicit.
    output: A summary document containing all 10 mandated clauses, dual-approval conditions, and verbatim flags where necessary.
    error_handling: Errors out if any of the 10 critical clauses (2.3, 2.4, 2.5, 2.6, 2.7, 3.2, 3.4, 5.2, 5.3, 7.2) are missing from the input.
