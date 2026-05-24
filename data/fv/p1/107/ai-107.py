import sys
import json
import plotly.graph_objects as go
from pathlib import Path

# Check for command-line argument
if len(sys.argv) != 2:
    print("Usage: python script.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]
json_path_obj = Path(json_path)

# Check if the JSON file exists
if not json_path_obj.is_file():
    print(f"Error: JSON file not found at '{json_path}'")
    sys.exit(1)

# Read data from the JSON file
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_info = json.load(f)
except json.JSONDecodeError:
    print(f"Error: Invalid JSON format in '{json_path}'")
    sys.exit(1)


# Extract data and texts from the loaded JSON
chart_data = chart_info.get("chart_data", {})
texts = chart_info.get("texts", {})
colors = chart_info.get("colors", [])
categories = chart_data.get("categories", [])
series_list = chart_data.get("series", [])

# Initialize the figure
fig = go.Figure()

# Add traces for each data series
for i, series in enumerate(series_list):
    fig.add_trace(go.Bar(
        x=categories,
        y=series.get("data", []),
        name=series.get("name", ""),
        marker=dict(
            color=colors[i % len(colors)] if colors else '#CCCCCC',
            line=dict(
                color='#00008B',  # Dark blue border for visibility
                width=1.5
            )
        ),
        text=series.get("data", []),
        texttemplate='<b>%{y}</b>',
        textposition='outside',
        textfont=dict(
            family="Arial",
            size=16,
            color='black'
        ),
        cliponaxis=False,
        hoverinfo='none'
    ))

# Update layout for a professional look and feel
fig.update_layout(
    title=dict(
        text=f"<b>{texts.get('title', '')}</b>",
        font=dict(
            family="Arial",
            size=20
        ),
        x=0.5,
        xanchor='center'
    ),
    xaxis=dict(
        title_text=f"<b>{texts.get('x_axis_title', '')}</b>",
        showgrid=False,
        zeroline=False,
        type='category' # Ensure x-axis is treated as categorical
    ),
    yaxis=dict(
        title_text=texts.get('y_axis_title', None),
        showgrid=True,
        gridcolor='lightgrey',
        range=[0, 20],
        dtick=2,
        zeroline=True,
        zerolinecolor='lightgrey'
    ),
    legend=dict(
        x=0.02,
        y=0.98,
        xanchor='left',
        yanchor='top',
        bgcolor='white',
        bordercolor='black',
        borderwidth=1
    ),
    plot_bgcolor='white',
    font=dict(
        family="Arial",
        size=12,
        color="black"
    ),
    margin=dict(t=80, b=80, l=60, r=40)
)

# Generate the output filename from the input JSON filename
output_filename = f"{json_path_obj.stem}.png"

# Save the figure as a high-resolution PNG image
try:
    fig.write_image(output_filename, scale=2)
    print(f"Chart saved to {output_filename}")
except Exception as e:
    print(f"Error saving image: {e}")
    sys.exit(1)