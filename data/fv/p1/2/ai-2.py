import sys
import json
import plotly.graph_objects as go
from pathlib import Path

# Check if a file path is provided
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <json_file_path>")
    sys.exit(1)

json_file_path = sys.argv[1]

# Read data from the JSON file
try:
    with open(json_file_path, 'r', encoding='utf-8') as f:
        chart_data_json = json.load(f)
except FileNotFoundError:
    print(f"Error: The file '{json_file_path}' was not found.")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from the file '{json_file_path}'.")
    sys.exit(1)

# Extract data and texts
chart_data = chart_data_json.get('chart_data', [])
texts = chart_data_json.get('texts', {})
colors = chart_data_json.get('colors', [])

# Initialize the figure
fig = go.Figure()

# Add traces for each density plot
for i, series in enumerate(chart_data):
    fig.add_trace(go.Scatter(
        x=series['x'],
        y=series['y'],
        name=series['name'],
        mode='lines',
        line=dict(color='black', width=1.5, shape='spline'),
        fill='tozeroy',
        fillcolor=colors[i]
    ))

# Update layout
fig.update_layout(
    xaxis_title=texts.get('x_axis_title'),
    yaxis_title=texts.get('y_axis_title'),
    legend_title_text=texts.get('legend_title'),
    font=dict(
        family="Arial",
        size=12,
        color="black"
    ),
    plot_bgcolor='#EBEBEB',
    paper_bgcolor='white',
    width=700,
    height=700,
    margin=dict(l=60, r=40, t=40, b=60),
    xaxis=dict(
        showline=True,
        linewidth=1,
        linecolor='black',
        mirror=True,
        ticks='outside',
        gridcolor='white',
        gridwidth=1,
        zeroline=False,
        range=[-0.2, 5.2]
    ),
    yaxis=dict(
        showline=True,
        linewidth=1,
        linecolor='black',
        mirror=True,
        ticks='outside',
        gridcolor='white',
        gridwidth=1,
        zeroline=False,
        range=[-0.05, 1.1]
    ),
    legend=dict(
        x=0.98,
        y=0.98,
        xanchor='right',
        yanchor='top',
        bgcolor='rgba(255, 255, 255, 0)',
        bordercolor='black',
        borderwidth=0
    )
)

# Determine output filename from the input JSON path
json_path = Path(json_file_path)
filename_base = json_path.stem
output_filename = f"{filename_base}.png"

# Save the figure as a PNG image
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")