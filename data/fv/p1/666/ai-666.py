import sys
import json
from pathlib import Path
import plotly.graph_objects as go

# Check for command-line argument
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <json_file_path>")
    sys.exit(1)

# Get paths from command-line argument
json_path = Path(sys.argv[1])
output_path = json_path.with_suffix(".png")

# Load data from JSON file
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_info = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_path}")
    sys.exit(1)

# Extract data for plotting
chart_data = chart_info.get("chart_data", [])
texts = chart_info.get("texts", {})
colors = chart_info.get("colors", [])

categories = [item['category'] for item in chart_data]
values = [item['value'] for item in chart_data]
annotations_text = [item.get('annotation', '') for item in chart_data]

# Create the figure
fig = go.Figure()

# Add bar trace
fig.add_trace(go.Bar(
    x=categories,
    y=values,
    marker_color=colors,
    text=annotations_text,
    textposition='outside',
    textfont=dict(family="Arial", size=12),
    cliponaxis=False,
    hoverinfo='none'
))

# Update layout
fig.update_layout(
    title=dict(
        text=texts.get("title"),
        x=0.5,
        xanchor='center',
        font=dict(size=20)
    ),
    xaxis=dict(
        title_text=texts.get("x_axis_title"),
        showline=True,
        linecolor='black',
        linewidth=1,
        showgrid=False,
        mirror=True,
        ticks='',
        tickfont=dict(size=12)
    ),
    yaxis=dict(
        title_text=texts.get("y_axis_title"),
        range=[0, 500],
        tickvals=[i for i in range(0, 501, 50)],
        showline=True,
        linecolor='black',
        linewidth=1,
        showgrid=False,
        mirror=True,
        ticks='outside',
        tickfont=dict(size=12)
    ),
    font=dict(
        family="Arial",
        size=12,
        color="black"
    ),
    plot_bgcolor='white',
    paper_bgcolor='white',
    showlegend=False,
    margin=dict(l=60, r=40, b=120, t=100)
)

# Add source/note annotation at the bottom
fig.add_annotation(
    text=texts.get("source"),
    xref="paper",
    yref="paper",
    x=0,
    y=-0.25, # Adjusted for long text and line break
    xanchor='left',
    yanchor='top',
    showarrow=False,
    align='left',
    font=dict(
        family="Arial",
        size=10,
        color="black"
    )
)

# Write image to file
fig.write_image(output_path, scale=2)

print(f"Chart saved to {output_path}")