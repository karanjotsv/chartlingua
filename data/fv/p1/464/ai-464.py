import sys
import json
import plotly.graph_objects as go
from pathlib import Path

# Check for required command-line argument
if len(sys.argv) != 2:
    print("Usage: python create_chart.py <path_to_json_file>")
    sys.exit(1)

# Get the JSON file path from the command-line argument
json_path = Path(sys.argv[1])
if not json_path.is_file():
    print(f"Error: JSON file not found at '{json_path}'")
    sys.exit(1)

# Load data from the specified JSON file
with open(json_path, 'r', encoding='utf-8') as f:
    config = json.load(f)

# Extract data and texts from the loaded configuration
chart_data = config.get('chart_data', [])
texts = config.get('texts', {})
colors = config.get('colors', [])

# Prepare data for Plotly
labels = [item['category'] for item in chart_data]
values = [item['value'] for item in chart_data]

# Create the pie chart trace
pie_trace = go.Pie(
    labels=labels,
    values=values,
    marker_colors=colors,
    texttemplate='%{label}<br>%{value}%',
    textposition='auto',
    textfont_size=14,
    insidetextfont=dict(color='white'),
    hoverinfo='label+percent',
    sort=False,
    direction='clockwise',
    domain=dict(x=[0, 0.7]) # Reserve space on the right for the source text
)

# Initialize the figure
fig = go.Figure(data=[pie_trace])

# Update the layout for a professional and accurate appearance
fig.update_layout(
    title=dict(
        text=f"<b>{texts.get('title', '')}</b>",
        y=0.95,
        x=0.5,
        xanchor='center',
        yanchor='top',
        font_size=20
    ),
    font=dict(
        family="Arial",
        size=12,
        color="black"
    ),
    showlegend=False,
    paper_bgcolor='white',
    plot_bgcolor='white',
    margin=dict(t=100, b=50, l=50, r=50),
    # Add a border around the entire chart area
    shapes=[
        dict(
            type='rect',
            xref='paper', yref='paper',
            x0=0, y0=0, x1=1, y1=1,
            line=dict(color='black', width=1)
        )
    ],
    # Add source text as an annotation on the right side
    annotations=[
        dict(
            text=texts.get('source', '').replace('<br>', '<br>'),
            showarrow=False,
            xref="paper",
            yref="paper",
            x=0.85,
            y=0.5,
            xanchor='center',
            yanchor='middle',
            align='center',
            font=dict(size=11)
        )
    ]
)

# Generate the output PNG filename from the input JSON filename
output_filename = json_path.stem + ".png"

# Write the figure to a high-resolution PNG file
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")