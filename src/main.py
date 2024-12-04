from benchmark import benchmark_insertion, benchmark_query  # Import functions to benchmark insertion and query performance
from database import setup_database  # Import function to set up the SQLite database
from bplustree import BPlusTree  # Import the B+ Tree implementation
from syntheticdata import generate_data  # Import function to generate synthetic data
from benchmark import plot_results  # Import function to plot query performance results

# Initialize the SQLite database connection and cursor
conn, cursor = setup_database()

# Create an instance of the B+ Tree for in-memory operations
tree = BPlusTree()

# Generate a dataset of 1,000,000 records with unique timestamps and corresponding values
dataset = generate_data(1000000)

# Benchmark the time required to insert the dataset into both the B+ Tree and the SQLite database
insertion_time = benchmark_insertion(tree, cursor, dataset)
print(f"Insertion Time: {insertion_time}")  # Print the total time taken for insertion

# Prepare a list of 100 query timestamps by extracting the timestamps from the first 100 records of the dataset
queries = [record[0] for record in dataset[:100]]

# Benchmark the query performance for both the B+ Tree and the SQLite database
tree_times, sql_times = benchmark_query(tree, cursor, queries)

# Plot the query performance comparison between the B+ Tree and SQL database
plot_results(tree_times, sql_times)

# Calculate and print the average query time for the B+ Tree
print(f"Average query time for the B+ Tree: {sum(tree_times) / len(tree_times)}")

# Calculate and print the average query time for the SQL database
print(f"Average query time for the SQL database: {sum(sql_times) / len(sql_times)}")
