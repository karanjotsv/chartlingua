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

# Load data from JSON file
with open(json_path, 'r', encoding='utf-8') as f:
    chart_info = json.load(f)

# Extract data for the chart
chart_data = chart_info.get('chart_data', [])
texts = chart_info.get('texts', {})
colors = chart_info.get('colors', [])

# Prepare data for Plotly pie chart
labels = [item['label'] for item in chart_data]
values = [item['value'] for item in chart_data]

# Create the pie chart trace
fig = go.Figure(data=[go.Pie(
    labels=labels,
    values=values,
    marker=dict(colors=colors, line=dict(color='#000000', width=1)),
    hoverinfo='label+percent',
    textinfo='value',
    textposition='outside',
    sort=False  # Preserve the order from the JSON file
)])

# Update layout
title_text = texts.get('title')
if title_text:
    fig.update_layout(title_text=title_text)

fig.update_layout(
    showlegend=True,
    font=dict(
        family="Arial",
        size=12,
        color="black"
    ),
    paper_bgcolor='white',
    plot_bgcolor='white',
    legend=dict(
        x=0.8,
        y=0.5,
        traceorder='normal',
        font=dict(
            family="Arial",
            size=12
        ),
        bgcolor='rgba(255,255,255,0.5)'
    ),
    margin=dict(l=40, r=150, t=40, b=40) # Adjust right margin for legend
)

# Generate output filename from JSON path
base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_filename}.png"

# Save the figure as a PNG image
try:
    fig.write_image(output_filename, scale=2)
    print(f"Chart saved as {output_filename}")
except ValueError as e:
    if "requires the kaleido package" in str(e):
        print("Error: The 'kaleido' package is required to save images.")
        print("Please install it using: pip install kaleido")
    else:
        print(f"An error occurred: {e}")
    sys.exit(1)