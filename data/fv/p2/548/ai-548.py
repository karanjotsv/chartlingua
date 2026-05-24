import sys
import json
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print("Usage: python script.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]

try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_data_json = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_path}")
    sys.exit(1)

fig = go.Figure()

chart_data = chart_data_json.get('chart_data', [])
texts = chart_data_json.get('texts', {})
colors = chart_data_json.get('colors', {})
layout_options = chart_data_json.get('layout_options', {})

primary_color = colors.get('primary', '#000000')

for trace_data in chart_data:
    fig.add_trace(go.Scatter(
        x=trace_data['x'],
        y=trace_data['y'],
        mode=trace_data['mode'],
        line=dict(color=primary_color, dash=trace_data['line_style']),
        marker=dict(color=primary_color, size=5),
        showlegend=False
    ))

# Combine title and subtitle
title_text = texts.get('title', '')
if texts.get('subtitle'):
    title_text += f"<br><sub>{texts['subtitle']}</sub>"

# Combine source and note
source_text = ""
if texts.get('source'):
    source_text += texts['source']
if texts.get('note'):
    source_text += f"<br>{texts['note']}"

fig.update_layout(
    title=dict(
        text=title_text,
        x=0.5,
        y=0.95,
        xanchor='center',
        yanchor='top'
    ),
    xaxis_title=texts.get('x_axis_title', ''),
    yaxis_title=dict(text=texts.get('y_axis_title', ''), standoff=10),
    font=dict(
        family="Arial",
        size=12,
        color=primary_color
    ),
    plot_bgcolor=colors.get('background', '#FFFFFF'),
    paper_bgcolor=colors.get('background', '#FFFFFF'),
    showlegend=False,
    margin=dict(l=60, r=40, t=90, b=80),
    xaxis=dict(
        showline=True,
        linewidth=1,
        linecolor=primary_color,
        mirror=True,
        showgrid=False,
        **layout_options.get('xaxis', {})
    ),
    yaxis=dict(
        showline=True,
        linewidth=1,
        linecolor=primary_color,
        mirror=True,
        showgrid=True,
        gridcolor=colors.get('grid', '#E0E0E0'),
        **layout_options.get('yaxis', {})
    )
)

# Add shapes from layout options
shapes = []
for shape_data in layout_options.get('shapes', []):
    shape_data['line']['color'] = primary_color
    shapes.append(go.layout.Shape(**shape_data))
fig.update_layout(shapes=shapes)

# Add annotations
annotations = []
for anno_data in texts.get('annotations', []):
    annotations.append(go.layout.Annotation(**anno_data))
fig.update_layout(annotations=annotations)

# Add source/note text as a separate annotation
if source_text:
    fig.add_annotation(
        text=source_text,
        xref="paper", yref="paper",
        x=0, y=-0.2,  # Adjust this value based on text length
        xanchor='left', yanchor='top',
        showarrow=False,
        align='left'
    )


output_filename = json_path.rsplit('.', 1)[0] + '.png'
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")