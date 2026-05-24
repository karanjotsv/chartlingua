import sys
import json
import plotly.graph_objects as go
from pathlib import Path

# Check for command-line argument
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <path_to_json_file>")
    sys.exit(1)

# Get the JSON file path from the command-line argument
json_file_path = Path(sys.argv[1])

# Check if the file exists
if not json_file_path.is_file():
    print(f"Error: JSON file not found at '{json_file_path}'")
    sys.exit(1)

# Read data from the JSON file
with open(json_file_path, 'r', encoding='utf-8') as f:
    chart_info = json.load(f)

# Extract data, texts, and colors from the loaded JSON
chart_data = chart_info.get('chart_data', [])
texts = chart_info.get('texts', {})
colors = chart_info.get('colors', [])

# Prepare data for Plotly
x_values = [d['x'] for d in chart_data]
y_values = [d['y'] for d in chart_data]

# Create the figure
fig = go.Figure()

# Add the bar trace
fig.add_trace(go.Bar(
    x=x_values,
    y=y_values,
    marker_color=colors[0] if colors else None,
    text=y_values,
    textposition='outside',
    textfont=dict(family="Arial", size=12, color='black'),
    cliponaxis=False,
    hoverinfo='none'
))

# Update layout
fig.update_layout(
    title_text=texts.get('title'),
    plot_bgcolor='white',
    paper_bgcolor='white',
    showlegend=False,
    font=dict(family="Arial", size=12, color='black'),
    margin=dict(l=80, r=40, t=50, b=100),
    xaxis=dict(
        title_text=texts.get('x_axis_title'),
        tickvals=x_values,
        tickmode='array',
        type='category',
        showgrid=False,
        showline=True,
        linewidth=1,
        linecolor='lightgrey',
        zeroline=False
    ),
    yaxis=dict(
        title_text=texts.get('y_axis_title'),
        range=[0, 20],
        tickvals=[0, 2.5, 5, 7.5, 10, 12.5, 15, 17.5, 20],
        showgrid=True,
        gridcolor='#EAEAEA',
        zeroline=False,
        showline=False
    )
)

# Add annotations for source information
annotations = []
if texts.get('source_left'):
    annotations.append(
        dict(
            xref='paper', yref='paper',
            x=0, y=-0.2,
            xanchor='left', yanchor='top',
            text=texts['source_left'],
            showarrow=False,
            font=dict(family="Arial", size=12)
        )
    )
if texts.get('source_right'):
    annotations.append(
        dict(
            xref='paper', yref='paper',
            x=1, y=-0.2,
            xanchor='right', yanchor='top',
            text=texts['source_right'],
            showarrow=False,
            font=dict(family="Arial", size=12, color='#7f7f7f')
        )
    )

fig.update_layout(annotations=annotations)

# Define output image path
output_image_path = json_file_path.with_suffix('.png')

# Save the figure as a PNG image
fig.write_image(str(output_image_path), scale=2)

print(f"Chart saved to {output_image_path}")