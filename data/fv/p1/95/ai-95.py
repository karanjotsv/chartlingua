import sys
import json
import pathlib
import plotly.graph_objects as go

# This script requires a command-line argument for the JSON file path.
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <path_to_json_file>")
    sys.exit(1)

json_path = pathlib.Path(sys.argv[1])
if not json_path.is_file():
    print(f"Error: Input JSON file not found at {json_path}")
    sys.exit(1)

# Load all data and text from the specified JSON file.
with open(json_path, 'r', encoding='utf-8') as f:
    config = json.load(f)

chart_data = config['chart_data']
texts = config['texts']
colors = config['colors']

# Prepare data for the Plotly pie chart trace.
labels = [item['label'] for item in chart_data]
values = [item['value'] for item in chart_data]

# Initialize the figure.
fig = go.Figure()

# Add the pie chart trace.
# 'sort=False' is critical to preserve the order of slices as defined in the JSON.
fig.add_trace(go.Pie(
    labels=labels,
    values=values,
    marker_colors=colors,
    hole=0,
    sort=False,
    direction='clockwise',
    textinfo='none',  # The original chart does not show percentages on slices.
    hoverinfo='label+percent'
))

# Configure the layout, titles, fonts, and legend.
# This section uses the 'texts' dictionary from the JSON for all display text.
title_text = texts.get('title', '')
if texts.get('subtitle'):
    title_text += f"<br><sub>{texts['subtitle']}</sub>"

source_text = texts.get('source', '')

fig.update_layout(
    title={
        'text': title_text,
        'y': 0.95,
        'x': 0.5,
        'xanchor': 'center',
        'yanchor': 'top',
        'font': {'size': 20}
    },
    font={
        'family': "Arial",
        'size': 12,
        'color': 'black'
    },
    legend={
        'orientation': "h",
        'yanchor': "bottom",
        'y': -0.15,
        'xanchor': "center",
        'x': 0.5,
        'traceorder': "normal"
    },
    margin={'t': 100, 'b': 100, 'l': 40, 'r': 40},
    paper_bgcolor='white',
    plot_bgcolor='white',
    annotations=[
        {
            'text': source_text,
            'showarrow': False,
            'xref': 'paper',
            'yref': 'paper',
            'x': 0,
            'y': -0.2,
            'xanchor': 'left',
            'yanchor': 'bottom',
            'font': {'size': 10}
        }
    ]
)

# Generate the output PNG image, named after the input JSON file.
output_path = json_path.with_suffix('.png')
fig.write_image(output_path, scale=2)

print(f"Chart successfully generated and saved to {output_path}")