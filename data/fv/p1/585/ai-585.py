import sys
import json
import os
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print(f"Usage: python {os.path.basename(__file__)} <json_file_path>")
    sys.exit(1)

json_path = sys.argv[1]

if not os.path.exists(json_path):
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)

try:
    with open(json_path, 'r', encoding='utf-8') as f:
        config = json.load(f)
except json.JSONDecodeError:
    print(f"Error: Invalid JSON format in {json_path}")
    sys.exit(1)

# Extract data and texts from the JSON structure
texts = config['texts']
colors = config['colors']
chart_data = config['chart_data']
legend_items = texts['legend_items']

# Prepare data for Plotly's grouped bar chart structure
categories = [d['category'] for d in chart_data]
num_series = len(legend_items)
series_data = [[d['values'][i] for d in chart_data] for i in range(num_series)]

# Create the figure
fig = go.Figure()

# Add a bar trace for each data series
for i in range(num_series):
    fig.add_trace(go.Bar(
        x=categories,
        y=series_data[i],
        name=legend_items[i],
        marker_color=colors[i]
    ))

# Update the layout for a clean, professional appearance
fig.update_layout(
    barmode='group',
    title={
        'text': texts.get('title', ''),
        'y': 0.95,
        'x': 0.5,
        'xanchor': 'center',
        'yanchor': 'top'
    },
    xaxis_title=texts.get('x_axis_title'),
    yaxis_title=texts.get('y_axis_title'),
    xaxis={
        'showgrid': False,
        'zeroline': False
    },
    yaxis={
        'range': [0, 35],
        'dtick': 5,
        'ticksuffix': '%',
        'gridcolor': '#E0E0E0',
        'zeroline': False
    },
    legend={
        'orientation': 'h',
        'yanchor': 'bottom',
        'y': -0.3,
        'xanchor': 'center',
        'x': 0.5
    },
    font={
        'family': 'Arial',
        'size': 12
    },
    plot_bgcolor='white',
    margin=dict(t=80, b=120, l=60, r=40)
)

# Determine the output filename from the input JSON path
base_filename, _ = os.path.splitext(os.path.basename(json_path))
output_filename = f"{base_filename}.png"

# Save the figure as a high-resolution PNG image
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")