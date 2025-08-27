"""Test script to verify Dash is working"""

import dash
from dash import html

# Create a simple test app
app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("Test Dashboard"),
    html.P("If you can see this, Dash is working!")
])

if __name__ == '__main__':
    print("Starting test server on http://localhost:8051")
    app.run(debug=True, port=8051, host='0.0.0.0')