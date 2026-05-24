import sys
import json
import pathlib
import plotly.graph_objects as go

# Ensure a JSON file path is provided as a command-line argument
if len(sys.argv) != 2:
    print("Usage: python create_chart.py <path_to_json_file>")
    sys.exit(1)

# Define file paths from the command-line argument
json_path = pathlib.Path(sys.argv[1])
if not json_path.is_file():
    print(f"Error: File not found at {json_path}")
    sys.exit(1)
output_path = json_path.with_suffix(".png")

# Load data and configuration from the JSON file
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        config = json.load(f)
except json.JSONDecodeError:
    print(f"Error: Invalid JSON format in {json_path}")
    sys.exit(1)

# Extract data for plotting
chart_data = config.get('chart_data', [])
texts = config.get('texts', {})
colors = config.get('colors', [])

labels = [item.get('category', '') for item in chart_data]
values = [item.get('value', 0) for item in chart_data]

# Create the pie chart trace
pie_trace = go.Pie(
    labels=labels,
    values=values,
    marker=dict(colors=colors, line=dict(color='#ffffff', width=2)),
    texttemplate='%{label} %{value}%',
    textposition='outside',
    hoverinfo='label+percent',
    sort=False,  # Preserve the original data order
    direction='clockwise'
)

# Initialize the figure
fig = go.Figure(data=[pie_trace])

# Combine title and subtitle
title_text = texts.get('title') or ''
subtitle_text = texts.get('subtitle') or ''
if subtitle_text:
    title_text = f"<b>{title_text}</b><br><sub>{subtitle_text}</sub>"
else:
    title_text = f"<b>{title_text}</b>"
    
# Combine source and note for annotation
source_text = texts.get('source') or ''
note_text = texts.get('note') or ''
if note_text:
    source_text = f"{source_text}<br>{note_text}"

annotations = []
if source_text:
    annotations.append(
        go.layout.Annotation(
            text=source_text,
            xref="paper",
            yref="paper",
            x=0.99,
            y=-0.1,
            xanchor='right',
            yanchor='top',
            showarrow=False,
            font=dict(family="Arial", size=10, color="grey")
        )
    )

# Configure the layout
fig.update_layout(
    title_text=title_text,
    title_x=0.5,
    showlegend=False,
    font=dict(family="Arial", size=14),
    margin=dict(l=100, r=100, t=50, b=50), # Add margins to prevent label clipping
    paper_bgcolor='white',
    plot_bgcolor='white',
    annotations=annotations
)

# Write the output image file
fig.write_image(output_path, scale=2)

print(f"Chart saved to {output_path}")