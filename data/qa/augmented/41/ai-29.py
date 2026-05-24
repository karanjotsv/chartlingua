import sys
import json
from pathlib import Path
import plotly.graph_objects as go

# Check for command-line argument
if len(sys.argv) != 2:
    print("Usage: python create_chart.py <json_file_path>")
    sys.exit(1)

# Get the JSON file path from the command-line argument
json_file_path = Path(sys.argv[1])

# Check if the JSON file exists
if not json_file_path.is_file():
    print(f"Error: JSON file not found at '{json_file_path}'")
    sys.exit(1)

# Read data from the JSON file
with open(json_file_path, 'r', encoding='utf-8') as f:
    chart_info = json.load(f)

# Extract data, texts, and colors from the loaded JSON
chart_data = chart_info.get("chart_data", [])
texts = chart_info.get("texts", {})
colors = chart_info.get("colors", [])

# Prepare data for Plotly
x_values = [item['x'] for item in chart_data]
y_values = [item['y'] for item in chart_data]

# Create the figure
fig = go.Figure()

# Add the line trace with markers and text labels
fig.add_trace(go.Scatter(
    x=x_values,
    y=y_values,
    mode='lines+markers+text',
    line=dict(color=colors[0], width=3),
    marker=dict(color=colors[0], size=8),
    text=[f'{y:.2f}' for y in y_values],
    textposition='top center',
    textfont=dict(
        family="Arial",
        size=12,
        color='black'
    ),
    hoverinfo='none',
    showlegend=False
))

# Update layout
fig.update_layout(
    font=dict(family="Arial", size=12, color="#000000"),
    title=dict(
        text=texts.get('title'),
        x=0.05,
        xanchor='left'
    ),
    xaxis=dict(
        title_text=texts.get('x_axis_title'),
        tickvals=x_values,
        ticktext=[str(x) for x in x_values],
        showgrid=True,
        gridcolor='#F0F0F0',
        gridwidth=1,
        zeroline=False,
        linecolor='lightgrey',
        ticks='outside'
    ),
    yaxis=dict(
        title_text=texts.get('y_axis_title'),
        range=[1.8, 3.2],
        tick0=1.8,
        dtick=0.2,
        showgrid=True,
        gridcolor='lightgrey',
        griddash='dash',
        zeroline=False,
        linecolor='lightgrey',
        ticks='outside'
    ),
    plot_bgcolor='white',
    paper_bgcolor='white',
    margin=dict(l=80, r=40, t=50, b=100),
    annotations=[
        dict(
            text=texts.get('source'),
            showarrow=False,
            xref='paper',
            yref='paper',
            x=1,
            y=-0.2,
            xanchor='right',
            yanchor='top',
            align='right',
            font=dict(family="Arial", size=12)
        )
    ]
)

# Generate the output PNG filename from the input JSON filename
output_filename = json_file_path.stem + ".png"

# Save the figure as a PNG image
fig.write_image(output_filename, scale=2)

print(f"Chart saved as {output_filename}")