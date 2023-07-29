import mysql.connector
import numpy as np
import matplotlib.pyplot as plt

# MySQL connection configuration
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'MySQL1965',
    'database': 'employees',
}

# 5 queries to be executed
queries = [
    "SELECT emp_no, COUNT(*) AS count FROM employees GROUP BY emp_no;", 
    "SELECT * FROM salaries WHERE salary = 94443 OR salary = 59571;", 
    "SELECT E.*, S.* FROM EMPLOYEES E JOIN SALARIES S ON E.EMP_NO = S.EMP_NO WHERE E.FIRST_NAME = 'Duangkaew';",  
    "SELECT * FROM TITLES WHERE TITLE LIKE 'senior%';", 
    "SELECT E.*, T.* FROM EMPLOYEES E JOIN TITLES T ON E.EMP_NO = T.EMP_NO WHERE E.FIRST_NAME = 'Duangkaew';"   
]

# Function to run queries and collect results
def run_queries(conn, queries, num_times):
    results = [[] for _ in range(len(queries))]
    for _ in range(num_times):
        for i, query in enumerate(queries):
            cursor = conn.cursor()
            cursor.execute(query)
            result = cursor.fetchall()
            cursor.close()
            results[i].append(result)
    return results

def main():
    num_times = 0
    

    try:
        # Connect to the database
        conn = mysql.connector.connect(**db_config)

        # Run the queries and collect results
        query_results = run_queries(conn, queries, num_times)

        # Calculate mean and variance for each query
        means = [np.mean([len(result) for result in results]) for results in query_results]
        variances = [np.var([len(result) for result in results]) for results in query_results]

        # Build histograms
        for i, query in enumerate(queries):
            plt.hist([len(result) for result in query_results[i]], bins=20, alpha=0.5, label=f"Query {i+1}")

        plt.legend(loc='upper right')
        plt.xlabel('Number of Rows')
        plt.ylabel('Frequency')
        plt.title('Histogram of Query Results')
        plt.show()

        # Print mean and variance
        for i, query in enumerate(queries):
            print(f"Query {i+1} - Mean: {means[i]}, Variance: {variances[i]}")

    except mysql.connector.Error as err:
        print(f"Error: {err}")

    finally:
        # Close the database connection
        if conn.is_connected():
            conn.close()

if __name__ == "__main__":
    main()
