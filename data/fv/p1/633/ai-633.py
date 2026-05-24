import sys
import json
import os
import plotly.graph_objects as go

# Check if a file path is provided as a command-line argument
if len(sys.argv) != 2:
    print("Usage: python <script_name>.py <path_to_json_file>")
    sys.exit(1)

# The path to the JSON file is taken from the first command-line argument
json_path = sys.argv[1]

# Read the JSON data from the file
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_data = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_path}")
    sys.exit(1)

# Create a new figure
fig = go.Figure()

# Extract data for plotting
data_series = chart_data['chart_data']
colors = chart_data['colors']
texts = chart_data['texts']

# Add a trace for each data series
for i, series in enumerate(data_series):
    fig.add_trace(go.Scatter(
        x=series['x'],
        y=series['y'],
        name=series['name'],
        mode='lines',
        line=dict(
            color=colors[i % len(colors)],
            dash=series.get('line_style', 'solid')
        )
    ))

# Update the layout of the chart
fig.update_layout(
    title_text=texts.get('title'),
    title_x=0.5,
    xaxis_title=texts.get('x_axis_title'),
    yaxis_title=texts.get('y_axis_title'),
    font=dict(family="Arial", size=12),
    plot_bgcolor='white',
    xaxis=dict(
        range=[20, 75],
        showgrid=True,
        gridwidth=1,
        gridcolor='#d3d3d3',
        tickmode='linear',
        dtick=5,
        linecolor='black'
    ),
    yaxis=dict(
        range=[140, 200],
        showgrid=True,
        gridwidth=1,
        gridcolor='#d3d3d3',
        griddash='dash',
        tickmode='linear',
        dtick=10,
        linecolor='black'
    ),
    legend=dict(
        x=0.22,
        y=0.02,
        xanchor='left',
        yanchor='bottom',
        bgcolor='rgba(255, 255, 255, 0.8)'
    ),
    margin=dict(t=80, b=60, l=70, r=40)
)

# Determine the output filename from the input JSON path
base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_filename}.png"

# Save the figure to a PNG file
fig.write_image(output_filename, scale=2)

print(f"Chart successfully generated and saved to {output_filename}")