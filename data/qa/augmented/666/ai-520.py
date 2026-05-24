import sys
import json
import pathlib
import plotly.graph_objects as go

# Check for command-line argument
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <json_file_path>")
    sys.exit(1)

# Get JSON file path from command-line argument
json_path = pathlib.Path(sys.argv[1])

# Check if the JSON file exists
if not json_path.is_file():
    print(f"Error: JSON file not found at '{json_path}'")
    sys.exit(1)

# Load data from JSON file
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_info = json.load(f)
except json.JSONDecodeError:
    print(f"Error: Invalid JSON format in '{json_path}'")
    sys.exit(1)

# Extract data for plotting
chart_data = chart_info.get('chart_data', [])
texts = chart_info.get('texts', {})
colors = chart_info.get('colors', [])

# Prepare data series from the JSON structure
categories = [d['category'] for d in chart_data]
values = [d['value'] for d in chart_data]

# Create the figure
fig = go.Figure()

# Add the bar trace
fig.add_trace(go.Bar(
    y=categories,
    x=values,
    orientation='h',
    marker=dict(color=colors[0]),
    text=values,
    texttemplate='%{x:.1f}',
    textposition='outside',
    textfont=dict(family="Arial", size=12)
))

# Update layout
fig.update_layout(
    font=dict(family="Arial", size=12, color="black"),
    title_text=texts.get('title'),
    xaxis_title=texts.get('x_axis_title'),
    yaxis_title=texts.get('y_axis_title'),
    plot_bgcolor='white',
    paper_bgcolor='white',
    margin=dict(l=100, r=60, t=30, b=80),
    xaxis=dict(
        showgrid=True,
        gridcolor='#EAEAEA',
        gridwidth=1,
        griddash='dot',
        zeroline=False,
        showline=False,
        tickmode='linear',
        tick0=0,
        dtick=5,
        range=[0, 52] # Extend range to avoid clipping text labels
    ),
    yaxis=dict(
        autorange="reversed", # Ensures top-to-bottom order from JSON
        showgrid=False,
        showline=False,
        ticks='outside',
        ticklen=5,
        tickcolor='lightgrey'
    ),
    showlegend=False,
    annotations=[
        dict(
            text=texts.get('source'),
            showarrow=False,
            xref="paper", yref="paper",
            x=0.99, y=-0.15,
            xanchor='right', yanchor='top',
            align='right',
            font=dict(family="Arial", size=10, color="grey")
        )
    ]
)

# Derive output filename from the input JSON filename
output_filename = json_path.stem + ".png"

# Save the figure as a PNG image
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")