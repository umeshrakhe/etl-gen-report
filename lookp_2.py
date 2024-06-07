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

    def process_and_enrich_chunk(chunk):
        # Convert TextFileReader to DataFrame for processing
        df = chunk.to_frame()  # Assuming chunk is a TextFileReader object

        # Merge with employee data using left outer join to preserve all transactions
        merged_df = df.merge(employee_dict, how="left", on="Employee Code")

        # Flag missing employee codes and potentially perform additional custom logic
        merged_df["Employee Details Missing"] = merged_df["Employee Code"].isnull()

        # Optionally, fill missing values with appropriate defaults or strategies
        # merged_df.fillna(..., inplace=True)

        return merged_df

    # Read transactional data in chunks for memory efficiency
    with pd.read_csv(transaction_data_path, chunksize=10000) as reader:
        result = reader.apply(process_and_enrich_chunk)  # Apply function to each chunk
        result.to_csv(output_path, index=False)
        
def process_and_enrich_chunk(reader, chunksize):
    for chunk in pd.read_csv(reader, chunksize=chunksize):
        # Convert chunk to DataFrame and process
        df = chunk.to_frame()

        # ... (rest of the processing logic)

        # Yield the processed chunk
        yield df

# In enrich_transactional_data function:
with pd.read_csv(transaction_data_path, chunksize=1000) as reader:
    result = pd.concat(process_and_enrich_chunk(reader, 1000))  # Concatenate processed chunks
    result.to_csv(output_path, index=False)


# Example usage
employee_data_path = "path/to/employee_data.csv"
transaction_data_path = "path/to/transaction_data.csv"
output_path = "path/to/enriched_transaction_data.csv"

enrich_transactional_data(employee_data_path, transaction_data_path, output_piece)
