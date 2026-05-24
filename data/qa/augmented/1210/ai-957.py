import sys
import json
from pathlib import Path
import plotly.graph_objects as go

# Check for command-line argument
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <json_file_path>")
    sys.exit(1)

# Get JSON file path from command-line argument
json_file_path = Path(sys.argv[1])

# Verify the file exists
if not json_file_path.is_file():
    print(f"Error: File not found at {json_file_path}")
    sys.exit(1)

# Read data from the JSON file
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
    texttemplate='%{text}',
    marker_color=colors[0],
    cliponaxis=False # Allows text to render outside plot area
))

# Update layout
fig.update_layout(
    font_family="Arial",
    plot_bgcolor='white',
    paper_bgcolor='white',
    showlegend=False,
    title={
        'text': texts.get('title'),
        'x': 0.05,
        'xanchor': 'left'
    },
    yaxis={
        'title': texts.get('y_axis_title'),
        'range': [0, 50],
        'gridcolor': '#e0e0e0',
        'showline': True,
        'linewidth': 1,
        'linecolor': 'lightgray'
    },
    xaxis={
        'title': texts.get('x_axis_title'),
        'showline': True,
        'linewidth': 1,
        'linecolor': 'lightgray'
    },
    margin=dict(l=80, r=40, t=50, b=120),
    annotations=[
        dict(
            text=texts.get('source'),
            showarrow=False,
            xref='paper',
            yref='paper',
            x=0.98,
            y=-0.15,
            xanchor='right',
            yanchor='top',
            font=dict(size=12, color='#666')
        ),
        dict(
            text=texts.get('note'),
            showarrow=False,
            xref='paper',
            yref='paper',
            x=0.98,
            y=-0.22,
            xanchor='right',
            yanchor='top',
            font=dict(size=12, color='#2a7ae2')
        )
    ]
)

# Update text font for the bar labels
fig.update_traces(textfont_size=12, textfont_color='black')


# Define output filename and save the image
output_filename = json_file_path.with_suffix('.png')
fig.write_image(output_filename, scale=2)

print(f"Chart saved as {output_filename}")