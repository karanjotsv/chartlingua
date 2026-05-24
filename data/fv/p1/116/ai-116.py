import sys
import json
import os
import plotly.graph_objects as go

# Check if the path to the JSON file is provided as a command-line argument
if len(sys.argv) != 2:
    print("Usage: python create_chart.py <path_to_json_file>")
    sys.exit(1)

json_file_path = sys.argv[1]

# Check if the JSON file exists
if not os.path.exists(json_file_path):
    print(f"Error: JSON file not found at {json_file_path}")
    sys.exit(1)

# Read data from the JSON file
with open(json_file_path, 'r', encoding='utf-8') as f:
    chart_info = json.load(f)

# Extract data and texts from the loaded JSON
chart_data = chart_info.get("chart_data", [])
texts = chart_info.get("texts", {})
colors = chart_info.get("colors", [])

# Prepare data for the pie chart
labels = [item['category'] for item in chart_data]
values = [item['value'] for item in chart_data]

# Create the pie chart trace
# The 'pull' parameter is used to "pull out" a slice, replicating the original chart's emphasis.
# We determine which slice to pull based on the smaller value, assuming it's the one to highlight.
pull_values = [0.1 if v == min(values) else 0 for v in values]

fig = go.Figure()

fig.add_trace(go.Pie(
    labels=labels,
    values=values,
    marker_colors=colors,
    pull=pull_values,
    textinfo='none',  # Disable default text
    texttemplate='%{label}<br>%{value}%',
    hovertemplate='%{label}: %{value}%<extra></extra>',
    insidetextfont=dict(color='black', size=14),
    outsidetextfont=dict(color='black', size=14),
    sort=False # Preserve the original data order from the JSON
))

# Update layout
title_text = texts.get('title', '')

fig.update_layout(
    title_text=title_text,
    title_x=0.5,
    title_font=dict(size=22, family='Arial', color='black', weight='bold'),
    font=dict(family="Arial", size=12, color="black"),
    showlegend=False,
    paper_bgcolor='white',
    plot_bgcolor='white',
    margin=dict(l=50, r=50, t=100, b=50),
    width=600,
    height=500
)

# Determine the output filename from the input JSON filename
base_filename = os.path.splitext(os.path.basename(json_file_path))[0]
output_image_path = f"{base_filename}.png"

# Save the figure as a high-resolution PNG image
try:
    fig.write_image(output_image_path, scale=2)
    print(f"Chart saved to {output_image_path}")
except ValueError as e:
    if "requires the kaleido" in str(e) or "requires the orca" in str(e):
        print("\nError: Plotly image export requires the 'kaleido' package.")
        print("Please install it using: pip install kaleido")
        sys.exit(1)
    else:
        raise e