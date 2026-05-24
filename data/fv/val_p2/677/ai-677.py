import sys
import json
import os
import plotly.graph_objects as go

# Ensure a JSON file path is provided as a command-line argument
if len(sys.argv) != 2:
    print("Usage: python <script_name>.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]

# Load chart data and configuration from the specified JSON file
with open(json_path, 'r', encoding='utf-8') as f:
    chart_info = json.load(f)

# Extract data for plotting
data_series = chart_info.get('chart_data', [])
colors = chart_info.get('colors', [])
texts = chart_info.get('texts', {})

# Initialize a new figure
fig = go.Figure()

# Add traces to the figure based on the chart data
for i, series in enumerate(data_series):
    fig.add_trace(go.Scatter(
        x=series.get('x'),
        y=series.get('y'),
        mode='lines',
        line=dict(
            color=colors[i % len(colors)] if colors else '#000000',
            width=5
        ),
        name=series.get('series_name', ''),
        showlegend=False
    ))

# Configure the layout to match the original image's minimalist aesthetic
fig.update_layout(
    plot_bgcolor='#000000',
    paper_bgcolor='#000000',
    xaxis=dict(
        visible=False,
        showgrid=False,
        zeroline=False
    ),
    yaxis=dict(
        visible=False,
        showgrid=False,
        zeroline=False
    ),
    margin=dict(l=0, r=0, t=0, b=0),
    font=dict(family="Arial")
)

# Determine the output image filename from the input JSON filename
base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_image_path = f"{base_filename}.png"

# Save the generated chart as a high-resolution PNG image
fig.write_image(output_image_path, scale=2)