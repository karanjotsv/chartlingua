import sys
import json
import plotly.graph_objects as go
from pathlib import Path

# Check for command-line argument
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <path_to_json_file>")
    sys.exit(1)

# Get JSON file path from command-line argument
json_file_path = Path(sys.argv[1])

# Read data from the JSON file
try:
    with open(json_file_path, 'r', encoding='utf-8') as f:
        chart_info = json.load(f)
except (FileNotFoundError, json.JSONDecodeError) as e:
    print(f"Error reading or parsing JSON file: {e}")
    sys.exit(1)

# Extract data and texts
chart_data = chart_info.get("chart_data", [])
texts = chart_info.get("texts", {})
colors = chart_info.get("colors", [])

# Initialize figure
fig = go.Figure()

# Add traces for each data series
for i, series in enumerate(chart_data):
    fig.add_trace(go.Bar(
        name=series['name'],
        x=series['x'],
        y=series['y'],
        marker_color=colors[i] if i < len(colors) else None,
        text=series['y'],
        textposition='outside',
        textfont=dict(
            family="Arial",
            size=12,
            color='black'
        ),
        cliponaxis=False
    ))

# Combine title and subtitle if they exist
chart_title = ""
if texts.get("title"):
    chart_title += f"<b>{texts['title']}</b>"
if texts.get("subtitle"):
    chart_title += f"<br><sub>{texts['subtitle']}</sub>"


# Update layout
fig.update_layout(
    barmode='group',
    title_text=chart_title if chart_title else None,
    yaxis_title=texts.get("y_axis_title"),
    xaxis_title=texts.get("x_axis_title"),
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=-0.3,
        xanchor="center",
        x=0.5
    ),
    plot_bgcolor='white',
    paper_bgcolor='white',
    font=dict(
        family="Arial",
        size=12,
        color="#333333"
    ),
    xaxis=dict(
        showgrid=False,
        tickmode='array',
        tickvals=chart_data[0]['x'] if chart_data else [],
        ticktext=[str(year) for year in (chart_data[0]['x'] if chart_data else [])]
    ),
    yaxis=dict(
        showgrid=True,
        gridcolor='#e0e0e0',
        range=[0, 135]
    ),
    margin=dict(l=80, r=40, t=60, b=150)
)

# Add source annotation
if texts.get("source"):
    fig.add_annotation(
        text=texts['source'],
        align='right',
        showarrow=False,
        xref='paper',
        yref='paper',
        x=1,
        y=-0.35,
        font=dict(
            family="Arial",
            size=12,
            color="#888888"
        )
    )

# Define output filename and save the image
output_filename_base = json_file_path.stem
output_path = f"{output_filename_base}.png"
fig.write_image(output_path, scale=2)

print(f"Chart saved to {output_path}")