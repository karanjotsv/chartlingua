import sys
import json
import plotly.graph_objects as go
from pathlib import Path

# Check if a file path is provided as a command-line argument
if len(sys.argv) < 2:
    print(f"Usage: python {sys.argv[0]} <json_file_path>")
    sys.exit(1)

json_path = sys.argv[1]

# Read the chart data and configuration from the specified JSON file
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_config = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_path}")
    sys.exit(1)

# Extract data, texts, and colors from the loaded configuration
chart_data = chart_config.get('chart_data', [])
texts = chart_config.get('texts', {})
colors = chart_config.get('colors', [])

# Initialize the figure
fig = go.Figure()

# Add a bar trace for each data series specified in the JSON
for i, series in enumerate(chart_data):
    fig.add_trace(go.Bar(
        x=series['x'],
        y=series['y'],
        name=series['name'],
        marker_color=colors[i % len(colors)],
        text=series['y'],
        textposition='outside',
        textfont=dict(
            family="Arial",
            size=12,
            color='black'
        ),
        cliponaxis=False
    ))

# Update the layout of the chart
fig.update_layout(
    barmode='group',
    font=dict(family="Arial"),
    title_text=texts.get('title'),
    yaxis=dict(
        title=texts.get('y_axis_title'),
        range=[0, 70],
        dtick=10,
        showgrid=True,
        gridcolor='lightgray',
        zeroline=False
    ),
    xaxis=dict(
        title=texts.get('x_axis_title'),
        tickfont=dict(size=12)
    ),
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=-0.25,
        xanchor="center",
        x=0.5
    ),
    plot_bgcolor='white',
    paper_bgcolor='white',
    margin=dict(l=60, r=40, b=120, t=40),
    annotations=[
        dict(
            text=texts.get('note'),
            showarrow=False,
            xref='paper',
            yref='paper',
            x=0,
            y=-0.35,
            xanchor='left',
            yanchor='bottom',
            font=dict(color='#007bff') # Matching blue color for link-like text
        ),
        dict(
            text=texts.get('source'),
            showarrow=False,
            xref='paper',
            yref='paper',
            x=1,
            y=-0.35,
            xanchor='right',
            yanchor='bottom'
        )
    ]
)

# Determine the output filename from the input JSON path
base_filename = Path(json_path).stem
output_filename = f"{base_filename}.png"

# Save the figure to a PNG file
fig.write_image(output_filename, scale=2)

print(f"Chart saved as {output_filename}")