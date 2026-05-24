import sys
import json
import os
import plotly.graph_objects as go

# Check if a command-line argument is provided
if len(sys.argv) != 2:
    print("Usage: python recreate_chart.py <path_to_json_file>")
    sys.exit(1)

json_file_path = sys.argv[1]

# Ensure the specified file exists
if not os.path.exists(json_file_path):
    print(f"Error: JSON file not found at '{json_file_path}'")
    sys.exit(1)

# Load the chart data from the JSON file
with open(json_file_path, 'r', encoding='utf-8') as f:
    config = json.load(f)

# Extract data and texts from the loaded JSON
chart_data = config['chart_data']
texts = config['texts']
colors = config['colors']

# Prepare data for Plotly traces
categories = [d['category'] for d in chart_data]
values = [d['value'] for d in chart_data]

# Create the main figure object
fig = go.Figure()

# Add the main bar trace, hiding the text for zero values to handle it separately
fig.add_trace(go.Bar(
    y=categories,
    x=values,
    orientation='h',
    marker=dict(color=colors[0], line=dict(width=0)),
    text=[v if v != 0 else '' for v in values],
    textposition='inside',
    insidetextanchor='middle',
    insidetextfont=dict(family='Arial', size=14, color='white')
))

# Specifically handle the label for any zero-value bars to match the original's style
if 0 in values:
    zero_indices = [i for i, v in enumerate(values) if v == 0]
    for index in zero_indices:
        fig.add_trace(go.Scatter(
            x=[0],
            y=[categories[index]],
            mode='text',
            text=['0'],
            textposition='middle right',
            textfont=dict(family='Arial', size=14, color='black'),
            showlegend=False
        ))
        
# Combine title and subtitle if they exist
title_text = ""
if texts.get("title"):
    title_text += f"<b>{texts['title']}</b>"
if texts.get("subtitle"):
    title_text += f"<br>{texts['subtitle']}" if title_text else texts['subtitle']

# Configure the chart layout
fig.update_layout(
    title=dict(text=title_text, x=0.05, xanchor='left'),
    xaxis=dict(
        title=texts.get('x_axis_title'),
        showgrid=True,
        gridcolor='#e0e0e0',
        gridwidth=1,
        griddash='dot',
        zeroline=False,
        range=[0, 65],
        dtick=10
    ),
    yaxis=dict(
        title=texts.get('y_axis_title'),
        autorange='reversed',  # Ensures top-to-bottom order matches JSON
        showgrid=False,
        zeroline=False,
        tickfont=dict(size=12)
    ),
    plot_bgcolor='white',
    paper_bgcolor='white',
    font=dict(family="Arial", size=12, color='#000000'),
    margin=dict(l=350, r=40, t=60, b=80), # Generous left margin for long labels
    showlegend=False
)

# Add the source text as an annotation at the bottom right
fig.add_annotation(
    text=texts.get('source'),
    align='left',
    showarrow=False,
    xref='paper',
    yref='paper',
    x=0.99,
    y=-0.12,
    xanchor='right',
    yanchor='top'
)

# Determine the output filename from the input JSON path
base_filename = os.path.splitext(os.path.basename(json_file_path))[0]
output_filename = f"{base_filename}.png"

# Save the figure as a high-resolution PNG image
fig.write_image(output_filename, scale=2)

print(f"Chart saved as {output_filename}")