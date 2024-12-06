from benchmark import benchmark_insertion, benchmark_query, benchmark_delete, benchmark_range_query  # Added range query benchmark
from database import setup_database  # Import function to set up the SQLite database
from bplustree import BPlusTree  # Import the B+ Tree implementation
from syntheticdata import generate_data  # Import function to generate synthetic data
from benchmark import plot_results  # Import function to plot query performance results
import numpy as np  # Import for calculating summary statistics
from datetime import timedelta  # Import for range query time intervals

def summarize_metrics(metrics):
    """
    Summarize the performance metrics: mean, standard deviation, min, and max.
    """
    return {
        "mean": np.mean(metrics),
        "std": np.std(metrics),
        "min": np.min(metrics),
        "max": np.max(metrics)
    }

def print_summary(summary, label):
    """
    Print a summary of performance metrics.
    """
    print(f"\n{label} Summary:")
    print(f"Mean: {summary['mean']:.6f} seconds")
    print(f"Standard Deviation: {summary['std']:.6f} seconds")
    print(f"Min: {summary['min']:.6f} seconds")
    print(f"Max: {summary['max']:.6f} seconds")

def main():
    # Parameters
    num_trials = 10
    num_records = 100000
    num_queries = 100

    # Initialize storage for performance metrics
    insertion_times = []
    query_tree_times = []
    query_sql_times = []
    deletion_tree_times = []
    deletion_sql_times = []
    range_tree_times = []
    range_sql_times = []

    for trial in range(num_trials):
        print(f"\nRunning Trial {trial + 1}/{num_trials}...")

        # Initialize the SQLite database connection and cursor
        conn, cursor = setup_database()

        # Create an instance of the B+ Tree for in-memory operations
        tree = BPlusTree()

        # Generate a dataset
        dataset = generate_data(num_records)

        # Benchmark insertion
        print("Benchmarking Insertion...")
        insertion_time = benchmark_insertion(tree, cursor, dataset)
        insertion_times.append(insertion_time)

        # Prepare query timestamps
        queries = [record[0] for record in dataset[:num_queries]]

        # Benchmark queries
        print("Benchmarking Queries...")
        tree_times, sql_times = benchmark_query(tree, cursor, queries)
        query_tree_times.append(sum(tree_times) / len(tree_times))
        query_sql_times.append(sum(sql_times) / len(sql_times))

        # Generate range queries
        ranges = [(record[0], record[0] + timedelta(seconds=10)) for record in dataset[:num_queries]]

        # Benchmark range queries
        print("Benchmarking Range Queries...")
        tree_range_times, sql_range_times = benchmark_range_query(tree, cursor, ranges)
        range_tree_times.append(sum(tree_range_times) / len(tree_range_times))
        range_sql_times.append(sum(sql_range_times) / len(sql_range_times))

        # Benchmark deletion
        print("Benchmarking Deletion...")
        deletion_tree_time, deletion_sql_time = benchmark_delete(tree, cursor, dataset)
        deletion_tree_times.append(sum(deletion_tree_time) / len(deletion_tree_time))
        deletion_sql_times.append(sum(deletion_sql_time) / len(deletion_sql_time))

        # Close the database connection
        conn.close()

    # Summarize performance metrics
    insertion_summary = summarize_metrics(insertion_times)
    query_tree_summary = summarize_metrics(query_tree_times)
    query_sql_summary = summarize_metrics(query_sql_times)
    range_tree_summary = summarize_metrics(range_tree_times)
    range_sql_summary = summarize_metrics(range_sql_times)
    deletion_tree_summary = summarize_metrics(deletion_tree_times)
    deletion_sql_summary = summarize_metrics(deletion_sql_times)

    # Print summaries
    print_summary(insertion_summary, "Insertion")
    print_summary(query_tree_summary, "Query (B+ Tree)")
    print_summary(query_sql_summary, "Query (SQL Database)")
    print_summary(range_tree_summary, "Range Query (B+ Tree)")
    print_summary(range_sql_summary, "Range Query (SQL Database)")
    print_summary(deletion_tree_summary, "Deletion (B+ Tree)")
    print_summary(deletion_sql_summary, "Deletion (SQL Database)")

if __name__ == "__main__":
    main()
