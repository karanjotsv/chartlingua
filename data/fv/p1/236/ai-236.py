import sys
import json
import plotly.graph_objects as go

# Check if the correct number of arguments is provided
if len(sys.argv) != 2:
    print(f"Usage: python {sys.argv[0]} <json_file_path>")
    sys.exit(1)

# Get the JSON file path from the command-line arguments
json_file_path = sys.argv[1]

# Read the JSON file
try:
    with open(json_file_path, 'r', encoding='utf-8') as f:
        chart_json = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at '{json_file_path}'")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from '{json_file_path}'")
    sys.exit(1)

# Extract data, texts, and colors from the JSON object
chart_data = chart_json.get('chart_data', [])
texts = chart_json.get('texts', {})
colors = chart_json.get('colors', [])

# Prepare data for the pie chart
labels = [item.get('label', '') for item in chart_data]
values = [item.get('value', 0) for item in chart_data]

# Create the pie chart trace
pie_trace = go.Pie(
    labels=labels,
    values=values,
    marker=dict(colors=colors, line=dict(color='#FFFFFF', width=1)),
    sort=False,  # Preserve the original order from the JSON
    direction='clockwise',
    textinfo='none', # No text on the slices themselves
    hoverinfo='label+percent'
)

# Create the figure
fig = go.Figure(data=[pie_trace])

# Combine title and subtitle
title_text = texts.get('title') or ''
subtitle_text = texts.get('subtitle') or ''
if subtitle_text:
    title_text = f"{title_text}<br><sub>{subtitle_text}</sub>"

# Update layout
fig.update_layout(
    title_text=title_text,
    title_x=0.5,
    font=dict(
        family="Arial",
        size=12,
        color="black"
    ),
    showlegend=True,
    legend=dict(
        x=0.98,
        y=0.98,
        xanchor='left',
        yanchor='top',
        traceorder='normal',
        bgcolor='rgba(255, 255, 255, 0.5)'
    ),
    paper_bgcolor='white',
    plot_bgcolor='white',
    margin=dict(l=40, r=250, b=40, t=50) # Increased right margin for legend
)

# Determine the output image filename from the input JSON path
if '.' in json_file_path:
    output_filename_base = json_file_path.rsplit('.', 1)[0]
else:
    output_filename_base = json_file_path

output_image_path = f"{output_filename_base}.png"

# Save the figure as a PNG image
fig.write_image(output_image_path, scale=2)

print(f"Chart saved to {output_image_path}")