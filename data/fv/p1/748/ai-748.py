import sys
import json
import plotly.graph_objects as go
from pathlib import Path

# Check for command-line argument
if len(sys.argv) != 2:
    print(f"Usage: python {sys.argv[0]} <json_file_path>")
    sys.exit(1)

json_path = Path(sys.argv[1])
if not json_path.is_file():
    print(f"Error: JSON file not found at '{json_path}'")
    sys.exit(1)

# Load data from the specified JSON file
with open(json_path, 'r', encoding='utf-8') as f:
    chart_json = json.load(f)

# Extract data for plotting
chart_data = chart_json['chart_data']
texts = chart_json['texts']
colors = chart_json['colors']
annotations_data = chart_json.get('annotations', [])
categories = chart_data['categories']

# Create the figure
fig = go.Figure()

# Add bar traces for each series
for i, series in enumerate(chart_data['series']):
    fig.add_trace(go.Bar(
        x=categories,
        y=series['data'],
        name=series['name'],
        marker_color=colors[i]
    ))

# Update layout
fig.update_layout(
    font_family="Arial",
    title=dict(
        text=texts['title'],
        x=0.01,
        y=0.95,
        xanchor='left',
        yanchor='top',
        font=dict(size=24)
    ),
    xaxis=dict(
        tickmode='array',
        tickvals=categories,
        ticktext=[cat if (int(cat) % 1 == 0) else '' for cat in categories],
        showgrid=True,
        gridcolor='#FFFFFF',
        zeroline=False,
        domain=[0.05, 1] # Add some padding on the left for the y-axis label
    ),
    yaxis=dict(
        range=[0, 150],
        tickvals=[0, 37.5, 75, 112.5, 150],
        gridcolor='#CCCCCC',
        zeroline=False
    ),
    plot_bgcolor='#E1E7F2',
    barmode='group',
    bargap=0.3,
    bargroupgap=0.0,
    legend=dict(
        orientation="h",
        yanchor="top",
        y=-0.15,
        xanchor="center",
        x=0.5
    ),
    margin=dict(l=60, r=40, t=100, b=120),
    showlegend=True
)

# Add custom annotations and shapes from JSON
for item in annotations_data:
    if item['type'] == 'line':
        fig.add_shape(
            type='line',
            x0=item['x_start'],
            x1=categories[-1],
            y0=item['y'],
            y1=item['y'],
            line=dict(color=item['color'], width=1)
        )
    elif item['type'] == 'text':
        fig.add_annotation(
            x=item['x'],
            y=item['y'],
            text=item['text'],
            showarrow=False,
            font=dict(color=item['color'], size=10),
            xanchor=item['align'],
            yanchor=item['valign'],
            xshift=5 if item['align'] == 'left' else 0, # Add a small shift for left-aligned text
            yshift=3 if item['valign'] == 'bottom' else 0
        )

# Add axis labels as annotations to match original placement
fig.add_annotation(
    text=texts['y_axis_title'],
    xref="paper", yref="y",
    x=-0.01, y=0,
    xanchor='right', yanchor='top',
    showarrow=False,
    yshift=-5
)
fig.add_annotation(
    text=texts['x_axis_title'],
    xref="x", yref="paper",
    x=categories[-1], y=-0.12,
    xanchor='right', yanchor='top',
    showarrow=False
)

# Generate output PNG file
output_filename = json_path.stem + ".png"
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")