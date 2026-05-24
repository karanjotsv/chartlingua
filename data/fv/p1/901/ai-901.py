import sys
import json
import pathlib
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print("Usage: python create_chart.py <path_to_json_file>")
    sys.exit(1)

json_path = pathlib.Path(sys.argv[1])
if not json_path.is_file():
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)

with open(json_path, 'r', encoding='utf-8') as f:
    chart_data = json.load(f)

fig = go.Figure()

# Add traces from JSON data
for i, series in enumerate(chart_data['chart_data']):
    fig.add_trace(go.Scatter(
        x=series['x'],
        y=series['y'],
        mode='lines',
        name=series['name'],
        line=dict(
            color=chart_data['colors'][i],
            dash=series['style']
        ),
        hoverinfo='none'
    ))

# Update layout
texts = chart_data['texts']
title_text = f"{texts['title']}<br><sub>{texts['subtitle']}</sub>" if texts['title'] and texts['subtitle'] else texts.get('title')

fig.update_layout(
    font_family="Arial",
    title_text=title_text,
    xaxis_title=texts['x_axis_title'],
    yaxis_title=texts['y_axis_title'],
    plot_bgcolor='white',
    showlegend=False,
    margin=dict(l=80, r=40, t=50, b=80),
    xaxis=dict(
        range=[0, 0.0105],
        tickmode='linear',
        dtick=0.001,
        showline=True,
        linewidth=1,
        linecolor='black',
        mirror=True,
        gridcolor=None,
        zeroline=False,
        ticks='outside'
    ),
    yaxis=dict(
        range=[0, 2.5],
        tickvals=[0, 0.5, 1, 1.5, 2, 2.5],
        ticktext=['0', '0,5', '1', '1,5', '2', '2,5'],
        showline=True,
        linewidth=1,
        linecolor='black',
        mirror=True,
        gridcolor='lightgrey',
        zeroline=False,
        ticks='outside'
    )
)

# Add annotations
if 'annotations' in chart_data:
    for ann in chart_data['annotations']:
        fig.add_annotation(ann)

# Add shapes
if 'shapes' in chart_data:
    for shape in chart_data['shapes']:
        fig.add_shape(shape)

# Generate output image
output_filename = json_path.with_suffix('.png')
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")