import sys
import json
import plotly.graph_objects as go
from pathlib import Path

# Check for command-line argument
if len(sys.argv) != 2:
    print(f"Usage: python {Path(__file__).name} <json_file_path>")
    sys.exit(1)

# Read the JSON file from the command-line argument
json_file_path = Path(sys.argv[1])
try:
    with open(json_file_path, 'r', encoding='utf-8') as f:
        chart_info = json.load(f)
except (FileNotFoundError, json.JSONDecodeError) as e:
    print(f"Error reading or parsing JSON file: {e}")
    sys.exit(1)

# Extract data and texts from JSON
chart_data = chart_info.get('chart_data', [])
texts = chart_info.get('texts', {})
colors = chart_info.get('colors', [])

# Prepare data for Plotly
# Data is pre-ordered in JSON for Plotly's bottom-to-top rendering
y_categories = [d.get('category') for d in chart_data]
x_values = [d.get('value') for d in chart_data]

# Create the figure
fig = go.Figure()

# Add the bar trace
fig.add_trace(go.Bar(
    y=y_categories,
    x=x_values,
    orientation='h',
    marker=dict(color=colors[0] if colors else '#3178C6'),
    text=[f"{v:.1f}" for v in x_values],
    textposition='outside',
    textfont=dict(family='Arial', size=12, color='black'),
    cliponaxis=False,
    hoverinfo='none'
))

# Update layout
fig.update_layout(
    font=dict(family="Arial", size=12, color="black"),
    xaxis=dict(
        title=texts.get('x_axis_title'),
        showgrid=True,
        gridcolor='#E0E0E0',
        griddash='dot',
        zeroline=False,
        showline=True,
        linecolor='black',
        range=[0, 9],
        tickmode='linear',
        tick0=0,
        dtick=1
    ),
    yaxis=dict(
        showgrid=False,
        showline=True,
        linecolor='black'
    ),
    plot_bgcolor='white',
    paper_bgcolor='white',
    margin=dict(l=280, r=40, t=40, b=80),
    bargap=0.4,
    showlegend=False
)

# Add source annotation
source_text = texts.get('source')
if source_text:
    fig.add_annotation(
        text=source_text,
        xref="paper", yref="paper",
        x=0.98, y=-0.15,
        showarrow=False,
        xanchor='right',
        yanchor='top',
        align='right',
        font=dict(family="Arial", size=12, color="#808080")
    )

# Define output filename and save the image
output_image_path = json_file_path.with_suffix(".png")
fig.write_image(str(output_image_path), scale=2)

print(f"Chart saved to {output_image_path}")