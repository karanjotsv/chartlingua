import sys
import json
import plotly.graph_objects as go
from pathlib import Path

# Check for command-line argument
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <json_file_path>")
    sys.exit(1)

# Get JSON file path from command-line argument
json_file_path = Path(sys.argv[1])

# Read data from the JSON file
with open(json_file_path, 'r', encoding='utf-8') as f:
    chart_data = json.load(f)

# Extract data and texts
data = chart_data['chart_data']
texts = chart_data['texts']
colors = chart_data['colors']

# Prepare data for Plotly
categories = [item['category'] for item in data]
values = [item['value'] for item in data]

# Create the bar chart
fig = go.Figure()

fig.add_trace(go.Bar(
    x=categories,
    y=values,
    marker_color=colors[0],
    text=values,
    textposition='outside',
    texttemplate='%{text:.2f}',
    cliponaxis=False # Allow text to be displayed outside the plot area
))

# Update layout
fig.update_layout(
    font_family="Arial",
    font_size=12,
    plot_bgcolor='white',
    paper_bgcolor='white',
    margin=dict(l=80, r=40, t=40, b=100),
    showlegend=False,
    yaxis=dict(
        title=texts['y_axis_title'],
        title_font_size=14,
        range=[0, 1200],
        dtick=200,
        showgrid=True,
        gridcolor='#e0e0e0',
        gridwidth=1,
        tickfont_size=14,
        tickformat=' ', # Use space as thousands separator
        zeroline=False
    ),
    xaxis=dict(
        title=texts['x_axis_title'],
        showgrid=False,
        tickfont_size=14
    ),
    annotations=[
        dict(
            text=texts['source'],
            align='right',
            showarrow=False,
            xref='paper',
            yref='paper',
            x=1.0,
            y=-0.15,
            xanchor='right',
            yanchor='top'
        )
    ]
)

fig.update_traces(textfont_size=12, textfont_color='black')

# Define output image path from the input JSON path
output_image_path = json_file_path.with_suffix('.png')

# Save the chart as a PNG image
fig.write_image(output_image_path, scale=2)

print(f"Chart saved to {output_image_path}")