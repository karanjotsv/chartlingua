import sys
import json
import os
import plotly.graph_objects as go

# Check for command-line argument
if len(sys.argv) != 2:
    print("Usage: python create_chart.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]

# Check if the JSON file exists
if not os.path.exists(json_path):
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)

# Read data from the specified JSON file
with open(json_path, 'r', encoding='utf-8') as f:
    chart_info = json.load(f)

# Extract data, texts, and colors from the JSON object
chart_data = chart_info['chart_data']
texts = chart_info['texts']
colors = chart_info['colors']

# Prepare data for Plotly
# The data is provided top-to-bottom, but Plotly plots y-axis categories bottom-to-top.
# We reverse the lists to match the original chart's visual order.
categories = [item['category'] for item in chart_data]
values = [item['value'] for item in chart_data]
categories.reverse()
values.reverse()

# Create the figure
fig = go.Figure()

# Add the bar trace
fig.add_trace(go.Bar(
    x=values,
    y=categories,
    orientation='h',
    marker=dict(color=colors[0]),
    hoverinfo='none'
))

# Build title string from JSON data
title_parts = []
if texts.get('title'):
    title_parts.append(f"<span style='font-size: 20px;'><b>{texts['title']}</b></span>")
if texts.get('subtitle'):
    title_parts.append(f"<span style='font-size: 16px;'>{texts['subtitle']}</span>")
final_title = "<br>".join(title_parts)

# Update layout for a clean, professional look
fig.update_layout(
    title=dict(text=final_title, x=0.05, y=0.95, xanchor='left', yanchor='top'),
    font=dict(family="Arial", size=12),
    plot_bgcolor='white',
    paper_bgcolor='white',
    showlegend=False,
    margin=dict(l=160, r=40, t=60, b=50),
    xaxis=dict(
        title_text=texts.get('x_axis_title'),
        showgrid=True,
        gridcolor='#e0e0e0',
        zeroline=False,
        tickformat=',.0f',
        range=[0, 10000000],
        dtick=2000000
    ),
    yaxis=dict(
        title_text=texts.get('y_axis_title'),
        showgrid=False,
        zeroline=False
    )
)

# Add source annotation if it exists
if texts.get('source'):
    fig.add_annotation(
        text=texts['source'],
        xref="paper", yref="paper",
        x=0, y=-0.15,
        xanchor='left', yanchor='top',
        showarrow=False,
        font=dict(size=12)
    )

# Determine output filename from the input JSON filename
base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_filename}.png"

# Save the figure to a high-resolution PNG file
try:
    fig.write_image(output_filename, scale=2)
    print(f"Chart successfully generated and saved to {output_filename}")
except Exception as e:
    print(f"Error saving image: {e}")
    sys.exit(1)