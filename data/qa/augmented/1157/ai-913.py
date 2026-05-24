import sys
import json
import plotly.graph_objects as go
import os

# Check if the JSON file path is provided as a command-line argument
if len(sys.argv) != 2:
    print("Usage: python create_chart.py <json_file_path>")
    sys.exit(1)

json_filepath = sys.argv[1]

# Check if the file exists
if not os.path.exists(json_filepath):
    print(f"Error: File not found at {json_filepath}")
    sys.exit(1)

# Load data from the specified JSON file
try:
    with open(json_filepath, 'r', encoding='utf-8') as f:
        chart_config = json.load(f)
except json.JSONDecodeError:
    print(f"Error: Invalid JSON format in {json_filepath}")
    sys.exit(1)

# Extract data and text from the JSON structure
chart_data = chart_config.get('chart_data', [])
texts = chart_config.get('texts', {})
colors = chart_config.get('colors', [])

# Prepare data for Plotly
categories = [item['category'] for item in chart_data]
values = [item['value'] for item in chart_data]

# Create the bar chart trace
fig = go.Figure()

fig.add_trace(go.Bar(
    x=categories,
    y=values,
    marker_color=colors[0] if colors else None,
    text=[f"{v}%" for v in values],
    textposition='outside',
    cliponaxis=False
))

# Configure the layout
fig.update_layout(
    title_text=texts.get('title'),
    yaxis_title_text=texts.get('y_axis_title'),
    xaxis_title_text=texts.get('x_axis_title'),
    font=dict(
        family="Arial",
        size=12,
        color="black"
    ),
    plot_bgcolor='white',
    showlegend=False,
    margin=dict(l=80, r=40, t=50, b=100),
    yaxis=dict(
        range=[0, 2.6],
        dtick=0.5,
        ticksuffix='%',
        showgrid=True,
        gridcolor='#dddddd',
        zeroline=False,
        linecolor='black', 
        linewidth=1
    ),
    xaxis=dict(
        type='category',
        showgrid=True,
        gridcolor='#f0f0f0',
        linecolor='black', 
        linewidth=1
    )
)

# Add source text as an annotation
if texts.get('source'):
    fig.add_annotation(
        text=texts['source'],
        align='left',
        showarrow=False,
        xref='paper',
        yref='paper',
        x=1.0,
        y=-0.15,
        xanchor='right',
        yanchor='top',
        font=dict(size=10)
    )

# Update trace text font
fig.update_traces(textfont_size=12)

# Define output filename based on the input JSON file path
base_filename = os.path.splitext(os.path.basename(json_filepath))[0]
output_filename = f"{base_filename}.png"

# Save the figure as a PNG image
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")