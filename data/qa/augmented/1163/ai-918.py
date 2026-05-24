import sys
import json
import plotly.graph_objects as go
from pathlib import Path

if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <json_file_path>")
    sys.exit(1)

json_file_path = Path(sys.argv[1])
if not json_file_path.is_file():
    print(f"Error: JSON file not found at {json_file_path}")
    sys.exit(1)

with open(json_file_path, 'r', encoding='utf-8') as f:
    chart_info = json.load(f)

chart_data = chart_info['chart_data']
texts = chart_info['texts']
colors = chart_info['colors']

x_values = [item['x'] for item in chart_data]
y_values = [item['y'] for item in chart_data]

fig = go.Figure()

fig.add_trace(go.Bar(
    x=x_values,
    y=y_values,
    marker_color=colors[0],
    text=[f'{y:.2f}'.rstrip('0').rstrip('.') for y in y_values],
    textposition='outside',
    cliponaxis=False,
    textfont=dict(family="Arial", size=12, color='black')
))

shapes = []
for i, x_val in enumerate(x_values):
    if i % 2 != 0:
        shapes.append(
            go.layout.Shape(
                type="rect",
                xref="x",
                yref="paper",
                x0=i - 0.5,
                x1=i + 0.5,
                y0=0,
                y1=1,
                fillcolor="#F8F8F8",
                layer="below",
                line_width=0,
            )
        )

annotations = []
if texts.get('note'):
    annotations.append(dict(
        xref='paper', yref='paper',
        x=0.0, y=-0.15,
        xanchor='left', yanchor='top',
        text=f'<span style="color:#007bff;">ⓘ</span> {texts["note"]}',
        showarrow=False,
        font=dict(family="Arial", size=12, color="#007bff")
    ))
if texts.get('source'):
    annotations.append(dict(
        xref='paper', yref='paper',
        x=1.0, y=-0.15,
        xanchor='right', yanchor='top',
        text=texts['source'],
        showarrow=False,
        font=dict(family="Arial", size=12, color='#666666')
    ))

fig.update_layout(
    font=dict(family="Arial"),
    plot_bgcolor='white',
    showlegend=False,
    xaxis=dict(
        title_text=texts['x_axis_title'],
        showgrid=False,
        zeroline=False,
        linecolor='lightgrey'
    ),
    yaxis=dict(
        title_text=texts['y_axis_title'],
        range=[0, 25],
        gridcolor='#EAEAEA',
        zeroline=False,
        showline=False
    ),
    margin=dict(t=50, r=20, b=100, l=90),
    shapes=shapes,
    annotations=annotations,
    bargap=0.35
)

output_filename = json_file_path.stem + '.png'
fig.write_image(output_filename, scale=2)
print(f"Chart saved to {output_filename}")