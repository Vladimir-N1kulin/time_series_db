from benchmark import benchmark_insertion, benchmark_query, benchmark_delete # Import functions for benchmarking
from database import setup_database  # Import function to set up the SQLite database
from bplustree import BPlusTree  # Import the B+ Tree implementation
from syntheticdata import generate_data  # Import function to generate synthetic data
from benchmark import plot_results  # Import function to plot query performance results

def main():
    # Initialize the SQLite database connection and cursor
    conn, cursor = setup_database()

    # Create an instance of the B+ Tree for in-memory operations
    tree = BPlusTree()

    # Generate a dataset of 100,000 records with unique timestamps and corresponding values
    print("Generating dataset...")
    dataset = generate_data(100000)  

    # 1. Benchmark the insertion process
    print("Benchmarking Insertion...")
    insertion_time = benchmark_insertion(tree, cursor, dataset)
    print(f"Insertion Time: {insertion_time:.4f} seconds")  # Print the total time taken for insertion

    # 2. Prepare a list of query timestamps by extracting the timestamps from the dataset
    queries = [record[0] for record in dataset[:100]]  # Select the first 1,000 timestamps for queries

    # Benchmark the query performance for both the B+ Tree and the SQLite database
    print("Benchmarking Queries...")
    tree_times, sql_times = benchmark_query(tree, cursor, queries)

    # Plot the query performance comparison
    plot_results(tree_times, sql_times)

    # Calculate and print average query times
    print(f"Average query time for the B+ Tree: {sum(tree_times) / len(tree_times):.6f} seconds")
    print(f"Average query time for the SQL database: {sum(sql_times) / len(sql_times):.6f} seconds")

    # Benchmark deletion performance
    print("Benchmarking Deletion...")
    deletion_tree_times, deletion_sql_times = benchmark_delete(tree, cursor, dataset)

    # Plot the deletion performance comparison
    plot_results(deletion_tree_times, deletion_sql_times)

    # Calculate and print average deletion times
    print(f"Average deletion time for the B+ Tree: {sum(deletion_tree_times) / len(deletion_tree_times):.6f} seconds")
    print(f"Average deletion time for the SQL database: {sum(deletion_sql_times) / len(deletion_sql_times):.6f} seconds")


    # Close the database connection after benchmarking
    conn.close()
    print("Benchmarking completed and database connection closed.")

if __name__ == "__main__":
    main()
