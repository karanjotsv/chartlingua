import sys
import json
import pathlib
import plotly.graph_objects as go

# Read the JSON file path from the command-line argument
json_path = sys.argv[1]

# Load chart configuration from the JSON file
with open(json_path, 'r', encoding='utf-8') as f:
    config = json.load(f)

# Extract data, texts, and colors from the configuration
chart_data = config['chart_data']
texts = config['texts']
colors = config['colors']

# Prepare data for plotting, ensuring original order is maintained
categories = [d['category'] for d in chart_data]
values = [d['value'] for d in chart_data]

# Create a new figure
fig = go.Figure()

# Add the horizontal bar trace
fig.add_trace(go.Bar(
    y=categories,
    x=values,
    orientation='h',
    marker_color=colors[0],
    name=''  # Use an empty name to avoid "trace 0" in hover text
))

# Update the layout of the chart for a professional and accurate appearance
fig.update_layout(
    plot_bgcolor='white',
    paper_bgcolor='white',
    font_family="Arial",
    margin=dict(l=100, r=40, t=40, b=80),
    showlegend=False,
    xaxis=dict(
        title_text=texts.get('x_axis_title'),
        range=[0, 110],
        tick0=0,
        dtick=10,
        ticksuffix='%',
        showgrid=True,
        gridcolor='lightgray',
        griddash='dot',
        linecolor='black'
    ),
    yaxis=dict(
        title_text=texts.get('y_axis_title'),
        linecolor='black'
    )
)

# Add the source text as an annotation at the bottom right
if texts.get('source'):
    fig.add_annotation(
        text=texts['source'],
        xref="paper",
        yref="paper",
        x=0.99,
        y=-0.18,
        showarrow=False,
        xanchor='right',
        yanchor='top',
        align='right',
        font=dict(size=12, color="dimgray")
    )

# Determine the output filename from the input JSON path
output_path = pathlib.Path(json_path).with_suffix('.png')

# Save the figure to a high-resolution PNG file
fig.write_image(output_path, scale=2)

print(f"Chart saved to {output_path}")