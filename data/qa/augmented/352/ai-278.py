import sys
import json
import plotly.graph_objects as go
from pathlib import Path

# Check if a command-line argument is provided
if len(sys.argv) != 2:
    print("Usage: python create_chart.py <path_to_json_file>")
    sys.exit(1)

# Get the JSON file path from the command-line argument
json_path = Path(sys.argv[1])

# Check if the JSON file exists
if not json_path.is_file():
    print(f"Error: JSON file not found at '{json_path}'")
    sys.exit(1)

# Define the output image path based on the input JSON filename
output_path = json_path.with_suffix(".png")

# Load data from the JSON file
with open(json_path, 'r', encoding='utf-8') as f:
    chart_data = json.load(f)

# Extract data and texts from the loaded JSON
data_series = chart_data['chart_data']
texts = chart_data['texts']
colors = chart_data['colors']
value_suffix = texts.get('value_suffix', '')

# Prepare data for Plotly
categories = [item['category'] for item in data_series]
values = [item['value'] for item in data_series]
text_labels = [f"{v}{value_suffix}" for v in values]

# Initialize the figure
fig = go.Figure()

# Add the bar trace
fig.add_trace(go.Bar(
    x=categories,
    y=values,
    text=text_labels,
    textposition='outside',
    marker_color=colors[0],
    cliponaxis=False,
    textfont=dict(family="Arial", size=14, color='black')
))

# Update layout for a professional appearance
fig.update_layout(
    font=dict(family="Arial"),
    plot_bgcolor='white',
    xaxis=dict(
        title_text=texts['x_axis_title'],
        showgrid=False,
        showline=True,
        linecolor='black',
        linewidth=1,
        tickfont=dict(size=12)
    ),
    yaxis=dict(
        title_text=texts['y_axis_title'],
        range=[0, 70],
        showgrid=True,
        gridcolor='#e0e0e0',
        tickformat="~s",
        ticksuffix='%',
        tickfont=dict(size=12)
    ),
    margin=dict(l=80, r=40, t=50, b=100),
    showlegend=False
)

# Add source annotation
if texts.get('source'):
    fig.add_annotation(
        text=texts['source'],
        align='right',
        showarrow=False,
        xref='paper',
        yref='paper',
        x=1.0,
        y=-0.2,
        xanchor='right',
        yanchor='bottom',
        font=dict(family="Arial", size=12, color='#666666')
    )

# Save the figure to a PNG file
fig.write_image(output_path, scale=2)

print(f"Chart saved to {output_path}")