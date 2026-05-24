import sys
import os
import json
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
with open(json_path, 'r', encoding='utf-8') as f:
    chart_info = json.load(f)

# Extract data for plotting
chart_data = chart_info.get("chart_data", [])
texts = chart_info.get("texts", {})
colors = chart_info.get("colors", [])
x_values = [d['x'] for d in chart_data]
y_values = [d['y'] for d in chart_data]

# Create the figure
fig = go.Figure()

# Add the bar trace
fig.add_trace(go.Bar(
    x=x_values,
    y=y_values,
    text=y_values,
    textposition='outside',
    marker_color=colors[0] if colors else None,
    cliponaxis=False # Allows text to be drawn outside the plotting area
))

# Combine title and subtitle
title_text = texts.get('title') or ''
subtitle_text = texts.get('subtitle') or ''
if subtitle_text:
    title_text = f"<b>{title_text}</b><br>{subtitle_text}"

# Combine source and notes
source_text = texts.get('source') or ''
notes_text = texts.get('notes') or ''
if notes_text:
    source_text = f"{notes_text}<br>{source_text}"

# Update layout
fig.update_layout(
    title=dict(
        text=title_text,
        x=0.05,
        xanchor='left'
    ),
    xaxis=dict(
        title=texts.get('x_axis_title'),
        tickfont=dict(size=12),
        showgrid=True,
        gridcolor='#F0F0F0',
        linecolor='black'
    ),
    yaxis=dict(
        title=texts.get('y_axis_title'),
        range=[0, 52],
        tickvals=[0, 10, 20, 30, 40, 50],
        showgrid=True,
        gridcolor='#E5E5E5'
    ),
    font=dict(
        family="Arial",
        size=12,
        color="black"
    ),
    plot_bgcolor='white',
    paper_bgcolor='white',
    showlegend=False,
    margin=dict(l=60, r=40, t=40, b=120),
    annotations=[
        dict(
            text=source_text,
            showarrow=False,
            xref="paper",
            yref="paper",
            x=0.98,
            y=-0.2, # Adjusted to provide space below axis
            xanchor='right',
            yanchor='top',
            align='right',
            font=dict(size=10, color='#666666')
        )
    ]
)

# Update trace text font
fig.update_traces(textfont_size=12, textfont_family="Arial")

# Define output filename
base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_filename}.png"

# Save the figure as a PNG image
try:
    fig.write_image(output_filename, scale=2)
    print(f"Chart successfully generated and saved as {output_filename}")
except Exception as e:
    print(f"Error saving image: {e}")
    sys.exit(1)