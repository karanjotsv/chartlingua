import sys
import json
import os
import plotly.graph_objects as go

# Ensure a JSON file path is provided as a command-line argument
if len(sys.argv) != 2:
    print("Usage: python create_chart.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]

# Check if the provided file path exists
if not os.path.exists(json_path):
    print(f"Error: File not found at {json_path}")
    sys.exit(1)

# Read data from the specified JSON file
with open(json_path, 'r', encoding='utf-8') as f:
    chart_info = json.load(f)

# Extract data, texts, and colors from the JSON structure
chart_data = chart_info.get('chart_data', [])
texts = chart_info.get('texts', {})
colors = chart_info.get('colors', [])

# Prepare data for Plotly
categories = [item['category'] for item in chart_data]
values = [item['value'] for item in chart_data]

# Create the figure object
fig = go.Figure()

# Add the bar trace
fig.add_trace(go.Bar(
    x=categories,
    y=values,
    text=values,
    textposition='outside',
    texttemplate='%{text:.2f}',
    marker_color=colors[0] if colors else None,
    cliponaxis=False  # Prevents text labels from being clipped
))

# Build title and source text using HTML for formatting
title_text = ""
if texts.get("title"):
    title_text += f'<b style="font-size: 20px;">{texts["title"]}</b>'
if texts.get("subtitle"):
    title_text += f'<br><span style="font-size: 14px;">{texts["subtitle"]}</span>'

# Update layout for a professional appearance
fig.update_layout(
    title_text=title_text,
    title_x=0.05,
    title_y=0.95,
    title_font_family="Arial",
    plot_bgcolor='white',
    paper_bgcolor='white',
    font=dict(family="Arial", size=12, color='black'),
    xaxis=dict(
        title_text=texts.get('x_axis_title'),
        showgrid=False,
        showline=True,
        linecolor='lightgrey',
        tickfont=dict(size=12)
    ),
    yaxis=dict(
        title_text=texts.get('y_axis_title'),
        range=[0, 3.5],
        tickmode='linear',
        dtick=0.5,
        gridcolor='lightgrey',
        showline=False,
        tickfont=dict(size=12)
    ),
    showlegend=False,
    margin=dict(l=60, r=40, t=80, b=80),  # Adjust margins to prevent clipping
    annotations=[
        dict(
            text=texts.get('source', ''),
            showarrow=False,
            xref='paper', yref='paper',
            x=1.0, y=-0.15,
            xanchor='right', yanchor='top',
            font=dict(family="Arial", size=10, color='grey')
        )
    ]
)

# Generate the output filename from the input JSON path
base_filename = os.path.splitext(json_path)[0]
output_filename = f"{base_filename}.png"

# Save the figure as a high-resolution PNG image
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")