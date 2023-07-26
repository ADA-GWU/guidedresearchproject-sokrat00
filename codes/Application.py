import pandas as pd
import plotly.graph_objs as go
from flask import Flask, render_template, request

app = Flask(__name__)

# Read the CSV file into a pandas DataFrame
df = pd.read_csv('BankChurners.csv')
@app.route('/')
def main():

    return render_template('main.html')

@app.route('/distribution', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        selected_column = request.form['column']
        column_data = df[selected_column]

        # Create histogram
        hist_trace = go.Histogram(x=column_data, nbinsx=10, name='Histogram')

        # Create box plot
        box_trace = go.Box(y=column_data, name='Box Plot')

        # Create density plot
        density_trace = go.Histogram(x=column_data, histnorm='probability', name='Density Plot')

        # Create scatter plot
        scatter_trace = go.Scatter(x=df.index, y=column_data, mode='markers', name='Scatter Plot')

        # Layout for each plot
        hist_layout = go.Layout(title=f'Histogram for Column {selected_column}',
                                xaxis=dict(title=selected_column),
                                yaxis=dict(title='Frequency'))

        box_layout = go.Layout(title=f'Box Plot for Column {selected_column}',
                               xaxis=dict(title=selected_column),
                               yaxis=dict(title='Value'))

        density_layout = go.Layout(title=f'Density Plot for Column {selected_column}',
                                   xaxis=dict(title=selected_column),
                                   yaxis=dict(title='Probability'))

        scatter_layout = go.Layout(title=f'Scatter Plot for Column {selected_column}',
                                   xaxis=dict(title='Index'),
                                   yaxis=dict(title=selected_column))

        # Create separate figures for each plot
        hist_fig = go.Figure(data=[hist_trace], layout=hist_layout)
        box_fig = go.Figure(data=[box_trace], layout=box_layout)
        density_fig = go.Figure(data=[density_trace], layout=density_layout)
        scatter_fig = go.Figure(data=[scatter_trace], layout=scatter_layout)

        # Convert the plots to JSON and pass them to the template
        hist_json = hist_fig.to_json()
        box_json = box_fig.to_json()
        density_json = density_fig.to_json()
        scatter_json = scatter_fig.to_json()

         
        return render_template('index.html', hist_json=hist_json, box_json=box_json, density_json=density_json, scatter_json=scatter_json)

    return render_template('index.html', hist_json=None, box_json=None, density_json=None, scatter_json=None)

@app.route('/alerting')
def alerting_page():
    # Check for null values in the DataFrame
    null_values = df.isnull().any()

    # Get columns with null values
    columns_with_null = list(null_values[null_values].index)

    return render_template('alerting.html', columns_with_null=columns_with_null)


if __name__ == '__main__':
    app.run(debug=True)
