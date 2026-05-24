import sys
import json
import os
import plotly.graph_objects as go

# Check if a file path is provided as a command-line argument
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <path_to_json_file>")
    sys.exit(1)

json_file_path = sys.argv[1]

# Check if the file exists
if not os.path.exists(json_file_path):
    print(f"Error: File not found at {json_file_path}")
    sys.exit(1)

# Read the chart data from the specified JSON file
with open(json_file_path, 'r', encoding='utf-8') as f:
    chart_info = json.load(f)

# Extract data, texts, and colors from the JSON object
chart_data = chart_info.get("chart_data", [])
texts = chart_info.get("texts", {})
colors = chart_info.get("colors", [])
chart_type = chart_info.get("chart_type")

# Prepare data for Plotly pie chart
labels = [f"{item['label']} {item['value']}%" for item in chart_data]
values = [item['value'] for item in chart_data]

# Create the pie chart trace
fig = go.Figure()

if chart_type == "pie":
    fig.add_trace(go.Pie(
        labels=labels,
        values=values,
        marker=dict(colors=colors, line=dict(color='#FFFFFF', width=1)),
        hoverinfo='none',
        textinfo='none',
        sort=False,
        direction='clockwise'
    ))

# Configure the layout
layout_annotations = []
if texts.get("source"):
    layout_annotations.append(
        dict(
            xref="paper", yref="paper",
            x=0.99, y=-0.05,
            xanchor="right", yanchor="top",
            text=texts["source"],
            showarrow=False,
            font=dict(family="Arial", size=12, color="grey")
        )
    )

fig.update_layout(
    showlegend=True,
    legend=dict(
        orientation="v",
        yanchor="top",
        y=1.0,
        xanchor="left",
        x=1.02,
        font=dict(family="Arial")
    ),
    font=dict(family="Arial", size=14),
    margin=dict(l=40, r=300, t=40, b=80),
    annotations=layout_annotations,
    paper_bgcolor='white',
    plot_bgcolor='white'
)

# Determine the output filename from the input JSON path
base_filename = os.path.splitext(os.path.basename(json_file_path))[0]
output_image_path = f"{base_filename}.png"

# Save the figure as a PNG image
fig.write_image(output_image_path, scale=2)

print(f"Chart saved to {output_image_path}")