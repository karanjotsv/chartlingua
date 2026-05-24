import sys
import json
from pathlib import Path
import plotly.graph_objects as go

# Ensure a JSON file path is provided as a command-line argument
if len(sys.argv) != 2:
    print(f"Usage: python {sys.argv[0]} <path_to_json_file>")
    sys.exit(1)

# Read the JSON data file
json_path = Path(sys.argv[1])
if not json_path.is_file():
    print(f"Error: File not found at {json_path}")
    sys.exit(1)

with open(json_path, 'r', encoding='utf-8') as f:
    config = json.load(f)

# Extract data and texts from the loaded JSON
chart_data = config['chart_data']
texts = config['texts']
colors = config['colors']

values = [d['value'] for d in chart_data]
hover_labels = [d['hover_label'] for d in chart_data]
display_labels = [d['display_label'] for d in chart_data]
text_colors = [d['text_color'] for d in chart_data]

# Create the figure
fig = go.Figure()

# Add the pie chart trace
fig.add_trace(go.Pie(
    values=values,
    labels=hover_labels,
    text=display_labels,
    textinfo='text',
    textfont=dict(
        family="Arial",
        size=14,
        color=text_colors
    ),
    marker=dict(
        colors=colors,
        line=dict(color='#FFFFFF', width=2)
    ),
    hole=0,
    sort=False,
    direction='clockwise',
    rotation=135  # Rotates the start of the first slice to match the image
))

# Configure the layout
fig.update_layout(
    title=dict(
        text=f"{texts['title']}<br><br>{texts['subtitle']}",
        font=dict(family="Arial", size=18, color='black'),
        x=0.05,
        y=0.98,
        xanchor='left',
        yanchor='top'
    ),
    showlegend=False,
    paper_bgcolor='white',
    plot_bgcolor='white',
    width=500,
    height=700,
    margin=dict(l=20, r=20, t=200, b=120)
)

# Add source and note annotation
fig.add_annotation(
    text=texts['source'],
    align='left',
    showarrow=False,
    xref='paper',
    yref='paper',
    x=0.01,
    y=0.1,
    xanchor='left',
    yanchor='top',
    font=dict(family="Arial", size=12, color='black')
)

# Add annotation for "Don't know" with an arrow
fig.add_annotation(
    text=texts['annotation_label'],
    align='center',
    showarrow=True,
    arrowhead=1,
    arrowcolor='#000000',
    arrowsize=1,
    arrowwidth=1.5,
    xref='paper',
    yref='paper',
    x=0.82,  # x position of the text
    y=0.18,  # y position of the text
    ax=-50,   # x component of the arrow's vector
    ay=50,    # y component of the arrow's vector
    font=dict(family="Arial", size=14, color='black')
)

# Generate the output image file path from the input JSON file path
output_filename = json_path.with_suffix('.png').name
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")