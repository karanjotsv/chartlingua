import sys
import json
import pathlib
import plotly.graph_objects as go

# Ensure a JSON file path is provided as a command-line argument
if len(sys.argv) != 2:
    print(f"Usage: python {pathlib.Path(__file__).name} <json_file_path>")
    sys.exit(1)

# Define file paths
json_file_path = pathlib.Path(sys.argv[1])
if not json_file_path.is_file():
    print(f"Error: File not found at {json_file_path}")
    sys.exit(1)

output_image_path = json_file_path.with_suffix(".png")

# Load all data and text from the JSON file
with open(json_file_path, 'r', encoding='utf-8') as f:
    chart_info = json.load(f)

chart_data = chart_info.get("chart_data", [])
texts = chart_info.get("texts", {})
colors = chart_info.get("colors", [])

# Prepare data for plotting
categories = [d.get("category") for d in chart_data]
values = [d.get("value") for d in chart_data]

# Create the figure object
fig = go.Figure()

# Add the bar trace, using the single color for all bars
fig.add_trace(go.Bar(
    x=categories,
    y=values,
    marker_color=colors[0] if colors else None,
    name='' # Hide from legend
))

# Combine title and subtitle using HTML for rich formatting
title_text = ""
if texts.get("title"):
    title_text += f"<b>{texts['title']}</b>"
if texts.get("subtitle"):
    title_text += f"<br>{texts['subtitle']}"

# Apply layout settings
fig.update_layout(
    title_text=title_text,
    title_x=0.5,
    title_y=0.95,
    title_xanchor='center',
    title_yanchor='top',
    font_family="Arial",
    font_size=14,
    plot_bgcolor='white',
    paper_bgcolor='white',
    showlegend=False,
    xaxis=dict(
        title_text=texts.get("x_axis_title"),
        showgrid=False,
        showline=True,
        linewidth=1,
        linecolor='black',
        mirror=True,
        ticks='',
        tickfont=dict(size=12)
    ),
    yaxis=dict(
        title_text=texts.get("y_axis_title"),
        showgrid=False,
        showticklabels=False, # Replicate missing y-axis labels
        showline=True,
        linewidth=1,
        linecolor='black',
        mirror=True,
        zeroline=False
    ),
    margin=dict(t=100, b=80, l=80, r=40)
)

# Write the output image file
fig.write_image(output_image_path, scale=2)

print(f"Chart successfully generated and saved to {output_image_path}")