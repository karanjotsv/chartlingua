import sys
import json
import os
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print("Usage: python create_chart.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]

try:
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
except FileNotFoundError:
    print(f"Error: File not found at {json_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Invalid JSON format in {json_path}")
    sys.exit(1)

chart_data = data['chart_data']
texts = data['texts']
colors = data['colors']

categories = [item['category'] for item in chart_data]
values = [item['value'] for item in chart_data]

color_iter = iter(colors)
bar_colors = [next(color_iter) if v > 0 else 'rgba(0,0,0,0)' for v in values]

fig = go.Figure()

fig.add_trace(go.Bar(
    x=categories,
    y=values,
    marker_color=bar_colors,
    width=0.6
))

annotations = []
for item in chart_data:
    if item.get('label') and item.get('value', 0) > 0:
        annotations.append(
            go.layout.Annotation(
                x=item['category'],
                y=item['value'],
                text=item['label'],
                showarrow=False,
                font=dict(family="Arial", size=10, color='#3D3D3D'),
                align='center',
                xanchor='center',
                yanchor='bottom',
                yshift=5,
                bgcolor='rgba(230, 230, 230, 0.85)',
                borderpad=3
            )
        )

fig.update_layout(
    title=dict(
        text=texts['title'],
        y=0.95,
        x=0.5,
        xanchor='center',
        yanchor='top',
        font=dict(size=14)
    ),
    xaxis=dict(
        showgrid=False,
        showline=True,
        linecolor='black',
        zeroline=False,
        tickfont=dict(size=10)
    ),
    yaxis=dict(
        range=[0, 6.1],
        tickmode='linear',
        tick0=0,
        dtick=1,
        showgrid=True,
        gridcolor='#D3D3D3',
        gridwidth=1,
        showline=True,
        linecolor='black',
        zeroline=False
    ),
    font=dict(family="Arial"),
    plot_bgcolor='white',
    paper_bgcolor='white',
    showlegend=False,
    margin=dict(t=100, b=120, l=40, r=40),
    annotations=annotations
)

base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_image_path = f"{base_filename}.png"

fig.write_image(output_image_path, scale=2)

print(f"Chart saved to {output_image_path}")