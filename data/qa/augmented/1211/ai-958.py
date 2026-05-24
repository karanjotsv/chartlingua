import sys
import json
import plotly.graph_objects as go
from pathlib import Path

# Check if the path to the JSON file is provided as a command-line argument
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <path_to_json_file>")
    sys.exit(1)

# Get the JSON file path from the command-line argument
json_file_path = Path(sys.argv[1])

# Read the JSON data from the file
with open(json_file_path, 'r', encoding='utf-8') as f:
    chart_info = json.load(f)

# Extract data, texts, and colors from the JSON object
chart_data = chart_info['chart_data']
texts = chart_info['texts']
colors = chart_info['colors']

# Prepare data for Plotly. The data is provided top-to-bottom,
# so we need to reverse it for Plotly's bottom-to-top y-axis.
categories = [item['category'] for item in chart_data]
values = [item['value'] for item in chart_data]
categories.reverse()
values.reverse()

# Create the figure
fig = go.Figure()

# Add the horizontal bar trace
fig.add_trace(go.Bar(
    y=categories,
    x=values,
    orientation='h',
    marker_color=colors[0],
    text=[f'{v}%' for v in values],
    textposition='outside',
    cliponaxis=False  # Allows text to be drawn outside the plot area
))

# Update layout for a clean and accurate representation
fig.update_layout(
    font_family="Arial",
    plot_bgcolor='white',
    xaxis=dict(
        title=texts.get('xaxis_title'),
        showgrid=True,
        gridcolor='#E5E5E5',
        gridwidth=1,
        zeroline=False,
        ticksuffix='%',
        range=[0, 22.5] # Set range to match original and prevent text clipping
    ),
    yaxis=dict(
        title=texts.get('yaxis_title'),
        showgrid=False,
        zeroline=False
    ),
    margin=dict(l=120, r=40, t=50, b=80),
    showlegend=False
)

# Add source annotation
if texts.get('source'):
    fig.add_annotation(
        text=texts['source'],
        align='left',
        showarrow=False,
        xref='paper',
        yref='paper',
        x=0,
        y=-0.15,
        xanchor='left',
        yanchor='top',
        font=dict(size=12, color="#808080")
    )

# Define output filename based on the input JSON filename
output_filename = json_file_path.with_suffix('.png')

# Write the image file
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")