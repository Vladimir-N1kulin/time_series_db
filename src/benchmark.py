import time
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from database import insert_record, search_exact_time
import matplotlib.pyplot as plt

def plot_results(tree_times, sql_times):
    plt.plot(tree_times, label="B+ Tree")
    plt.plot(sql_times, label="SQL")
    plt.legend()
    plt.xlabel("Query Index")
    plt.ylabel("Time (s)")
    plt.title("Query Performance")
    plt.show()

def benchmark_insertion(tree, cursor, dataset):
    start_time = time.time()
    for timestamp, value in dataset:
        tree.insert(timestamp, value)
        insert_record(cursor, timestamp, value)
    return time.time() - start_time

def benchmark_query(tree, cursor, queries):
    tree_times = []
    sql_times = []

    for query in queries:
        # Benchmark B+ Tree
        start_time = time.time()
        tree.query(query)
        tree_times.append(time.time() - start_time)

        # Benchmark SQL
        start_time = time.time()
        search_exact_time(cursor, query)
        sql_times.append(time.time() - start_time)

    return tree_times, sql_times
