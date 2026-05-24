import sys
import json
import plotly.graph_objects as go
from pathlib import Path

# Check for command-line argument
if len(sys.argv) != 2:
    print("Usage: python create_chart.py <json_file_path>")
    sys.exit(1)

json_path_str = sys.argv[1]
json_path = Path(json_path_str)

# Ensure the JSON file exists
if not json_path.is_file():
    print(f"Error: JSON file not found at '{json_path_str}'")
    sys.exit(1)

# Read data from the JSON file
with open(json_path, 'r', encoding='utf-8') as f:
    chart_info = json.load(f)

# Extract data for plotting
categories = chart_info['categories']
chart_data = chart_info['chart_data']
texts = chart_info['texts']
colors = chart_info['colors']

# Create figure
fig = go.Figure()

# Add traces for each data series
for i, series in enumerate(chart_data):
    # Set text color based on bar color for visibility
    # The last series (light gray bar) needs black text
    text_font_color = 'black' if i == len(chart_data) - 1 else 'white'

    fig.add_trace(go.Bar(
        x=categories,
        y=series['y'],
        name=series['name'],
        marker_color=colors[i],
        text=series['text'],
        textposition='inside',
        insidetextanchor='middle',
        textfont=dict(
            family="Arial",
            color=text_font_color,
            size=12
        ),
        hoverinfo='none'
    ))

# Update layout
fig.update_layout(
    barmode='stack',
    plot_bgcolor='white',
    paper_bgcolor='white',
    font=dict(family="Arial", size=12),
    margin=dict(l=80, r=40, t=50, b=120),
    xaxis=dict(
        title_text=texts['x_axis_title'],
        tickmode='array',
        tickvals=categories,
        ticktext=[str(cat) for cat in categories],
        showgrid=False,
        showline=True,
        linecolor='lightgray',
        ticks='outside',
        tickfont=dict(size=12)
    ),
    yaxis=dict(
        title_text=texts['y_axis_title'],
        range=[0, 101],
        tickvals=[0, 25, 50, 75, 100],
        ticksuffix='%',
        gridcolor='lightgray',
        zeroline=False,
        tickfont=dict(size=12)
    ),
    legend=dict(
        orientation='h',
        yanchor='top',
        y=-0.2,
        xanchor='center',
        x=0.5
    ),
    annotations=[
        dict(
            text=texts['source_text'],
            showarrow=False,
            xref='paper',
            yref='paper',
            x=1.0,
            y=-0.28,
            xanchor='right',
            yanchor='bottom',
            font=dict(size=12, color='gray')
        )
    ]
)

# Generate output filename from JSON path
output_filename = json_path.stem + ".png"

# Save the figure as a PNG image
fig.write_image(output_filename, scale=2)

print(f"Chart saved as {output_filename}")