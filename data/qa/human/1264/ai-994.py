import sys
import json
from pathlib import Path
import plotly.graph_objects as go

# Check for command-line argument
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <json_file_path>")
    sys.exit(1)

# Get file path from argument
json_file_path = Path(sys.argv[1])
if not json_file_path.is_file():
    print(f"Error: File not found at {json_file_path}")
    sys.exit(1)

# Load data from JSON file
with open(json_file_path, 'r', encoding='utf-8') as f:
    chart_data = json.load(f)

# --- Chart Creation ---

# Extract data for the pie chart
pie_values = [item['value'] for item in chart_data['chart_data']]
pie_colors = chart_data['colors']
pie_rotation = chart_data.get('chart_style', {}).get('pie_rotation', 0)

# Create the pie chart trace
pie_trace = go.Pie(
    values=pie_values,
    marker=dict(
        colors=pie_colors,
        line=dict(color='white', width=1)
    ),
    hole=0,
    sort=False,
    direction='clockwise',
    rotation=pie_rotation,
    textinfo='none',
    hoverinfo='none'
)

# --- Annotations and Layout ---

# Create annotations for each pie slice
annotations = []
for item in chart_data['chart_data']:
    pos = item['anno_pos']
    annotations.append(
        go.layout.Annotation(
            text=item['label_text'],
            x=pos['x'],
            y=pos['y'],
            xref='paper',
            yref='paper',
            showarrow=True,
            arrowhead=0,
            arrowcolor="#000000",
            arrowwidth=1,
            ax=pos['ax'],
            ay=pos['ay'],
            font=dict(family="Arial", size=12, color="black"),
            align='left',
            xanchor=pos['xanchor'],
            yanchor='middle'
        )
    )

# Add source annotation
source_text = chart_data['texts']['source']
annotations.append(
    go.layout.Annotation(
        text=source_text,
        x=0,
        y=-0.1,
        xref='paper',
        yref='paper',
        showarrow=False,
        xanchor='left',
        yanchor='bottom',
        font=dict(family="Arial", size=12, color="black")
    )
)

# Create the layout
layout = go.Layout(
    title=dict(
        text=chart_data['texts']['title'],
        x=0.01,
        y=0.98,
        xanchor='left',
        yanchor='top',
        font=dict(family="Arial", size=18, color="#666666")
    ),
    showlegend=False,
    paper_bgcolor='white',
    plot_bgcolor='white',
    annotations=annotations,
    margin=dict(l=20, r=20, t=80, b=80),
    xaxis=dict(showgrid=False, zeroline=False, showticklabels=False, visible=False),
    yaxis=dict(showgrid=False, zeroline=False, showticklabels=False, visible=False)
)

# --- Figure Generation ---

# Create the figure object
fig = go.Figure(data=[pie_trace], layout=layout)

# Generate output filename from input JSON path
output_filename = json_file_path.with_suffix(".png")

# Save the figure as a PNG image
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")