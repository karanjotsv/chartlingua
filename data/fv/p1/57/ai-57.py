import sys
import json
import plotly.graph_objects as go
import datetime
import os

# Check for the required command-line argument
if len(sys.argv) != 2:
    print("Usage: python <script_name>.py <json_file_path>")
    sys.exit(1)

# Get the JSON file path from the command-line argument
json_file_path = sys.argv[1]

# Read the JSON file
try:
    with open(json_file_path, 'r', encoding='utf-8') as f:
        chart_data_json = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_file_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_file_path}")
    sys.exit(1)

# Extract data from the JSON object
chart_data = chart_data_json.get('chart_data', [])
texts = chart_data_json.get('texts', {})
colors = chart_data_json.get('colors', [])

# Prepare data for Plotly
# Convert date strings to datetime objects for correct plotting
x_values = [datetime.datetime.strptime(item['x'], '%d.%m.%y') for item in chart_data]
y_values = [item['y'] for item in chart_data]

# Create the figure
fig = go.Figure()

# Add the line trace
if chart_data:
    fig.add_trace(go.Scatter(
        x=x_values,
        y=y_values,
        mode='lines+markers',
        line=dict(color=colors[0] if colors else '#0000FF', width=1.5),
        marker=dict(color=colors[0] if colors else '#0000FF', symbol='diamond', size=4),
        showlegend=False
    ))

# Build the title string
title_text = texts.get('title') or ''
if texts.get('subtitle'):
    title_text += f"<br><sub>{texts.get('subtitle')}</sub>"

# Configure layout to match the original image
fig.update_layout(
    title_text=title_text,
    font=dict(family="Arial", size=12, color="black"),
    plot_bgcolor='white',
    paper_bgcolor='white',
    xaxis=dict(
        showgrid=False,
        showline=True,
        linewidth=1,
        linecolor='black',
        mirror=True,
        tickvals=['01.08.04', '17.02.05', '05.09.05', '24.03.06', '10.10.06', '28.04.07', '14.11.07'],
        ticktext=['01.08.04', '17.02.05', '05.09.05', '24.03.06', '10.10.06', '28.04.07', '14.11.07']
    ),
    yaxis=dict(
        title_text=texts.get('y_axis_title'),
        range=[100, 550],
        dtick=25,
        showgrid=True,
        gridwidth=1,
        gridcolor='black',
        showline=True,
        linewidth=1,
        linecolor='black',
        mirror=True,
        zeroline=False
    ),
    margin=dict(l=50, r=20, t=30, b=50),
    showlegend=False
)

# Determine the output filename from the input JSON path
base_filename = os.path.splitext(os.path.basename(json_file_path))[0]
output_filename = f"{base_filename}.png"

# Save the figure as a PNG image
fig.write_image(output_filename, scale=2)

print(f"Chart saved as {output_filename}")