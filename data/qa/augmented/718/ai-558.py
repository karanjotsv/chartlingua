import sys
import json
import os
import plotly.graph_objects as go

# --- 1. Load Data from JSON ---
# Ensure a command-line argument is provided
if len(sys.argv) != 2:
    print(f"Usage: python {os.path.basename(__file__)} <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]

# Check if the JSON file exists
if not os.path.exists(json_path):
    print(f"Error: JSON file not found at '{json_path}'")
    sys.exit(1)

# Read the JSON file, which is the sole source of data and text
with open(json_path, 'r', encoding='utf-8') as f:
    config = json.load(f)

chart_data = config['chart_data']
texts = config['texts']
colors = config['colors']

# --- 2. Create Plotly Figure ---
fig = go.Figure()

# Add traces by iterating through the chart_data from the JSON
for i, series in enumerate(chart_data):
    fig.add_trace(go.Bar(
        x=series['x'],
        y=series['y'],
        name=series['name'],
        marker_color=colors[i],
        marker_line_width=0 # To match the solid bars in the original
    ))

# --- 3. Configure Layout ---
# Use a dictionary for cleaner layout updates
layout_config = {
    'barmode': 'stack',
    'plot_bgcolor': 'white',
    'paper_bgcolor': 'white',
    'font': {'family': "Arial", 'size': 12},
    'margin': {'l': 90, 'r': 40, 'b': 120, 't': 50},
    'yaxis': {
        'title': texts['y_axis_title'],
        'tickmode': 'array',
        'tickvals': [0, 500000, 1000000, 1500000, 2000000, 2500000, 3000000, 3500000],
        'ticktext': ['0', '500 000', '1 000 000', '1 500 000', '2 000 000', '2 500 000', '3 000 000', '3 500 000'],
        'gridcolor': '#EAEAEA',
        'zeroline': False,
        'showline': False
    },
    'xaxis': {
        'title': texts['x_axis_title'],
        'showgrid': False,
        'showline': True,
        'linecolor': 'black'
    },
    'legend': {
        'orientation': "h",
        'yanchor': "bottom",
        'y': -0.25,
        'xanchor': "center",
        'x': 0.5
    },
    'annotations': []
}

# Add title and subtitle if they exist in the JSON
# This part is omitted since the titles are null, but it shows how to handle them
if texts.get('title'):
    layout_config['title'] = {
        'text': texts['title'],
        'x': 0.05,
        'xanchor': 'left'
    }

# Add source annotation if it exists
if texts.get('source'):
    layout_config['annotations'].append(
        {
            'text': texts['source'],
            'align': 'right',
            'showarrow': False,
            'xref': 'paper',
            'yref': 'paper',
            'x': 1.0,
            'y': -0.35,
            'xanchor': 'right',
            'yanchor': 'bottom',
            'font': {'size': 10, 'color': 'grey'}
        }
    )

fig.update_layout(**layout_config)


# --- 4. Output Image ---
# Derive the output filename from the input JSON file path
base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_filename}.png"

# Save the figure as a PNG file
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")