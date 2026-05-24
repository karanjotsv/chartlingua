import sys
import json
import plotly.graph_objects as go
from pathlib import Path

# Ensure a JSON file path is provided as a command-line argument
if len(sys.argv) != 2:
    print(f"Usage: python {Path(__file__).name} <path_to_json>")
    sys.exit(1)

json_path = sys.argv[1]

# Read and parse the JSON file
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_info = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at '{json_path}'")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from '{json_path}'")
    sys.exit(1)

# Extract data, texts, and colors from the JSON structure
data = chart_info['chart_data']
texts = chart_info['texts']
colors = chart_info['colors']
categories = data['categories']

# Initialize the figure
fig = go.Figure()

# Add traces by iterating through the series in the JSON data
for i, series in enumerate(data['series']):
    if series['type'] == 'bar':
        fig.add_trace(go.Bar(
            x=categories,
            y=series['data'],
            name=series['name'],
            marker_color=colors[i],
            showlegend=series['show_in_legend']
        ))
    elif series['type'] == 'line':
        fig.add_trace(go.Scatter(
            x=categories,
            y=series['data'],
            name=series['name'],
            mode='lines',
            line=dict(color=colors[i], width=3),
            yaxis=series.get('y_axis'),
            showlegend=series['show_in_legend']
        ))

# Update the layout of the figure
fig.update_layout(
    barmode='stack',
    bargap=0.15,
    font_family="Arial",
    plot_bgcolor='white',
    xaxis=dict(
        title_text=texts['x_axis_title'],
        tickmode='linear',
        showgrid=False,
        zeroline=False
    ),
    yaxis=dict(
        title_text=texts['y_axis_title'],
        range=[0, 30],
        tickformat=".2f",
        dtick=5,
        showgrid=True,
        gridcolor='#e0e0e0',
        zeroline=True,
        zerolinecolor='#a0a0a0'
    ),
    yaxis2=dict(
        title_text=texts['y2_axis_title'],
        overlaying='y',
        side='right',
        autorange='reversed',
        range=[10, 1],
        tickmode='linear',
        dtick=1,
        showgrid=False,
        zeroline=False
    ),
    legend=dict(
        orientation='h',
        yanchor='top',
        y=-0.2,
        xanchor='center',
        x=0.5
    ),
    margin=dict(l=60, r=60, t=30, b=100)
)

# Derive the output filename from the input JSON path
output_filename_base = Path(json_path).stem
output_image_path = f"{output_filename_base}.png"

# Save the figure as a PNG image
fig.write_image(output_image_path, scale=2)

print(f"Chart saved to {output_image_path}")