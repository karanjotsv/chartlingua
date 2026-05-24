import sys
import json
import pathlib
import plotly.graph_objects as go

# Ensure a command-line argument is provided for the JSON file path.
if len(sys.argv) != 2:
    print(f"Usage: python {sys.argv[0]} <path_to_json_file>")
    sys.exit(1)

json_path_str = sys.argv[1]
json_path = pathlib.Path(json_path_str)

# Ensure the JSON file exists.
if not json_path.is_file():
    print(f"Error: File not found at {json_path}")
    sys.exit(1)

# Generate the output PNG filename from the JSON filename.
output_path = json_path.with_suffix('.png')

# Load and parse the JSON data.
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_info = json.load(f)
except json.JSONDecodeError:
    print(f"Error: Invalid JSON in {json_path}")
    sys.exit(1)

# Extract data, texts, and colors from the JSON structure.
chart_data = chart_info['chart_data']
texts = chart_info['texts']
colors = chart_info['colors']

# Prepare data for the Plotly trace.
categories = [item['category'] for item in chart_data]
values = [item['value'] for item in chart_data]

# Create the figure object.
fig = go.Figure()

# Add the bar trace.
fig.add_trace(go.Bar(
    x=categories,
    y=values,
    marker_color=colors[0],
    texttemplate='%{y}%',
    textposition='outside',
    textfont=dict(color='black', size=12, family="Arial"),
    cliponaxis=False
))

# Configure the chart layout.
fig.update_layout(
    font=dict(family="Arial", size=12, color="black"),
    plot_bgcolor='white',
    paper_bgcolor='white',
    yaxis=dict(
        title=texts.get('yaxis_title'),
        range=[0, 70],
        tick0=0,
        dtick=10,
        ticksuffix='%',
        showgrid=True,
        gridcolor='#E5E5E5',
        griddash='dash',
        gridwidth=1,
        zeroline=False
    ),
    xaxis=dict(
        title=texts.get('xaxis_title'),
        showline=True,
        linewidth=1,
        linecolor='black',
        tickfont=dict(size=12)
    ),
    showlegend=False,
    margin=dict(l=70, r=20, t=30, b=100)
)

# Add source annotation if present in the JSON.
source_text = texts.get('source')
if source_text:
    fig.add_annotation(
        text=source_text,
        xref="paper",
        yref="paper",
        x=0.99,
        y=-0.2,
        showarrow=False,
        xanchor='right',
        yanchor='top',
        font=dict(size=10, color="#666666")
    )

# Write the output image.
fig.write_image(output_path, scale=2)

print(f"Chart saved to {output_path}")