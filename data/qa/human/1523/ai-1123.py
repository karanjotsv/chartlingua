import sys
import json
import os
import plotly.graph_objects as go

# Check for command-line argument
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <json_file_path>")
    sys.exit(1)

json_path = sys.argv[1]

# Read data from the specified JSON file
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_config = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_path}")
    sys.exit(1)

# Extract data and texts from the JSON structure
chart_data = chart_config.get('chart_data', [])
texts = chart_config.get('texts', {})
colors = chart_config.get('colors', [])

# Prepare data for Plotly
# The order is reversed to match the visual top-to-bottom presentation of the original chart
categories = [item['category'] for item in reversed(chart_data)]
values = [item['value'] for item in reversed(chart_data)]
bar_colors = list(reversed(colors))
bar_labels = [f"{item['value']:.2f}% ({item['year']})" for item in reversed(chart_data)]

# Create the figure
fig = go.Figure()

# Add the bar trace
fig.add_trace(go.Bar(
    y=categories,
    x=values,
    orientation='h',
    marker=dict(color=bar_colors),
    text=bar_labels,
    textposition='outside',
    textfont=dict(family="Arial", size=12, color='#333333'),
    hoverinfo='none',
    cliponaxis=False
))

# Combine title and subtitle using HTML for styling
title_text = f"<b>{texts.get('title', '')}</b><br><span style='font-size: 14px; color: #7f7f7f;'>{texts.get('subtitle', '')}</span>"

# Update layout for a clean, professional look
fig.update_layout(
    title=dict(
        text=title_text,
        x=0.01,
        y=0.95,
        xanchor='left',
        yanchor='top'
    ),
    font=dict(family="Arial", size=12),
    xaxis=dict(
        title_text=texts.get('x_axis_title'),
        showticklabels=True,
        ticksuffix='%',
        showgrid=True,
        gridcolor='#e5e5e5',
        zeroline=False,
        range=[0, max(values) * 1.15] # Add padding to the right
    ),
    yaxis=dict(
        title_text=texts.get('y_axis_title'),
        showgrid=False,
        zeroline=False,
        showline=False,
        ticks='outside',
        ticklen=8
    ),
    plot_bgcolor='white',
    paper_bgcolor='white',
    showlegend=False,
    margin=dict(l=200, r=90, t=110, b=80)
)

# Add source and note annotations
fig.add_annotation(
    text=texts.get('source', ''),
    xref="paper", yref="paper",
    x=0, y=-0.12,
    xanchor='left', yanchor='top',
    showarrow=False,
    font=dict(size=12, color="#7f7f7f")
)
fig.add_annotation(
    text=texts.get('note', ''),
    xref="paper", yref="paper",
    x=1, y=-0.12,
    xanchor='right', yanchor='top',
    showarrow=False,
    font=dict(size=12, color="#7f7f7f")
)


# Determine output filename from the input JSON filename
base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_image_path = f"{base_filename}.png"

# Save the figure as a high-resolution PNG image
fig.write_image(output_image_path, scale=2)

print(f"Chart saved to {output_image_path}")