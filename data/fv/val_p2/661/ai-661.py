import sys
import json
import pathlib
import plotly.graph_objects as go

# Ensure a JSON file path is provided as a command-line argument
if len(sys.argv) != 2:
    print(f"Usage: python {sys.argv[0]} <json_file_path>")
    sys.exit(1)

# Get the JSON file path from the command-line argument
json_file_path = pathlib.Path(sys.argv[1])

# Check if the file exists
if not json_file_path.is_file():
    print(f"Error: File not found at {json_file_path}")
    sys.exit(1)

# Read data from the JSON file
with open(json_file_path, 'r', encoding='utf-8') as f:
    chart_info = json.load(f)

# Extract data, texts, and colors from the loaded JSON
chart_data = chart_info.get("chart_data", [])
texts = chart_info.get("texts", {})
colors = chart_info.get("colors", [])

# Initialize the figure
fig = go.Figure()

# Add traces to the figure by iterating through the chart_data
for i, series in enumerate(chart_data):
    color = colors[i % len(colors)] if colors else None
    fig.add_trace(go.Scatter(
        x=series.get("x"),
        y=series.get("y"),
        name=series.get("name", ""),
        mode='lines',
        line=dict(color=color, width=2)
    ))

# Update the layout of the figure
fig.update_layout(
    title=dict(
        text=texts.get("title"),
        x=0.05,
        xanchor='left',
        font=dict(
            family="Arial",
            size=16,
            color="black"
        )
    ),
    xaxis=dict(
        title_text=texts.get("x_axis_title"),
        showgrid=False,
        showline=True,
        linecolor='black',
        linewidth=1,
        tickfont=dict(family="Arial", size=12, color="black"),
        title_font=dict(family="Arial", size=14, color="black"),
        tickangle=0
    ),
    yaxis=dict(
        title_text=texts.get("y_axis_title"),
        range=[0, 12.5],
        dtick=2,
        showgrid=True,
        gridcolor='lightgray',
        showline=True,
        linecolor='black',
        linewidth=1,
        tickfont=dict(family="Arial", size=12, color="black"),
        title_font=dict(family="Arial", size=14, color="black")
    ),
    font=dict(
        family="Arial",
        size=12,
        color="black"
    ),
    plot_bgcolor='white',
    paper_bgcolor='white',
    showlegend=False,
    margin=dict(l=80, r=40, t=80, b=80)
)

# Define the output filename based on the input JSON filename
output_filename = json_file_path.with_suffix('.png')

# Save the figure as a PNG image
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")