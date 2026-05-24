import sys
import json
import plotly.graph_objects as go
from pathlib import Path

# Check if the JSON file path is provided as a command-line argument
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <path_to_json_file>")
    sys.exit(1)

json_file_path = Path(sys.argv[1])
if not json_file_path.is_file():
    print(f"Error: File not found at {json_file_path}")
    sys.exit(1)

# Load data from the JSON file
with open(json_file_path, 'r', encoding='utf-8') as f:
    chart_config = json.load(f)

# Extract data for plotting
chart_data = chart_config['chart_data']
texts = chart_config['texts']
colors = chart_config['colors']

# Prepare data for the bar trace
categories = [item['category'] for item in chart_data]
values = [item['value'] for item in chart_data]

# Create the figure
fig = go.Figure()

# Add the bar trace
fig.add_trace(go.Bar(
    x=categories,
    y=values,
    marker_color=colors,
    textposition='none', # Annotations will be added manually
    hoverinfo='none'
))

# Add annotations above each bar
for item in chart_data:
    fig.add_annotation(
        x=item['category'],
        y=item['value'],
        text=item['annotation_text'],
        showarrow=False,
        font=dict(
            family="Arial",
            size=11,
            color="black"
        ),
        bgcolor="rgba(230, 230, 230, 0.7)",
        borderpad=2,
        yshift=15,
        yanchor="middle"
    )

# Update layout
fig.update_layout(
    title=dict(
        text=texts['title'],
        x=0.5,
        xanchor='center',
        y=0.95,
        yanchor='top',
        font=dict(family="Arial", size=16, color="black", weight="bold")
    ),
    xaxis=dict(
        title_text=texts['x_axis_title'],
        showline=True,
        linewidth=1,
        linecolor='black',
        tickfont=dict(family="Arial", size=10)
    ),
    yaxis=dict(
        title_text=texts['y_axis_title'],
        range=[0, 10],
        tickvals=[0, 2, 4, 6, 8, 10],
        showgrid=True,
        gridcolor='#BDBDBD',
        gridwidth=1,
        showline=True,
        linewidth=1,
        linecolor='black',
        tickfont=dict(family="Arial", size=12)
    ),
    font=dict(
        family="Arial",
        size=12
    ),
    plot_bgcolor='white',
    paper_bgcolor='white',
    showlegend=False,
    margin=dict(l=50, r=50, t=100, b=120)
)

# Generate output filename from JSON path
output_filename = json_file_path.with_suffix('.png')

# Save the figure as a PNG image
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")