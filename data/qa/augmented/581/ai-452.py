import sys
import json
import pathlib
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print("Usage: python script.py <path_to_json_file>")
    sys.exit(1)

json_path = pathlib.Path(sys.argv[1])
if not json_path.is_file():
    print(f"Error: JSON file not found at '{json_path}'")
    sys.exit(1)

with open(json_path, 'r', encoding='utf-8') as f:
    chart_data = json.load(f)

data = chart_data['chart_data']
texts = chart_data['texts']
colors = chart_data['colors']

categories = [item['category'] for item in data]
values = [item['value'] for item in data]

fig = go.Figure()

fig.add_trace(go.Bar(
    x=categories,
    y=values,
    marker_color=colors[0],
    text=[f'{v:.1f}%' for v in values],
    textposition='outside',
    cliponaxis=False,
    textfont=dict(
        family="Arial",
        size=12,
        color='black'
    )
))

annotations = []
if texts.get('note'):
    annotations.append(dict(
        xref='paper', yref='paper',
        x=0, y=-0.15,
        xanchor='left', yanchor='top',
        text=texts['note'],
        showarrow=False,
        font=dict(family="Arial", size=12, color=colors[0])
    ))

if texts.get('source'):
    annotations.append(dict(
        xref='paper', yref='paper',
        x=1, y=-0.15,
        xanchor='right', yanchor='top',
        text=texts['source'],
        showarrow=False,
        font=dict(family="Arial", size=12, color='#666666')
    ))

fig.update_layout(
    font_family="Arial",
    plot_bgcolor='white',
    paper_bgcolor='white',
    showlegend=False,
    bargap=0.35,
    margin=dict(l=80, r=20, t=50, b=100),
    xaxis=dict(
        showgrid=True,
        gridcolor='#f0f0f0',
        linecolor='black',
        tickfont=dict(size=12)
    ),
    yaxis=dict(
        title=texts['y_axis_title'],
        range=[0, 60],
        dtick=10,
        ticksuffix='%',
        showgrid=True,
        gridcolor='#dddddd',
        griddash='dot',
        zeroline=False,
        tickfont=dict(size=12)
    ),
    annotations=annotations
)

output_filename = f"{json_path.stem}.png"
fig.write_image(output_filename, scale=2)
print(f"Chart saved as {output_filename}")