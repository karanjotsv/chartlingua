import sys
import json
from pathlib import Path
import plotly.graph_objects as go

# Check for command-line argument
if len(sys.argv) != 2:
    print("Usage: python create_chart.py <json_file_path>")
    sys.exit(1)

# Get JSON file path from command-line argument
json_file_path = Path(sys.argv[1])
if not json_file_path.is_file():
    print(f"Error: File not found at {json_file_path}")
    sys.exit(1)

# Read data from the JSON file
with open(json_file_path, 'r', encoding='utf-8') as f:
    chart_data = json.load(f)

# Extract data and texts from the JSON structure
data = chart_data['chart_data']
texts = chart_data['texts']
colors = chart_data['colors']

# Prepare data for Plotly
categories = [item['category'] for item in data]
values = [item['value'] for item in data]

# Create the figure
fig = go.Figure()

# Add the bar trace
fig.add_trace(go.Bar(
    x=categories,
    y=values,
    marker_color=colors[0],
    text=[f'{v:.2f}%' for v in values],
    textposition='outside',
    hoverinfo='none'
))

# Update layout
fig.update_layout(
    font_family="Arial",
    plot_bgcolor='white',
    paper_bgcolor='white',
    showlegend=False,
    title={
        'text': f"{texts.get('title', '')}<br><sup>{texts.get('subtitle', '')}</sup>" if texts.get('title') else None,
        'x': 0.05,
        'xanchor': 'left'
    },
    xaxis=dict(
        title_text=texts.get('x_axis_title'),
        showgrid=False,
        showline=True,
        linecolor='lightgrey',
        tickfont=dict(size=12)
    ),
    yaxis=dict(
        title_text=texts.get('y_axis_title'),
        range=[0, 100],
        dtick=20,
        ticksuffix='%',
        gridcolor='#EAEAEA',
        tickfont=dict(size=12)
    ),
    margin=dict(l=80, r=40, t=80, b=120),
    annotations=[
        dict(
            text=texts['source_note'].get('left', ''),
            showarrow=False,
            xref='paper',
            yref='paper',
            x=0,
            y=-0.15,
            xanchor='left',
            yanchor='top',
            align='left',
            font=dict(size=12, color="#666666")
        ),
        dict(
            text=texts['source_note'].get('right', ''),
            showarrow=False,
            xref='paper',
            yref='paper',
            x=1,
            y=-0.15,
            xanchor='right',
            yanchor='top',
            align='right',
            font=dict(size=12, color="#666666")
        )
    ]
)

# Set position for the text above bars
fig.update_traces(
    textfont_size=12,
    textangle=0,
    cliponaxis=False
)

# Generate the output PNG filename from the JSON filename
output_filename = json_file_path.with_suffix('.png')

# Save the figure as a PNG image
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")