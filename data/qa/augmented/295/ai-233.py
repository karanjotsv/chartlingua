import sys
import json
import plotly.graph_objects as go
from pathlib import Path

# Check for command-line argument
if len(sys.argv) != 2:
    print("Usage: python script.py <path_to_json_file>")
    sys.exit(1)

# Get the JSON file path from the command-line argument
json_file_path = Path(sys.argv[1])

# Check if the JSON file exists
if not json_file_path.is_file():
    print(f"Error: File not found at {json_file_path}")
    sys.exit(1)

# Read the JSON data
with open(json_file_path, 'r', encoding='utf-8') as f:
    chart_data = json.load(f)

# Extract data for plotting
data = chart_data['chart_data']
texts = chart_data['texts']
colors = chart_data['colors']

categories = [item['category'] for item in data]
values = [item['value'] for item in data]

# Create the figure
fig = go.Figure()

# Add the bar trace
fig.add_trace(go.Bar(
    x=categories,
    y=values,
    text=values,
    textposition='outside',
    marker_color=colors[0],
    cliponaxis=False,
    textfont=dict(family='Arial', size=12, color='black')
))

# Update layout
fig.update_layout(
    font=dict(family="Arial", size=12, color="#000000"),
    title_text=texts.get('title'),
    yaxis_title=texts.get('y_axis_title'),
    xaxis_title=texts.get('x_axis_title'),
    plot_bgcolor='white',
    paper_bgcolor='white',
    showlegend=False,
    margin=dict(l=80, r=40, t=50, b=100),
    xaxis=dict(
        showgrid=False,
        showline=True,
        linewidth=1,
        linecolor='black',
        tickfont=dict(family="Arial", size=12)
    ),
    yaxis=dict(
        range=[0, 41],
        gridcolor='#dddddd',
        zeroline=False,
        title_standoff=10,
        tickfont=dict(family="Arial", size=12)
    )
)

# Add source annotation
annotations = []
if texts.get('source'):
    annotations.append(
        dict(
            xref='paper',
            yref='paper',
            x=1,
            y=-0.22,
            xanchor='right',
            yanchor='top',
            text=texts['source'],
            showarrow=False,
            font=dict(family='Arial', size=12, color='grey')
        )
    )

fig.update_layout(annotations=annotations)

# Define output image path from the input JSON path
output_image_path = json_file_path.with_suffix(".png")

# Save the figure as a PNG image
fig.write_image(str(output_image_path), scale=2)

print(f"Chart saved to {output_image_path}")