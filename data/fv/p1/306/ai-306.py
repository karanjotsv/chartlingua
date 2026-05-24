import sys
import json
import os
import plotly.graph_objects as go

# Ensure the script is called with a JSON file path
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]

# Read data from the specified JSON file
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        config = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)

# Extract data and configuration from the JSON object
chart_data = config['chart_data']
texts = config['texts']
colors = config['colors']
style = config.get('style', {})

# Prepare data for Plotly
labels = [d['label'] for d in chart_data]
values = [d['value'] for d in chart_data]
pull_values = style.get('pull', [0] * len(chart_data))
text_colors = style.get('text_colors', ['#000000'] * len(chart_data))

# Create the pie chart trace
# Note: The 3D "extruded" effect of the original is not a standard feature in Plotly.
# This recreation uses a 2D pie chart with an exploded slice to preserve the key data representation.
pie_trace = go.Pie(
    labels=labels,
    values=values,
    marker=dict(colors=colors, line=dict(color='#000000', width=1.5)),
    pull=pull_values,
    textinfo='label+percent',
    textposition='inside',
    textfont=dict(color=text_colors[0]), # Set a default color, will be overridden below if multiple specified
    insidetextorientation='horizontal',
    sort=False  # This is crucial to preserve the original order of slices
)

fig = go.Figure(data=[pie_trace])

# Since text colors vary per slice, we must update the trace's textfont.color array
fig.update_traces(textfont=dict(color=text_colors, size=14))


# Update layout for a professional look and feel
title_text = ""
if texts.get('title'):
    title_text += f"<b>{texts['title']}</b>"
if texts.get('subtitle'):
    title_text += f"<br><sub>{texts['subtitle']}</sub>" if title_text else texts['subtitle']

fig.update_layout(
    title_text=title_text if title_text else None,
    title_x=0.5,
    font=dict(family="Arial"),
    showlegend=False,
    margin=dict(l=20, r=20, t=50, b=100),  # Adjust bottom margin for the source text
    annotations=[
        dict(
            text=texts.get('source', ''),
            showarrow=False,
            xref="paper",
            yref="paper",
            x=0,
            y=-0.1,  # Positioned below the plot area
            xanchor='left',
            yanchor='top',
            align='left',
            font=dict(size=12)
        )
    ]
)

# Generate the output filename from the input JSON path
base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_filename}.png"

# Save the figure as a high-resolution PNG image
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")