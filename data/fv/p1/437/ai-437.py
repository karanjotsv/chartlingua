import sys
import json
import pathlib
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <json_file_path>")
    sys.exit(1)

json_path = pathlib.Path(sys.argv[1])
if not json_path.is_file():
    print(f"Error: JSON file not found at '{json_path}'")
    sys.exit(1)

output_path = json_path.with_suffix('.png')

with open(json_path, 'r', encoding='utf-8') as f:
    chart_json = json.load(f)

chart_data = chart_json['chart_data']
texts = chart_json['texts']
colors = chart_json['colors']

categories = [item['category'] for item in chart_data]
values = [item['value'] for item in chart_data]

fig = go.Figure()

# Add bar trace, showing text only for non-zero values
fig.add_trace(go.Bar(
    x=categories,
    y=values,
    marker_color=colors,
    text=[f'<b>{v}%</b>' if v > 0 else '' for v in values],
    textposition='outside',
    textfont=dict(family="Arial", size=14, color='black'),
    cliponaxis=False
))

# Add annotations for zero-value labels for precise placement
annotations = []
for item in chart_data:
    if item['value'] == 0:
        annotations.append(
            go.layout.Annotation(
                x=item['category'],
                y=0,
                text='<b>0%</b>',
                showarrow=False,
                font=dict(family="Arial", size=14, color='black'),
                xanchor='center',
                yanchor='bottom',
                yshift=5 
            )
        )

fig.update_layout(
    title_text=texts['title'],
    title_x=0.5,
    title_y=0.95,
    title_font=dict(family="Arial", size=18),
    font=dict(family="Arial", size=12, color='black'),
    yaxis=dict(
        range=[0, 101],
        tickvals=[i for i in range(0, 101, 10)],
        ticktext=[f'{i}%' for i in range(0, 101, 10)],
        showgrid=True,
        gridcolor='#e0e0e0',
        zeroline=False,
        title_text=texts.get('y_axis_title')
    ),
    xaxis=dict(
        showgrid=False,
        title_text=texts.get('x_axis_title')
    ),
    plot_bgcolor='white',
    showlegend=False,
    margin=dict(t=100, b=80, l=60, r=40),
    annotations=annotations
)

fig.write_image(str(output_path), scale=2)

print(f"Chart saved to {output_path}")