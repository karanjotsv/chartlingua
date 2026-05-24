import sys
import json
import plotly.graph_objects as go
import os

# --- Main execution ---
if len(sys.argv) != 2:
    print("Usage: python <script_name>.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]

# Derive the output filename from the input JSON path
# e.g., 'path/to/chart.json' -> 'chart.png'
base_name = os.path.basename(json_path)
filename_sans_ext = os.path.splitext(base_name)[0]
output_filename = f"{filename_sans_ext}.png"

# Read chart data from the specified JSON file
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_info = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at '{json_path}'")
    sys.exit(1)

# Extract data, texts, and colors from the JSON structure
chart_data = chart_info.get('chart_data', [])
texts = chart_info.get('texts', {})
colors = chart_info.get('colors', [])

# Prepare data for Plotly trace
categories = [d['category'] for d in chart_data]
values = [d['value'] for d in chart_data]

# Create the figure object
fig = go.Figure()

# Add the bar trace to the figure
fig.add_trace(go.Bar(
    x=categories,
    y=values,
    marker_color=colors[0] if colors else '#0000FF',
    showlegend=False
))

# Update the layout of the chart for a professional and accurate appearance
fig.update_layout(
    title={
        'text': texts.get('title', ''),
        'y': 0.95,
        'x': 0.5,
        'xanchor': 'center',
        'yanchor': 'top',
        'font': {'size': 24}
    },
    xaxis_title=texts.get('x_axis_title', ''),
    yaxis_title=texts.get('y_axis_title', ''),
    font={
        'family': "Arial",
        'size': 14,
        'color': "black"
    },
    plot_bgcolor='white',
    paper_bgcolor='white',
    xaxis={
        'type': 'category',
        'showline': True,
        'linewidth': 1,
        'linecolor': '#333',
        'showgrid': False,
        'tickfont': {'size': 14}
    },
    yaxis={
        'range': [0, 20],
        'dtick': 5,
        'showline': True,
        'linewidth': 1,
        'linecolor': '#333',
        'gridcolor': '#CCCCCC',
        'tickfont': {'size': 14}
    },
    margin={'l': 100, 'r': 40, 't': 100, 'b': 80}
)

# Write the chart to a high-resolution PNG file
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")