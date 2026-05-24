import sys
import json
import plotly.graph_objects as go
from pathlib import Path

# Check for command-line argument
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <path_to_json>")
    sys.exit(1)

# Get the JSON file path from the command-line argument
json_path = Path(sys.argv[1])
if not json_path.is_file():
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)

# Load data from the specified JSON file
with open(json_path, 'r', encoding='utf-8') as f:
    config = json.load(f)

# Extract data, texts, and colors from the JSON structure
chart_data = config['chart_data']
texts = config['texts']
colors = config['colors']

# Prepare data for Plotly
categories = [item['category'] for item in chart_data]
values = [item['value'] for item in chart_data]

# Create the figure
fig = go.Figure()

# Add the horizontal bar trace
fig.add_trace(go.Bar(
    y=categories,
    x=values,
    orientation='h',
    marker=dict(color=colors[0]),
    text=values,
    textposition='outside',
    texttemplate='%{x}',
    cliponaxis=False
))

# Update layout for a professional appearance
fig.update_layout(
    title_text=texts.get('title'),
    font=dict(family="Arial", size=12),
    plot_bgcolor='white',
    paper_bgcolor='white',
    xaxis=dict(
        title=texts.get('x_axis_title'),
        showgrid=True,
        gridcolor='#e9e9e9',
        gridwidth=1,
        griddash='dot',
        zeroline=False,
        range=[0, max(values) * 1.18] # Ensure space for labels
    ),
    yaxis=dict(
        title=texts.get('y_axis_title'),
        autorange='reversed',  # Display categories from top to bottom
        showgrid=False
    ),
    margin=dict(l=120, r=40, t=40, b=80),
    showlegend=False,
    annotations=[
        dict(
            text=texts.get('source'),
            align='right',
            showarrow=False,
            xref='paper',
            yref='paper',
            x=0.98,
            y=-0.12,
            xanchor='right',
            yanchor='top'
        )
    ]
)

# Determine the output filename from the input JSON path
output_filename = json_path.stem + '.png'

# Save the figure as a PNG image
fig.write_image(output_filename, scale=2)

print(f"Chart successfully generated and saved to {output_filename}")