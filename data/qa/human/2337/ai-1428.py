import sys
import json
import plotly.graph_objects as go
from pathlib import Path

# Ensure a JSON file path is provided as a command-line argument
if len(sys.argv) != 2:
    print(f"Usage: python {Path(__file__).name} <json_file_path>")
    sys.exit(1)

json_path = Path(sys.argv[1])

# Verify the JSON file exists
if not json_path.is_file():
    print(f"Error: JSON file not found at '{json_path}'")
    sys.exit(1)

# Load data from the specified JSON file
with open(json_path, 'r', encoding='utf-8') as f:
    chart_info = json.load(f)

# Extract data and text from the JSON structure
chart_data = chart_info.get("chart_data", {})
texts = chart_info.get("texts", {})
colors = chart_info.get("colors", [])
categories = chart_data.get("categories", [])
series_data = chart_data.get("series", [])

# Initialize the figure
fig = go.Figure()

# Add a bar trace for each series, preserving order
for i, series in enumerate(series_data):
    fig.add_trace(go.Bar(
        name=series.get("name"),
        x=categories,
        y=series.get("data"),
        marker_color=colors[i % len(colors)],  # Cycle through colors if needed
        text=series.get("data"),
        textposition='outside',
        textfont=dict(
            family="Arial",
            size=12,
            color='black'
        ),
        cliponaxis=False
    ))

# Configure the chart layout
fig.update_layout(
    barmode='group',
    plot_bgcolor='white',
    font=dict(family="Arial", size=12, color="black"),
    title=dict(
        text=texts.get("title") if texts.get("title") else None,
        font=dict(size=24)
    ),
    xaxis=dict(
        title_text=texts.get("x_axis_title"),
        showgrid=False,
        showline=True,
        linewidth=1,
        linecolor='black'
    ),
    yaxis=dict(
        title_text=texts.get("y_axis_title"),
        showgrid=True,
        gridcolor='#E5E5E5',
        range=[0, 500],
        dtick=100,
        showline=False
    ),
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=-0.25,
        xanchor="center",
        x=0.5
    ),
    margin=dict(l=70, r=40, t=40, b=120)
)

# Add source annotation if present in the JSON
if texts.get("source"):
    fig.add_annotation(
        text=texts["source"],
        align='right',
        showarrow=False,
        xref='paper',
        yref='paper',
        x=1.0,
        y=-0.35,
        xanchor='right',
        yanchor='bottom',
        font=dict(family="Arial", size=10, color="grey")
    )

# Define the output image file path
output_image_path = f"{json_path.stem}.png"

# Save the figure to a PNG file
fig.write_image(output_image_path, scale=2)

print(f"Chart saved to {output_image_path}")