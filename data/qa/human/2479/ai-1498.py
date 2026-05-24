import sys
import json
import plotly.graph_objects as go
import pathlib

if len(sys.argv) != 2:
    print(f"Usage: python {sys.argv[0]} <json_file_path>")
    sys.exit(1)

json_file_path = pathlib.Path(sys.argv[1])
output_image_path = json_file_path.with_suffix('.png')

with open(json_file_path, 'r', encoding='utf-8') as f:
    chart_info = json.load(f)

data = chart_info['chart_data']
texts = chart_info['texts']
colors = chart_info['colors']

labels = [item['label'] for item in data]
values = [item['value'] for item in data]

trace = go.Pie(
    labels=labels,
    values=values,
    marker=dict(colors=colors, line=dict(color='#FFFFFF', width=2)),
    texttemplate='%{label} %{value}%',
    textposition='outside',
    sort=False,
    direction='clockwise',
    showlegend=False
)

title_text = ""
if texts.get('title') and texts.get('subtitle'):
    title_text = f"<b>{texts['title']}</b><br>{texts['subtitle']}"
elif texts.get('title'):
    title_text = f"<b>{texts['title']}</b>"
elif texts.get('subtitle'):
    title_text = texts['subtitle']

annotations = []
if texts.get('source'):
    annotations.append(
        dict(
            text=texts['source'],
            showarrow=False,
            xref="paper",
            yref="paper",
            x=0.98,
            y=-0.1,
            xanchor='right',
            yanchor='top',
            align='right',
            font=dict(size=10, color="grey")
        )
    )

layout = go.Layout(
    title_text=title_text,
    title_x=0.05,
    title_xanchor='left',
    font=dict(family="Arial"),
    margin=dict(t=60, b=80, l=60, r=60),
    paper_bgcolor='white',
    plot_bgcolor='white',
    annotations=annotations,
    uniformtext_minsize=10,
    uniformtext_mode='hide'
)

fig = go.Figure(data=[trace], layout=layout)

fig.write_image(output_image_path, scale=2)

print(f"Chart saved to {output_image_path}")