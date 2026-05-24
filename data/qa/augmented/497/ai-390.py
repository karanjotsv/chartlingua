import sys
import json
import os
import plotly.graph_objects as go

# Ensure a JSON file path is provided as a command-line argument
if len(sys.argv) != 2:
    print("Usage: python create_chart.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]

# Read the chart data and configuration from the specified JSON file
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_info = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_path}")
    sys.exit(1)

# Extract data, texts, and colors from the JSON structure
chart_data = chart_info.get('chart_data', [])
texts = chart_info.get('texts', {})
colors = chart_info.get('colors', ['#2672D1'])

# Prepare data for Plotly
categories = [item.get('category') for item in chart_data]
values = [item.get('value') for item in chart_data]

# Initialize the figure
fig = go.Figure()

# Add the bar trace to the figure
fig.add_trace(go.Bar(
    x=categories,
    y=values,
    text=values,
    textposition='outside',
    marker_color=colors[0],
    hoverinfo='none',
    texttemplate='%{y}',
    cliponaxis=False  # Allows text to be drawn outside the plot area
))

# Update the layout of the figure
fig.update_layout(
    font=dict(family="Arial", size=12),
    plot_bgcolor='white',
    xaxis=dict(
        title_text=texts.get('x_axis_title'),
        tickangle=-45,
        automargin=False,
        showgrid=False,
        showline=True,
        linecolor='black',
        linewidth=1
    ),
    yaxis=dict(
        title_text=texts.get('y_axis_title'),
        showgrid=True,
        gridcolor='#E0E0E0',
        range=[0, 50],
        showline=False,
        zeroline=False
    ),
    margin=dict(l=80, r=40, t=40, b=180),
    showlegend=False
)

# Add the source text as an annotation
if texts.get('source'):
    fig.add_annotation(
        text=texts['source'],
        align='right',
        showarrow=False,
        xref='paper',
        yref='paper',
        x=0.98,
        y=0,
        xanchor='right',
        yanchor='top',
        yshift=-40 # Position below the x-axis labels
    )

# Derive the output filename from the input JSON path
base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_filename}.png"

# Save the figure to a PNG file with a high resolution
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")