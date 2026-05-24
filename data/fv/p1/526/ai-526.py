import sys
import json
import plotly.graph_objects as go
import os

# Check for command-line argument
if len(sys.argv) != 2:
    print("Usage: python script.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]

# Ensure the JSON file exists
if not os.path.exists(json_path):
    print(f"Error: JSON file not found at '{json_path}'")
    sys.exit(1)

# Derive base filename for output
filename_base = os.path.splitext(os.path.basename(json_path))[0]

# Load data from the specified JSON file
with open(json_path, 'r', encoding='utf-8') as f:
    chart_info = json.load(f)

# Extract data, texts, and colors from the JSON structure
data = chart_info['chart_data']
texts = chart_info['texts']
colors = chart_info['colors']

# Create the figure object
fig = go.Figure()

# Add the bar trace using the multicategory x-axis format
fig.add_trace(go.Bar(
    x=[data['x_level1'], data['x_level2']],
    y=data['y'],
    marker_color=colors['bar_color'],
    showlegend=False
))

# Update the layout for a clean, accurate representation
fig.update_layout(
    font_family="Arial",
    title={
        'text': texts['title'],
        'x': 0.5,
        'xanchor': 'center',
        'yanchor': 'top',
        'font': {'size': 20}
    },
    plot_bgcolor='white',
    xaxis={
        'type': 'multicategory',
        'showgrid': False,
        'showline': True,
        'linewidth': 1,
        'linecolor': 'black',
        'tickson': 'boundaries',
        'showdividers': True,  # Show lines between major categories
        'dividercolor': 'black',
        'dividerwidth': 1
    },
    yaxis={
        'title_text': texts['y_axis_title'],
        'showgrid': True,
        'gridcolor': '#d3d3d3',
        'range': [0, 200],
        'dtick': 20,
        'showline': True,
        'linewidth': 1,
        'linecolor': 'black',
        'zeroline': False
    },
    margin=dict(l=60, r=40, t=80, b=80),
    bargap=0.15
)

# Generate the output image
output_filename = f"{filename_base}.png"
fig.write_image(output_filename, scale=2)

print(f"Chart saved as {output_filename}")