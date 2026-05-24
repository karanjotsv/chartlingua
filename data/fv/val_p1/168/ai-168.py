import sys
import json
import pathlib
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print(f"Usage: python {sys.argv[0]} <json_file_path>")
    sys.exit(1)

json_file_path = pathlib.Path(sys.argv[1])
if not json_file_path.is_file():
    print(f"Error: File not found at {json_file_path}")
    sys.exit(1)

output_image_path = json_file_path.with_suffix('.png')

with open(json_file_path, 'r', encoding='utf-8') as f:
    config = json.load(f)

chart_data = config['chart_data']
texts = config['texts']
colors = config['colors']

categories = [d['category'] for d in chart_data]
values = [d['value'] for d in chart_data]

fig = go.Figure()

fig.add_trace(go.Bar(
    x=categories,
    y=values,
    marker_color=colors,
    width=0.6
))

for item in chart_data:
    if item.get('annotation'):
        fig.add_annotation(
            x=item['category'],
            y=item['value'],
            text=item['annotation'],
            showarrow=False,
            yshift=12,
            font=dict(family="Arial", size=11, color="black"),
            bgcolor="rgba(220, 220, 220, 0.8)",
            borderpad=3
        )

fig.update_layout(
    title_text=texts.get('title', ''),
    title_x=0.5,
    title_font=dict(family="Arial", size=16),
    paper_bgcolor='white',
    plot_bgcolor='white',
    font=dict(family="Arial", size=12, color="black"),
    showlegend=False,
    xaxis=dict(
        showgrid=False,
        showline=True,
        linewidth=1,
        linecolor='black',
        tickfont=dict(size=11),
        automargin=True
    ),
    yaxis=dict(
        title_text=texts.get('y_axis_title'),
        range=[0, 6],
        tickvals=[0, 1, 2, 3, 4, 5, 6],
        showgrid=True,
        gridcolor='#D3D3D3',
        gridwidth=1,
        zeroline=False,
        showline=True,
        linewidth=1,
        linecolor='black',
        automargin=True
    ),
    margin=dict(t=100, b=120, l=50, r=50)
)

fig.write_image(output_image_path, scale=2, width=900, height=600)

print(f"Chart saved to {output_image_path}")