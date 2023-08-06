import mysql.connector
import psycopg2
import time
import numpy as np
import matplotlib.pyplot as plt

# Define database connection parameters
mysql_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'MySQL1965',
    'database': 'employees'
}

postgres_config = {
    'host': 'localhost',
    'user': 'postgres',
    'password': 'Postgre1965',
    'database': 'employees'
}

# Queries to be executed
queries = [
    "SELECT emp_no, COUNT(*) AS count FROM employees GROUP BY emp_no;",
    "SELECT * FROM salaries WHERE salary = 94443 OR salary = 59571;",
    "SELECT E.*, S.* FROM employees E JOIN salaries S ON E.emp_no = S.emp_no WHERE E.first_name = 'Duangkaew';",
    "SELECT * FROM titles WHERE title LIKE 'senior%';",
    "SELECT E.*, T.* FROM employees E JOIN titles T ON E.emp_no = T.emp_no WHERE E.first_name = 'Duangkaew';",
]

# Function to run queries and collect results
def run_queries(conn, queries, num_times):
    results = []
    for query in queries:
        execution_times = []
        for _ in range(num_times):
            cursor = conn.cursor()
            start_time = time.time()
            cursor.execute(query)
            # Fetch and process the results, e.g., by using cursor.fetchall()
            # If you don't need the results, just iterate over the cursor to consume them
            for _ in cursor:
                pass
            end_time = time.time()
            execution_time = end_time - start_time
            execution_times.append(execution_time)
            cursor.close()
        results.append(execution_times)
    return results

def main():
    num_times = 1000

    try:
        # Connect to MySQL and PostgreSQL databases
        mysql_conn = mysql.connector.connect(**mysql_config)
        postgres_conn = psycopg2.connect(**postgres_config)

        # Run queries and collect results for MySQL
        mysql_query_results = run_queries(mysql_conn, queries, num_times)

        # Run queries and collect results for PostgreSQL
        postgres_query_results = run_queries(postgres_conn, queries, num_times)

        # Close connections
        mysql_conn.close()
        postgres_conn.close()

        # Build histograms for each query's execution time in MySQL and PostgreSQL
        for i, query in enumerate(queries):
            plt.figure(i + 1)
            plt.hist(mysql_query_results[i], bins=20, alpha=0.5, label="MySQL")
            plt.hist(postgres_query_results[i], bins=20, alpha=0.5, label="PostgreSQL")
            plt.legend(loc='upper right')
            plt.xlabel('Execution Time (seconds)')
            plt.ylabel('Frequency')
            
            # Calculate mean and variance
            mysql_mean = np.mean(mysql_query_results[i])
            postgres_mean = np.mean(postgres_query_results[i])
            mysql_variance = np.var(mysql_query_results[i])
            postgres_variance = np.var(postgres_query_results[i])
            
            # Display mean and variance in the histogram title
            plt.title(f'Histogram for Query {i+1}\n'
                      f'MySQL: Mean={mysql_mean:.6f}, Variance={mysql_variance:.6f}\n'
                      f'PostgreSQL: Mean={postgres_mean:.6f}, Variance={postgres_variance:.6f}')
            plt.savefig(f'histogram_query_{i+1}.png')
            plt.close()

            # Print mean and variance to the console
            print(f'Query {i+1} - MySQL: Mean={mysql_mean:.6f}, Variance={mysql_variance:.6f}')
            print(f'Query {i+1} - PostgreSQL: Mean={postgres_mean:.6f}, Variance={postgres_variance:.6f}')
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
