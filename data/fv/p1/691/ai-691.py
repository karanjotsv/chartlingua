import sys
import json
import plotly.graph_objects as go
import os

# Check if the JSON file path is provided as a command-line argument
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]

# Check if the file exists
if not os.path.exists(json_path):
    print(f"Error: File not found at {json_path}")
    sys.exit(1)

# Load data from the specified JSON file
with open(json_path, 'r', encoding='utf-8') as f:
    chart_info = json.load(f)

# Extract data for the chart
chart_data = chart_info.get("chart_data", [])
texts = chart_info.get("texts", {})
colors = chart_info.get("colors", {})

# Prepare data for Plotly
labels = [item['label'] for item in chart_data]
values = [item['value'] for item in chart_data]
slice_colors = colors.get("slices", [])
background_color = colors.get("background", "#FFFFFF")

# Create the pie chart figure
fig = go.Figure()

fig.add_trace(go.Pie(
    labels=labels,
    values=values,
    hole=0,
    marker=dict(colors=slice_colors),
    textinfo='percent',
    textposition='outside',
    textfont=dict(size=14, family="Arial"),
    hoverinfo='label+percent',
    sort=False  # Preserve the order from the JSON file
))

# Update layout for title, legend, and general appearance
fig.update_layout(
    title=dict(
        text=texts.get('title'),
        y=0.95,
        x=0.5,
        xanchor='center',
        yanchor='top',
        font=dict(
            family="Arial",
            size=22,
            color='black'
        )
    ),
    legend=dict(
        orientation="h",
        yanchor="top",
        y=-0.1,
        xanchor="center",
        x=0.5,
        font=dict(
            family="Arial",
            size=14
        )
    ),
    font=dict(
        family="Arial"
    ),
    paper_bgcolor=background_color,
    plot_bgcolor=background_color,
    margin=dict(t=100, b=120, l=40, r=40)
)

# Define the output filename based on the input JSON filename
base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_filename}.png"

# Save the figure as a high-resolution PNG image
try:
    fig.write_image(output_filename, scale=2)
    print(f"Chart saved as {output_filename}")
except Exception as e:
    print(f"Error saving image: {e}")
    print("Please ensure you have 'kaleido' installed (`pip install kaleido`) for static image export.")
    sys.exit(1)