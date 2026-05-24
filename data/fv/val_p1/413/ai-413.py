import sys
import json
import plotly.graph_objects as go
from pathlib import Path

# Check if the JSON file path is provided as a command-line argument
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <json_file_path>")
    sys.exit(1)

json_path = sys.argv[1]

# Ensure the file exists before proceeding
if not Path(json_path).is_file():
    print(f"Error: File not found at {json_path}")
    sys.exit(1)

# Read the JSON data from the file
with open(json_path, 'r', encoding='utf-8') as f:
    chart_data = json.load(f)

# Extract data and text from the JSON structure
data = chart_data['chart_data']
texts = chart_data['texts']
colors = chart_data['colors']
series_names = chart_data['series_names']

# Prepare data for Plotly
categories = [item['category'] for item in data]
num_series = len(series_names)
series_values = [[item['values'][i] for item in data] for i in range(num_series)]

# Create the figure object
fig = go.Figure()

# Add a trace for each data series
for i in range(num_series):
    fig.add_trace(go.Scatter(
        x=categories,
        y=series_values[i],
        name=series_names[i],
        mode='lines+markers+text',
        line=dict(color=colors[i], width=3),
        marker=dict(color=colors[i], size=8),
        text=[f'{val:.2f}' if isinstance(val, float) else str(val) for val in series_values[i]],
        textposition='top center',
        textfont=dict(
            family="Arial",
            size=10,
            color='black'
        )
    ))

# Combine title and subtitle if they exist
title_text = texts['title']
if texts['subtitle']:
    title_text += f"<br><sub>{texts['subtitle']}</sub>"

# Update layout for a professional look, ensuring all elements are visible
fig.update_layout(
    title=dict(
        text=title_text,
        x=0.5,
        xanchor='center'
    ),
    xaxis=dict(
        title=texts.get('x_axis_title'),
        tickangle=-45,
        showgrid=True,
        gridcolor='lightgrey',
        showline=True,
        linewidth=1,
        linecolor='black'
    ),
    yaxis=dict(
        title=texts.get('y_axis_title'),
        range=[0, 12],
        dtick=2.4,
        showgrid=True,
        gridcolor='lightgrey',
        showline=True,
        linewidth=1,
        linecolor='black'
    ),
    font=dict(
        family="Arial",
        size=12,
        color="black"
    ),
    plot_bgcolor='white',
    legend=dict(
        x=1.02,
        y=0.5,
        xanchor='left',
        yanchor='middle'
    ),
    margin=dict(l=60, r=150, t=80, b=120)
)

# Generate the output filename from the input JSON path
filename_base = Path(json_path).stem
output_filename = f"{filename_base}.png"

# Save the figure to a PNG file
fig.write_image(output_filename, scale=2)

print(f"Chart saved as {output_filename}")