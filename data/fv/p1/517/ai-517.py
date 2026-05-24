import sys
import json
import os
import plotly.graph_objects as go

# Check for command-line argument
if len(sys.argv) != 2:
    print(f"Usage: python {os.path.basename(__file__)} <json_file_path>")
    sys.exit(1)

json_path = sys.argv[1]

# Read data from the JSON file
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_info = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at '{json_path}'")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from '{json_path}'")
    sys.exit(1)

# Extract data, texts, and colors
chart_data = chart_info.get("chart_data", [])
texts = chart_info.get("texts", {})
colors = chart_info.get("colors", {})

# Create the figure
fig = go.Figure()

# Add trace(s) to the figure
for series in chart_data:
    fig.add_trace(go.Scatter(
        x=series.get("x"),
        y=series.get("y"),
        mode='lines',
        fill='tozeroy',
        line=dict(color=colors.get("line"), width=2.5),
        fillcolor=colors.get("fill"),
        showlegend=False
    ))

# Update layout
fig.update_layout(
    title=dict(
        text=texts.get("title"),
        x=0.5,
        font=dict(size=18)
    ),
    xaxis_title=texts.get("x_axis_title"),
    yaxis_title=texts.get("y_axis_title"),
    font=dict(
        family="Arial",
        size=12
    ),
    plot_bgcolor=colors.get("background", "#FFFFFF"),
    paper_bgcolor=colors.get("background", "#FFFFFF"),
    margin=dict(l=60, r=30, t=80, b=60),
    xaxis=dict(
        showgrid=False,
        tickmode='linear',
        dtick=1,
        tickangle=0
    ),
    yaxis=dict(
        showgrid=True,
        gridcolor=colors.get("grid", "#D3D3D3"),
        range=[0, 250],
        tickvals=[0, 50, 100, 150, 200, 250]
    )
)

# Determine output filename and save the image
base_name = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_name}.png"
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")