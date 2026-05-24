import sys
import json
import os
import plotly.graph_objects as go

# Check for command-line argument
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]

# Check if the file exists
if not os.path.exists(json_path):
    print(f"Error: File not found at {json_path}")
    sys.exit(1)

# Read data from the JSON file
with open(json_path, 'r', encoding='utf-8') as f:
    config = json.load(f)

# Extract data for the chart
chart_data = config.get('chart_data', [])
texts = config.get('texts', {})
colors = config.get('colors', [])

# Prepare data for Plotly
labels = [item['label'] for item in chart_data]
values = [item['value'] for item in chart_data]

# Create the pie chart trace
pie_trace = go.Pie(
    labels=labels,
    values=values,
    marker=dict(colors=colors, line=dict(color='#000000', width=1)),
    hoverinfo='label+percent',
    textinfo='none',
    sort=False,
    direction='clockwise',
    rotation=65
)

# Create the figure
fig = go.Figure(data=[pie_trace])

# Update layout
fig.update_layout(
    title=dict(
        text=texts.get('title'),
        y=0.05,
        x=0.5,
        xanchor='center',
        yanchor='bottom',
        font=dict(
            family="Arial",
            size=20,
            color="black"
        )
    ),
    showlegend=False,
    margin=dict(l=20, r=20, t=20, b=80),
    paper_bgcolor='white',
    plot_bgcolor='white',
    font=dict(family="Arial", color="black"),
    width=600,
    height=550
)

# Add annotations from JSON
annotations = texts.get('annotations', [])
for ann in annotations:
    fig.add_annotation(
        text=ann.get('text'),
        x=ann.get('x'),
        y=ann.get('y'),
        showarrow=ann.get('showarrow', False),
        font=dict(
            family="Arial",
            size=ann.get('font_size', 12),
            color="black"
        ),
        align=ann.get('align', 'center'),
        ax=ann.get('ax', 0),
        ay=ann.get('ay', 0),
        arrowhead=ann.get('arrowhead', 0),
        arrowwidth=ann.get('arrowwidth', 1),
        arrowcolor=ann.get('arrowcolor', 'black'),
        xanchor='center',
        yanchor='middle'
    )

# Determine output filename from JSON path
base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_filename}.png"

# Save the figure as a PNG image
fig.write_image(output_filename, scale=2)

print(f"Chart saved as {output_filename}")