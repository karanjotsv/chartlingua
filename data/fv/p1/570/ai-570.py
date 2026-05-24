import sys
import json
import plotly.graph_objects as go

# Check for command-line argument
if len(sys.argv) != 2:
    print("Usage: python script.py <path_to_json_file>")
    sys.exit(1)

# Get JSON file path from command-line argument
json_path = sys.argv[1]

# Read data from JSON file
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_data = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_path}")
    sys.exit(1)

# Extract data for plotting
data = chart_data['chart_data']
texts = chart_data['texts']
colors = chart_data['colors']

categories = [item['category'] for item in data]
values = [item['value'] for item in data]

# Create the figure
fig = go.Figure()

# Add bar trace
fig.add_trace(go.Bar(
    x=categories,
    y=values,
    text=[f'{v:,}' for v in values],
    textposition='outside',
    marker_color=colors[0],
    hoverinfo='none',
    cliponaxis=False # Prevent text from being clipped
))

# Combine title and subtitle if available
title_text = texts['title']
if texts['subtitle']:
    title_text += f"<br><sub>{texts['subtitle']}</sub>"

# Update layout
fig.update_layout(
    title={
        'text': title_text,
        'y': 0.95,
        'x': 0.5,
        'xanchor': 'center',
        'yanchor': 'top'
    },
    font={
        'family': "Arial",
        'size': 12,
        'color': "black"
    },
    xaxis={
        'title_text': texts['x_axis_title'],
        'tickangle': -45,
        'showgrid': False,
        'zeroline': False
    },
    yaxis={
        'title_text': texts['y_axis_title'],
        'showgrid': True,
        'gridcolor': '#D3D3D3',
        'zeroline': False,
        'range': [0, 8000],
        'dtick': 1000,
        'tickformat': ','
    },
    plot_bgcolor='white',
    showlegend=False,
    margin={'t': 60, 'r': 30, 'b': 150, 'l': 60},
    autosize=False,
    width=800,
    height=600
)

# Set font for text on bars
fig.update_traces(textfont={'family': 'Arial', 'size': 12, 'color': 'black'})


# Determine output filename and save image
output_filename = json_path.rsplit('.', 1)[0] + '.png'
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")