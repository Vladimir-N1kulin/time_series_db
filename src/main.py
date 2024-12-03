from benchmark import benchmark_insertion, benchmark_query
from database import setup_database
from bplustree import BPlusTree
from syntheticdata import generate_data
from benchmark import plot_results

from bplustree import BPlusTree


conn, cursor = setup_database()
tree = BPlusTree()

# Generate dataset
dataset = generate_data(1000000)

# Benchmark insertion
insertion_time = benchmark_insertion(tree, cursor, dataset)
print(f"Insertion Time: {insertion_time}")

# Benchmark queries
queries = [record[0] for record in dataset[:1000]]  # Select first 100 timestamps
tree_times, sql_times = benchmark_query(tree, cursor, queries)

plot_results(tree_times, sql_times)
print(f"Tree Times: {sum(tree_times) / len(tree_times)}")
print(f"SQL Times: {sum(sql_times) / len(sql_times)}")
