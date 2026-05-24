import sys
import json
import plotly.graph_objects as go
import pathlib

# Check for command-line argument
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <json_file_path>")
    sys.exit(1)

# Get JSON file path from command-line argument
json_file_path = sys.argv[1]

# Read data from the specified JSON file
try:
    with open(json_file_path, 'r', encoding='utf-8') as f:
        chart_config = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at '{json_file_path}'")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from '{json_file_path}'")
    sys.exit(1)

# Extract data and texts from the JSON object
chart_data = chart_config.get('chart_data', [])
texts = chart_config.get('texts', {})
colors = chart_config.get('colors', [])

# Prepare data for Plotly
# The order is reversed to match the visual top-to-bottom order of the original chart
categories = [d['category'] for d in reversed(chart_data)]
values = [d['value'] for d in reversed(chart_data)]

# Format text labels with a space for thousands separator
formatted_texts = [f"{v:,}".replace(",", " ") if v != 0 else "0" for v in values]

# Create the figure
fig = go.Figure()

# Add the bar trace
fig.add_trace(go.Bar(
    y=categories,
    x=values,
    orientation='h',
    marker_color=colors[0] if colors else '#1f77b4',
    text=formatted_texts,
    textposition='outside',
    cliponaxis=False,  # Prevents text from being clipped at the chart edge
    textfont=dict(
        family="Arial",
        size=12,
        color='black'
    )
))

# Update layout for a clean and accurate look
fig.update_layout(
    template="plotly_white",
    font=dict(family="Arial", size=12, color="black"),
    margin=dict(l=80, r=40, t=30, b=80),
    showlegend=False,
    xaxis=dict(
        title=texts.get('x_axis_title'),
        showgrid=True,
        gridcolor='#EAEAEA',
        griddash='dot',
        zeroline=False,
        showline=False,
        range=[0, max(values) * 1.18],  # Add padding for outside text
        dtick=2500
    ),
    yaxis=dict(
        showgrid=False,
        zeroline=False
    ),
    separators='.,' # Use a dot for decimal and a comma for thousands (default) for engine, formatting is done on text
)

# Manually format x-axis tick labels to use spaces
fig.update_xaxes(tickformat=" ,.0f", tickfont=dict(size=12))

# Add source annotation
if texts.get('source'):
    fig.add_annotation(
        text=texts['source'],
        xref="paper", yref="paper",
        x=1.0, y=-0.15,
        xanchor='right', yanchor='top',
        showarrow=False,
        font=dict(size=12, color="#7f7f7f")
    )

# Define output filename based on the input JSON filename
base_filename = pathlib.Path(json_file_path).stem
output_filename = f"{base_filename}.png"

# Write the image file
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")