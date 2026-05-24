import sys
import json
import plotly.graph_objects as go
from pathlib import Path

# Load data from the JSON file provided as a command-line argument
json_path = Path(sys.argv[1])
with open(json_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

# Extract data and text elements
chart_data = data['chart_data']
texts = data['texts']
colors = data['colors']

x_values = [d['x'] for d in chart_data]
y_values = [d['y'] for d in chart_data]

# Create the figure
fig = go.Figure()

# Add the bar trace
fig.add_trace(go.Bar(
    x=x_values,
    y=y_values,
    text=[f'{y:.1f}%'.replace('.0%', '%') for y in y_values],
    textposition='outside',
    marker_color=colors[0],
    hoverinfo='none',
    cliponaxis=False
))

# Configure the layout
fig.update_layout(
    font=dict(family="Arial", size=12),
    plot_bgcolor='white',
    paper_bgcolor='white',
    showlegend=False,
    xaxis=dict(
        title_text=texts.get('x_axis_title'),
        tickvals=x_values,
        ticktext=[str(x) for x in x_values],
        showgrid=False,
        zeroline=False,
        linecolor='lightgrey'
    ),
    yaxis=dict(
        title_text=texts.get('y_axis_title'),
        range=[0, 12.5],
        tickvals=[0, 2, 4, 6, 8, 10, 12],
        ticktext=[f"{i}%" for i in [0, 2, 4, 6, 8, 10, 12]],
        showgrid=True,
        gridcolor='lightgrey',
        zeroline=False
    ),
    margin=dict(l=90, r=20, t=40, b=100),
    annotations=[
        dict(
            text=texts.get('source'),
            align='right',
            showarrow=False,
            xref='paper',
            yref='paper',
            x=0.99,
            y=-0.18,
            xanchor='right',
            yanchor='top',
            font=dict(size=10)
        )
    ]
)

# Update trace font for bar labels
fig.update_traces(textfont_size=11)

# Generate and save the output image
output_filename_base = json_path.stem
fig.write_image(f"{output_filename_base}.png", scale=2)

print(f"Chart saved to {output_filename_base}.png")