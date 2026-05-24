import sys
import json
import os
import plotly.graph_objects as go

# Check for command-line argument
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]

# Check if the JSON file exists
if not os.path.exists(json_path):
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)

# Read data from the JSON file
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_info = json.load(f)
except json.JSONDecodeError:
    print(f"Error: Invalid JSON format in {json_path}")
    sys.exit(1)


# Extract data for the chart
chart_data = chart_info.get('chart_data', [])
texts = chart_info.get('texts', {})
colors = chart_info.get('colors', [])

# Prepare data for Plotly
labels = [item['label'] for item in chart_data]
values = [item['value'] for item in chart_data]

# Create the pie chart
fig = go.Figure()

fig.add_trace(go.Pie(
    labels=labels,
    values=values,
    marker=dict(colors=colors, line=dict(color='#FFFFFF', width=1)),
    textinfo='percent',
    texttemplate='%{value}%',
    hoverinfo='label+percent',
    textposition='outside',
    sort=False  # This is crucial to preserve the original data order
))

# Combine title and subtitle
title_text = f"<b>{texts.get('title', '')}</b><br>{texts.get('subtitle', '')}"

# Update layout
fig.update_layout(
    title=dict(
        text=title_text,
        y=0.95,
        x=0.5,
        xanchor='center',
        yanchor='top'
    ),
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=-0.15,
        xanchor="center",
        x=0.5
    ),
    paper_bgcolor='#e6e6fa',
    font=dict(
        family="Arial",
        size=12,
        color="#000000"
    ),
    margin=dict(t=100, b=100, l=40, r=40),
    showlegend=True
)

# Determine the output filename from the input JSON filename
base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_image_filename = f"{base_filename}.png"

# Save the chart as a high-resolution PNG image
try:
    fig.write_image(output_image_filename, scale=2)
    print(f"Chart saved to {output_image_filename}")
except ValueError as e:
    if "requires the kaleido" in str(e) or "requires the orca" in str(e):
        print("\nError: Image export requires the 'kaleido' package.")
        print("Please install it using: pip install kaleido")
        sys.exit(1)
    else:
        raise e