import sys
import json
import plotly.graph_objects as go
import os

# Check for the required command-line argument
if len(sys.argv) != 2:
    print(f"Usage: python {sys.argv[0]} <json_file_path>")
    sys.exit(1)

# Get the JSON file path from the command-line argument
json_path = sys.argv[1]

# Read and parse the JSON file
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_config = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at '{json_path}'")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from '{json_path}'")
    sys.exit(1)

# Extract data and texts from the loaded JSON
chart_data = chart_config.get('chart_data', [])
texts = chart_config.get('texts', {})
colors = chart_config.get('colors', [])

# Prepare data for Plotly, preserving the order from the JSON
labels = [item['label'] for item in chart_data]
values = [item['value'] for item in chart_data]

# Create the pie chart trace
pie_trace = go.Pie(
    labels=labels,
    values=values,
    marker=dict(
        colors=colors,
        line=dict(color='#FFFFFF', width=1.5)
    ),
    hoverinfo='label+percent',
    textinfo='none',
    sort=False  # This is crucial to preserve the original data order
)

# Create the figure
fig = go.Figure(data=[pie_trace])

# Combine title and subtitle using HTML for rich formatting
title_text = f"<b>{texts.get('title', '')}</b><br><sub>{texts.get('subtitle', '')}</sub>"

# Update layout for a professional look and feel
fig.update_layout(
    title=dict(
        text=title_text,
        y=0.95,
        x=0.5,
        xanchor='center',
        yanchor='top'
    ),
    font=dict(
        family="Arial",
        size=12,
        color="white"
    ),
    paper_bgcolor='black',
    plot_bgcolor='black',
    margin=dict(t=120, b=150, l=40, r=40),
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=-0.3,
        xanchor="center",
        x=0.5
    ),
    showlegend=True
)

# Add source annotation at the bottom, ensuring it doesn't overlap with the legend
fig.add_annotation(
    text=texts.get('source', ''),
    align='left',
    showarrow=False,
    xref='paper',
    yref='paper',
    x=0,
    y=-0.4, # Positioned below the legend
    xanchor='left',
    yanchor='bottom'
)

# Generate the output image filename from the input JSON filename
base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_filename}.png"

# Save the figure to a high-resolution PNG file
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")