import sys
import json
import pathlib
import plotly.graph_objects as go

# Check for command-line argument
if len(sys.argv) != 2:
    print(f"Usage: {sys.argv[0]} <json_file_path>")
    sys.exit(1)

# Get file paths
json_file_path = pathlib.Path(sys.argv[1])
if not json_file_path.is_file():
    print(f"Error: File not found at {json_file_path}")
    sys.exit(1)

output_image_path = json_file_path.with_suffix(".png")

# Load data from JSON
with open(json_file_path, 'r', encoding='utf-8') as f:
    chart_info = json.load(f)

chart_data = chart_info["chart_data"]
texts = chart_info["texts"]
colors = chart_info["colors"]

# Create figure
fig = go.Figure()

# Add traces from chart_data
for i, series in enumerate(chart_data):
    fig.add_trace(go.Bar(
        x=series['x'],
        y=series['y'],
        name=series.get('name', ''),
        marker_color=colors[i % len(colors)]
    ))

# Update layout
fig.update_layout(
    title_text=texts.get("title", ""),
    title_x=0.5,
    title_font=dict(
        family="Arial",
        size=30,
        color="black",
    ),
    yaxis_title_text=texts.get("y_axis_title", ""),
    xaxis_title_text=texts.get("x_axis_title", ""),
    font=dict(
        family="Arial",
        size=14,
        color="black"
    ),
    plot_bgcolor='white',
    paper_bgcolor='white',
    showlegend=False,
    margin=dict(l=100, r=40, t=100, b=80),
    yaxis=dict(
        showgrid=True,
        gridcolor='#e5e5e5',
        range=[0, 25000000],
        tickformat=','
    ),
    xaxis=dict(
        showgrid=False,
        tickangle=0,
        type='category' # Ensures all x-axis labels are shown
    )
)

# Set bold title font using update_traces or direct layout property update
fig.update_layout(
    title_font_weight="bold"
)

# Write image to file
fig.write_image(output_image_path, scale=2)

print(f"Chart saved to {output_image_path}")