import pandas as pd


def enrich_transactional_data(employee_data_path, transaction_data_path, output_path):
    """
    Enriches transactional data with employee details using employee code,
    handling missing employee codes efficiently for large datasets.

    Args:
        employee_data_path (str): Path to the CSV file containing employee data.
        transaction_data_path (str): Path to the CSV file containing transaction data.
        output_path (str): Path to save the enriched transactional data.
    """

    # Read employee data into a dictionary for efficient lookups (hash table)
    employee_dict = pd.read_csv(employee_data_path).set_index("Employee Code")
    employee_dict = employee_dict.to_dict(orient="index")

    # Load transactional data in chunks for memory efficiency
    def process_chunk(chunk):
        # Merge with employee data using left outer join to preserve all transactions
        merged_chunk = chunk.merge(employee_dict, how="left", on="Employee Code")

        # Flag missing employee codes and potentially perform additional custom logic
        merged_chunk["Employee Details Missing"] = merged_chunk["Employee Code"].isnull()

        # Optionally, fill missing values with appropriate defaults or strategies
        # merged_chunk.fillna(..., inplace=True)

        return merged_chunk

    with pd.read_csv(transaction_data_path, chunksize=10000) as reader:  # Adjust chunksize as needed
        result = reader.pipe(process_chunk)
        result.to_csv(output_path, index=False)


# Example usage
employee_data_path = "path/to/employee_data.csv"
transaction_data_path = "path/to/transaction_data.csv"
output_path = "path/to/enriched_transaction_data.csv"

enrich_transactional_data(employee_data_path, transaction_data_path, output_path)
