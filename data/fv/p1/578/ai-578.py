import sys
import json
import os
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print(f"Usage: python {os.path.basename(__file__)} <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]

try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_config = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_path}")
    sys.exit(1)

chart_data = chart_config['chart_data']
texts = chart_config['texts']
colors = chart_config['colors']
shapes = chart_config.get('shapes', [])

years = [d['year'] for d in chart_data]
rates = [d['rate'] for d in chart_data]

bar_colors = [colors['positive'] if r >= 0 else colors['negative'] for r in rates]

fig = go.Figure()

fig.add_trace(go.Bar(
    x=years,
    y=rates,
    marker_color=bar_colors,
    width=0.8
))

fig.update_layout(
    title_text=texts['title'],
    title_x=0.5,
    font=dict(family="Arial", size=12, color="black"),
    xaxis=dict(
        title_text=texts.get('x_axis_title'),
        tickmode='linear',
        tick0=1930,
        dtick=5,
        range=[1928, 2008],
        showgrid=True,
        gridcolor=colors['grid'],
        zeroline=True,
        zerolinewidth=2,
        zerolinecolor='black'
    ),
    yaxis=dict(
        title_text=texts.get('y_axis_title'),
        tickmode='linear',
        tick0=-5,
        dtick=5,
        range=[-5.5, 30.5],
        showgrid=True,
        gridcolor=colors['grid'],
        zeroline=True,
        zerolinewidth=2,
        zerolinecolor='black'
    ),
    plot_bgcolor='white',
    paper_bgcolor='white',
    showlegend=False,
    margin=dict(l=60, r=40, t=80, b=80),
)

for ann in texts.get('annotations', []):
    fig.add_annotation(
        x=ann['x'],
        y=ann['y'],
        text=ann['text'],
        showarrow=False,
        align=ann['align'],
        font=dict(color=ann.get('font_color', 'black'), size=10),
        xanchor='left',
        yanchor='top'
    )

for shape in shapes:
    fig.add_shape(
        type=shape['type'],
        x0=shape['x0'],
        y0=shape['y0'],
        x1=shape['x1'],
        y1=shape['y1'],
        fillcolor=shape.get('fillcolor', colors.get('annotation_shape')),
        opacity=shape.get('opacity', 0.5),
        layer=shape.get('layer', 'below'),
        line=dict(width=shape.get('line_width', 0))
    )

base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_filename}.png"

fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")