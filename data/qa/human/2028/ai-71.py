import sys
import json
import plotly.graph_objects as go
from pathlib import Path

# Check for command-line argument
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <json_file_path>")
    sys.exit(1)

# Get the JSON file path from the command-line argument
json_file_path = Path(sys.argv[1])

# Check if the JSON file exists
if not json_file_path.is_file():
    print(f"Error: File not found at {json_file_path}")
    sys.exit(1)

# Read and parse the JSON file
with open(json_file_path, 'r', encoding='utf-8') as f:
    chart_config = json.load(f)

# Extract data, texts, and colors from the JSON
chart_data = chart_config.get('chart_data', [])
texts = chart_config.get('texts', {})
colors = chart_config.get('colors', [])

# Prepare data for Plotly
# Reverse data to match the visual top-to-bottom order of the original chart
categories = [item['category'] for item in reversed(chart_data)]
values = [item['value'] for item in reversed(chart_data)]

# Format text for data labels to use a space as a thousands separator
text_labels = [f'{v:,}'.replace(',', ' ') for v in values]

# Create the figure
fig = go.Figure()

# Add the bar trace
fig.add_trace(go.Bar(
    y=categories,
    x=values,
    orientation='h',
    marker=dict(color=colors[0]),
    text=text_labels,
    textposition='auto',
    insidetextanchor='middle',
    textfont=dict(
        family="Arial",
        color='black'
    )
))

# Update layout
fig.update_layout(
    font=dict(family="Arial", size=12, color="black"),
    title=dict(
        text=texts.get('title'),
        x=0.05,
        xanchor='left'
    ),
    xaxis=dict(
        title=texts.get('x_axis_title'),
        showgrid=True,
        gridcolor='#e0e0e0',
        gridwidth=1,
        griddash='dot',
        zeroline=False,
        showline=False,
        showticklabels=False # Hide x-axis labels as values are on bars
    ),
    yaxis=dict(
        title=texts.get('y_axis_title'),
        showgrid=False,
        zeroline=False,
        showline=False,
        autorange="reversed" # Ensures categories are plotted top-to-bottom
    ),
    plot_bgcolor='white',
    paper_bgcolor='white',
    showlegend=False,
    margin=dict(l=100, r=60, t=50, b=80),
    annotations=[
        dict(
            text=texts.get('source'),
            showarrow=False,
            xref='paper', yref='paper',
            x=0.98, y=-0.12,
            xanchor='right', yanchor='top',
            align='right',
            font=dict(size=12)
        )
    ]
)

# Derive the output filename from the input JSON filename
output_filename = json_file_path.stem + '.png'

# Save the figure as a PNG image
fig.write_image(output_filename, scale=2)

print(f"Chart saved as {output_filename}")