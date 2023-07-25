import os
import plotly.express as px
import pandas as pd
import plotly.graph_objs as go
from flask import Flask, render_template, request

app = Flask(__name__)

# Read the CSV file into a pandas DataFrame
df = pd.read_csv('BankChurners.csv')
    
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        selected_column = request.form['column']
        column_data = df[selected_column]

        # Create histogram
        hist_trace = go.Histogram(x=column_data, nbinsx=10, name='Distribution Plot')

        # Create box plot
        box_trace = go.Box(y=column_data, name='Box Plot')

        # Layout for both plots
        layout = go.Layout(title=f'Distribution Plot and Box Plot for Column {selected_column}',
                           xaxis=dict(title=selected_column),
                           yaxis=dict(title='Frequency/Value'))

        # Combine the plots
        fig = go.Figure(data=[hist_trace, box_trace], layout=layout)

        # Convert the plot to JSON and pass it to the template
        plot_json = fig.to_json()

        return render_template('index.html', plot_json=plot_json)

    return render_template('index.html', plot_json=None)

if __name__ == '__main__':
    app.run(debug=True)

