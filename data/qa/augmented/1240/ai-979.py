import sys
import json
import os
import plotly.graph_objects as go

# Ensure a JSON file path is provided as a command-line argument
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <json_file_path>")
    sys.exit(1)

json_path = sys.argv[1]

# Read data from the specified JSON file
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        config = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at '{json_path}'")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from '{json_path}'")
    sys.exit(1)

# Extract data, texts, and colors from the JSON structure
chart_data = config.get('chart_data', [])
texts = config.get('texts', {})
colors = config.get('colors', {})

# Prepare data for Plotly
categories = [item['category'] for item in chart_data]
values = [item['value'] for item in chart_data]

# Create the figure object
fig = go.Figure()

# Add the bar trace to the figure
fig.add_trace(go.Bar(
    x=categories,
    y=values,
    marker_color=colors.get('bar_color', '#1f77b4'),
    text=values,
    texttemplate='%{text}',
    textposition='outside',
    cliponaxis=False  # Prevents data labels from being clipped at the top
))

# Configure the layout of the chart
annotations = []
if texts.get('source'):
    annotations.append(
        go.layout.Annotation(
            text=texts['source'],
            align='right',
            showarrow=False,
            xref='paper',
            yref='paper',
            x=1,
            y=-0.2,
            xanchor='right',
            yanchor='top'
        )
    )

fig.update_layout(
    font=dict(family="Arial", size=14),
    plot_bgcolor='white',
    paper_bgcolor='white',
    showlegend=False,
    xaxis=dict(
        title_text=texts.get('x_axis_title'),
        showline=True,
        linewidth=1,
        linecolor='black'
    ),
    yaxis=dict(
        title_text=texts.get('y_axis_title'),
        range=[0, 8],
        showgrid=True,
        gridcolor='#e0e0e0',
        zeroline=False,
        showline=False
    ),
    margin=dict(l=100, r=40, t=50, b=80),
    annotations=annotations
)

# Determine output filename from the input JSON filename
base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_filename}.png"

# Write the chart to a high-resolution PNG file
fig.write_image(output_filename, scale=2)

print(f"Chart successfully generated and saved to {output_filename}")