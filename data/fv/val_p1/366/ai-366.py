import sys
import json
import plotly.graph_objects as go
from pathlib import Path

# Check for command-line argument
if len(sys.argv) != 2:
    print("Usage: python create_chart.py <path_to_json_file>")
    sys.exit(1)

json_path_str = sys.argv[1]
json_path = Path(json_path_str)

# Ensure the JSON file exists
if not json_path.is_file():
    print(f"Error: JSON file not found at {json_path_str}")
    sys.exit(1)

# Read data from the specified JSON file
with open(json_path, 'r', encoding='utf-8') as f:
    chart_data = json.load(f)

# Extract data for plotting, preserving order
categories = [d['category'] for d in chart_data['chart_data']]
values = [d['value'] for d in chart_data['chart_data']]
texts_dict = chart_data['texts']
bar_color = chart_data['colors'][0]

# Create the figure
fig = go.Figure()

# Add the bar trace
fig.add_trace(go.Bar(
    x=categories,
    y=values,
    text=values,
    textposition='outside',
    marker_color=bar_color,
    marker_line_width=0,
    textfont=dict(
        family="Arial",
        size=12,
        color='black'
    ),
    cliponaxis=False,  # Prevents text labels from being clipped
    hoverinfo='none'
))

# Combine title and subtitle using HTML for styling
title_text = (
    f"<span style='font-size: 26px; color: #D9531E;'><b>{texts_dict['title']}</b></span>"
    f"<br><span style='font-size: 18px; color: #C00000;'>{texts_dict['subtitle']}</span>"
)

# Update layout for a clean, accurate appearance
fig.update_layout(
    title=dict(
        text=title_text,
        y=0.95,
        x=0.5,
        xanchor='center',
        yanchor='top'
    ),
    xaxis=dict(
        title_text=texts_dict['x_axis_title'],
        showgrid=False,
        showline=True,
        linecolor='darkgrey',
        linewidth=1,
        zeroline=False,
        tickfont=dict(family="Arial", size=12)
    ),
    yaxis=dict(
        title_text=texts_dict['y_axis_title'],
        visible=False,  # Hide y-axis line, ticks, and labels
        range=[0, max(values) * 1.2] # Ensure space for text above the highest bar
    ),
    plot_bgcolor='white',
    paper_bgcolor='white',
    showlegend=False,
    font=dict(
        family="Arial"
    ),
    margin=dict(t=120, b=60, l=40, r=40),
    bargap=0.5
)

# Determine output filename from the input JSON filename
output_filename = json_path.with_suffix(".png")

# Save the figure as a high-resolution PNG image
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")