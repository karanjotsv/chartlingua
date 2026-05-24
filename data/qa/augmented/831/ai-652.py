import sys
import json
import os
import plotly.graph_objects as go

# Ensure a JSON file path is provided as a command-line argument
if len(sys.argv) != 2:
    print("Usage: python recreate_chart.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]

# Read and parse the JSON file
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_info = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_path}")
    sys.exit(1)

# Extract data and text from the JSON structure
chart_data = chart_info['chart_data']
texts = chart_info['texts']
colors = chart_info['colors']

# Prepare data for plotting by extracting categories and values
categories = [item['category'] for item in chart_data]
values = [item['value'] for item in chart_data]

# Initialize the figure
fig = go.Figure()

# Add the bar trace to the figure
fig.add_trace(go.Bar(
    x=categories,
    y=values,
    marker_color=colors[0],
    text=[f"{v}%" for v in values],
    textposition='outside',
    cliponaxis=False,
    textfont=dict(
        family="Arial",
        size=12,
        color='black'
    )
))

# Configure the layout of the chart
fig.update_layout(
    font=dict(family="Arial", size=12, color="black"),
    yaxis_title_text=texts['y_axis_title'],
    showlegend=False,
    plot_bgcolor='white',
    paper_bgcolor='white',
    margin=dict(l=80, r=40, t=40, b=120),
    yaxis=dict(
        range=[0, 50],
        tickvals=[0, 10, 20, 30, 40, 50],
        ticksuffix='%',
        showgrid=True,
        gridcolor='#E5E5E5',
        zeroline=False,
        title_standoff=15
    ),
    xaxis=dict(
        tickangle=-45,
        showgrid=False,
        showline=True,
        linewidth=1,
        linecolor='#B0B0B0'
    )
)

# Add the source text as an annotation at the bottom right
if texts.get('source'):
    fig.add_annotation(
        text=texts['source'],
        align='right',
        showarrow=False,
        xref='paper',
        yref='paper',
        x=1,
        y=-0.25,
        xanchor='right',
        yanchor='top',
        font=dict(size=12, color='#666666')
    )

# Determine the output filename from the input JSON path
base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_filename}.png"

# Save the chart as a PNG image
fig.write_image(output_filename, scale=2)

print(f"Chart saved successfully to {output_filename}")