import sys
import json
import plotly.graph_objects as go
import pathlib

# --- 1. Load Data ---
# Ensure a JSON file path is provided as a command-line argument
if len(sys.argv) != 2:
    print(f"Usage: python {pathlib.Path(__file__).name} <json_file_path>")
    sys.exit(1)

json_path = pathlib.Path(sys.argv[1])
if not json_path.is_file():
    print(f"Error: File not found at {json_path}")
    sys.exit(1)

# Load the chart data and settings from the specified JSON file
with open(json_path, 'r', encoding='utf-8') as f:
    config = json.load(f)

chart_data = config.get('chart_data', [])
texts = config.get('texts', {})
colors = config.get('colors', [])

# --- 2. Create Chart ---
# Extract labels and values, preserving the order from the JSON
labels = [item['label'] for item in chart_data]
values = [item['value'] for item in chart_data]

# Create the Pie chart trace
# The texttemplate is crafted to match the original's format " - Label Value%"
fig = go.Figure(data=[go.Pie(
    labels=labels,
    values=values,
    marker=dict(colors=colors, line=dict(color='#FFFFFF', width=2)),
    texttemplate=" - %{label} %{value}%",
    textposition='outside',
    sort=False,  # Preserve the original data order
    hoverinfo='label+percent'
)])

# --- 3. Configure Layout ---
# Combine title and subtitle using HTML for rich text formatting
title_text = texts.get('title')
subtitle_text = texts.get('subtitle')
full_title = ""
if title_text:
    full_title = f"<b>{title_text}</b>"
    if subtitle_text:
        full_title += f"<br><sub>{subtitle_text}</sub>"

# Apply layout settings for a clean and accurate recreation
fig.update_layout(
    title_text=full_title,
    title_x=0.5, # Center the title
    showlegend=False,
    font=dict(family="Arial", size=14),
    paper_bgcolor='white',
    plot_bgcolor='white',
    # Adjust margins to prevent labels or annotations from being cut off
    margin=dict(t=60, b=80, l=40, r=40),
    annotations=[
        # Source annotation (bottom-right)
        dict(
            text=texts.get('source', ''),
            align='right',
            showarrow=False,
            xref='paper',
            yref='paper',
            x=0.98,
            y=0.01,
            xanchor='right',
            yanchor='bottom',
            font=dict(size=12)
        ),
        # Note annotation (bottom-left)
        dict(
            text=texts.get('note', ''),
            align='left',
            showarrow=False,
            xref='paper',
            yref='paper',
            x=0.02,
            y=0.01,
            xanchor='left',
            yanchor='bottom',
            font=dict(size=12, color="#2471D1")
        )
    ]
)

# --- 4. Output Image ---
# Derive the output filename from the input JSON filename
output_filename = json_path.with_suffix('.png')

# Save the figure to a high-resolution PNG file
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")