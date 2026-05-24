import sys
import json
from pathlib import Path
import plotly.graph_objects as go

# Read chart configuration from JSON file specified in command-line argument
json_file_path = Path(sys.argv[1])
with open(json_file_path, 'r', encoding='utf-8') as f:
    chart_details = json.load(f)

# Initialize figure
fig = go.Figure()

# Add data traces from JSON
for i, series in enumerate(chart_details['chart_data']):
    fig.add_trace(go.Scatter(
        x=series.get('x'),
        y=series.get('y'),
        mode='lines',
        name=series.get('name', ''),
        line=dict(color=chart_details['colors'][i], width=2)
    ))

# Prepare annotations from JSON
annotations = []
if 'annotations' in chart_details['texts'] and chart_details['texts']['annotations']:
    for ann in chart_details['texts']['annotations']:
        # This allows flexible styling directly from JSON
        annotations.append(go.layout.Annotation(**ann))

# Update layout
fig.update_layout(
    title=dict(
        text=chart_details['texts'].get('title', ''),
        x=0.01,
        y=0.98,
        xanchor='left',
        yanchor='top',
        font=dict(size=14)
    ),
    font=dict(family="Arial", size=12, color="black"),
    xaxis=dict(
        type='log',
        title_text=chart_details['texts'].get('x_axis_title'),
        showline=True,
        linewidth=1,
        linecolor='black',
        mirror=True,
        showgrid=True,
        gridwidth=1,
        gridcolor='darkgrey',
        ticks='outside',
        range=[1, 4.7]  # Corresponds to 10 to ~50,000
    ),
    yaxis=dict(
        type='log',
        title_text=chart_details['texts'].get('y_axis_title'),
        showline=True,
        linewidth=1,
        linecolor='black',
        mirror=True,
        showgrid=True,
        gridwidth=1,
        gridcolor='darkgrey',
        ticks='outside',
        range=[-3.301, -1.301]  # Corresponds to 0.0005 to 0.05
    ),
    plot_bgcolor='white',
    paper_bgcolor='white',
    showlegend=False,
    margin=dict(l=60, r=40, t=50, b=50),
    annotations=annotations
)

# Derive output filename and save image
output_path = json_file_path.with_suffix('.png')
fig.write_image(output_path, scale=2)
print(f"Chart saved to {output_path}")