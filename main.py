from flask import Flask, render_template
import requests
import plotly.graph_objs as go

app = Flask(__name__)

# Function to fetch COVID-19 data from the API
def fetch_covid_data(api_key):
    url = f"https://api.covidactnow.org/v2/states.json?apiKey={api_key}"
    response = requests.get(url)
    data = response.json()
    return data

# Function to extract necessary data for plotting
def extract_data_for_plotting(data):
    states = []
    cases = []
    deaths = []
    
    for state_data in data:
        states.append(state_data['state'])
        cases.append(state_data['actuals']['cases'])
        deaths.append(state_data['actuals']['deaths'])
    
    return states, cases, deaths

# Route for the dashboard
@app.route('/')
def dashboard():
    api_key = "03f8a3198ce74eb6bfb7f872337b7f88"  # Replace this with your API key
    data = fetch_covid_data(api_key)
    states, cases, deaths = extract_data_for_plotting(data)

    # Create plots
    case_plot = go.Bar(x=states, y=cases, name='Cases')
    death_plot = go.Bar(x=states, y=deaths, name='Deaths')

    # Layout
    layout = go.Layout(title='COVID-19 Cases and Deaths by State',
                       xaxis=dict(title='States'),
                       yaxis=dict(title='Count'))

    # Plot configuration
    case_fig = go.Figure(data=[case_plot], layout=layout)
    death_fig = go.Figure(data=[death_plot], layout=layout)

    case_graph = case_fig.to_html(full_html=False)
    death_graph = death_fig.to_html(full_html=False)

    return render_template('dashboard.html', case_graph=case_graph, death_graph=death_graph)

if __name__ == '__main__':
	app.run(host="0.0.0.0", debug=False)
