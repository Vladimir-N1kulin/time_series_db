import time
import sys
import os
# Add the '../src' directory to the Python path to access the database module
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from database import insert_record, search_exact_time  # Import required functions from the database module
import matplotlib.pyplot as plt  # Import for plotting results

# Function to plot the query performance results
def plot_results(tree_times, sql_times):
    # Set dark background theme
    plt.style.use('dark_background')
    
    # Plot the times for the B+ Tree and SQL queries with custom colors
    plt.plot(tree_times, label="B+ Tree", color='cyan', linewidth=2)
    plt.plot(sql_times, label="SQL", color='magenta', linewidth=2)
    
    # Add a legend to differentiate the two lines
    plt.legend(loc='best', facecolor='black', edgecolor='white')
    
    # Label the axes and add a title
    plt.xlabel("Query Index", color='white')
    plt.ylabel("Time (s)", color='white')
    plt.title("Query Performance", color='white')
    
    # Customize gridlines
    plt.grid(color='gray', linestyle='--', linewidth=0.5)
    
    # Customize tick colors
    plt.xticks(color='white')
    plt.yticks(color='white')
    
    # Display the plot
    plt.show()

# Function to benchmark insertion performance for both a B+ Tree and SQL database
def benchmark_insertion(tree, cursor, dataset):
    start_time = time.time()  # Record the start time
    # Loop through the dataset, inserting each record into both the B+ Tree and the SQL database
    for timestamp, value in dataset:
        tree.insert(timestamp, value)  # Insert into the B+ Tree
        insert_record(cursor, timestamp, value)  # Insert into the SQL database
    return time.time() - start_time  # Return the total time taken for insertion

# Function to benchmark query performance for both a B+ Tree and SQL database
def benchmark_query(tree, cursor, queries):
    tree_times = []  # List to store query times for the B+ Tree
    sql_times = []  # List to store query times for the SQL database

    for query in queries:
        # Benchmark B+ Tree query
        start_time = time.time()  # Record the start time
        tree.query(query)  # Perform the query on the B+ Tree
        tree_times.append(time.time() - start_time)  # Record the time taken

        # Benchmark SQL query
        start_time = time.time()  # Record the start time
        search_exact_time(cursor, query)  # Perform the query on the SQL database
        sql_times.append(time.time() - start_time)  # Record the time taken

    return tree_times, sql_times  # Return the times for both the B+ Tree and SQL queries
