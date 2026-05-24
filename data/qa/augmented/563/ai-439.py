import sys
import json
import os
import plotly.graph_objects as go

# Ensure a JSON file path is provided as a command-line argument
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <json_file_path>")
    sys.exit(1)

json_path = sys.argv[1]

# Check if the JSON file exists
if not os.path.exists(json_path):
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)

# Load data and configuration from the JSON file
with open(json_path, 'r', encoding='utf-8') as f:
    chart_config = json.load(f)

# Extract data, texts, and colors from the loaded JSON
chart_data = chart_config.get('chart_data', [])
texts = chart_config.get('texts', {})
colors = chart_config.get('colors', [])

# Prepare data for Plotly
categories = [item['category'] for item in chart_data]
values = [item['value'] for item in chart_data]

# Create the figure
fig = go.Figure()

# Add the bar trace
fig.add_trace(go.Bar(
    x=categories,
    y=values,
    marker_color=colors[0] if colors else None,
    text=values,
    textposition='outside',
    texttemplate='%{text}',
    cliponaxis=False # Allows text to render outside plot area if needed
))

# Configure the layout
annotations = []
if texts.get('source_left'):
    annotations.append(
        dict(
            xref='paper', yref='paper',
            x=0, y=-0.15,
            xanchor='left', yanchor='top',
            text=texts['source_left'],
            showarrow=False,
            align='left',
            font=dict(family="Arial", size=12, color="#666666")
        )
    )
if texts.get('source_right'):
    annotations.append(
        dict(
            xref='paper', yref='paper',
            x=1.0, y=-0.15,
            xanchor='right', yanchor='top',
            text=texts['source_right'],
            showarrow=False,
            align='right',
            font=dict(family="Arial", size=12, color="#666666")
        )
    )

fig.update_layout(
    title_text=texts.get('title'),
    plot_bgcolor='white',
    paper_bgcolor='white',
    font=dict(family="Arial", size=12, color='black'),
    showlegend=False,
    xaxis=dict(
        title_text=texts.get('x_axis_title'),
        showgrid=False,
        showline=True,
        linecolor='black'
    ),
    yaxis=dict(
        title_text=texts.get('y_axis_title'),
        showgrid=True,
        gridcolor='#e0e0e0',
        range=[0, 600],
        dtick=100,
        zeroline=False
    ),
    margin=dict(l=80, r=40, t=40, b=120),
    annotations=annotations
)

# Determine the output filename from the input JSON filename
base_name = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_name}.png"

# Save the figure as a PNG image
fig.write_image(output_filename, scale=2)

print(f"Chart successfully generated and saved to {output_filename}")