import sys
import json
import plotly.graph_objects as go
import os

if len(sys.argv) != 2:
    print("Usage: python script.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]

try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_info = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_path}")
    sys.exit(1)

chart_data = chart_info.get('chart_data', [])
texts = chart_info.get('texts', {})
colors = chart_info.get('colors', [])

# Prepare data for Plotly horizontal bar chart
# The visual order is top-to-bottom, so we reverse the lists for Plotly
categories = [item['category'] for item in chart_data][::-1]
values = [item['value'] for item in chart_data][::-1]
value_suffix = texts.get('value_suffix', '')

fig = go.Figure()

# Add bar trace
fig.add_trace(go.Bar(
    x=values,
    y=categories,
    orientation='h',
    marker_color=colors[0] if colors else '#3577D5',
    text=[f"{v}{value_suffix}" for v in values],
    textposition='outside',
    textfont=dict(color='black', size=12),
    cliponaxis=False
))

# Update layout
fig.update_layout(
    font=dict(family="Arial", size=12),
    plot_bgcolor='white',
    showlegend=False,
    margin=dict(l=120, r=40, t=50, b=60),
    xaxis=dict(
        title=texts.get('x_axis_title'),
        range=[0, max(values) * 1.15],
        showgrid=True,
        gridcolor='#E5E5E5',
        griddash='dot',
        zeroline=False,
        ticksuffix=value_suffix,
        tickfont=dict(size=12)
    ),
    yaxis=dict(
        showline=False,
        ticks='',
        tickfont=dict(size=12)
    )
)

# Add source as an annotation
source_text = texts.get('source')
if source_text:
    fig.add_annotation(
        text=source_text,
        xref="paper", yref="paper",
        x=1, y=-0.1,  # Position at bottom-right, adjusted for margin
        xanchor='right', yanchor='top',
        showarrow=False,
        font=dict(size=10, color='grey')
    )

# Determine output filename and save the image
base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_filename}.png"

fig.write_image(output_filename, scale=2)
print(f"Chart saved as {output_filename}")