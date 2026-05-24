import sys
import json
import pathlib
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print(f"Usage: python {pathlib.Path(__file__).name} <json_file_path>", file=sys.stderr)
    sys.exit(1)

json_path = sys.argv[1]

with open(json_path, 'r', encoding='utf-8') as f:
    chart_info = json.load(f)

chart_data = chart_info['chart_data']
texts = chart_info['texts']
colors = chart_info['colors']

categories = [item['category'] for item in chart_data][::-1]
values = [item['value'] for item in chart_data][::-1]
text_labels = [f"{v:,}".replace(",", " ") for v in values]

fig = go.Figure()

fig.add_trace(go.Bar(
    y=categories,
    x=values,
    orientation='h',
    marker=dict(color=colors[0]),
    text=text_labels,
    textposition='outside',
    cliponaxis=False,
    textfont=dict(family="Arial", size=12, color='black')
))

title_components = []
if texts.get('title'):
    title_components.append(f"<b>{texts['title']}</b>")
if texts.get('subtitle'):
    title_components.append(f"<sub>{texts['subtitle']}</sub>")
title_text = "<br>".join(title_components)

source_note_components = []
if texts.get('source'):
    source_note_components.append(texts['source'])
if texts.get('note'):
    source_note_components.append(texts['note'])
source_note_text = "<br>".join(source_note_components)

fig.update_layout(
    title_text=title_text if title_text else None,
    font=dict(family="Arial", size=12, color='#444444'),
    plot_bgcolor='white',
    paper_bgcolor='white',
    showlegend=False,
    xaxis=dict(
        title=texts.get('x_axis_title'),
        showgrid=True,
        gridcolor='#EAEAEA',
        zeroline=False,
        showline=False,
        range=[0, max(values) * 1.15]
    ),
    yaxis=dict(
        title=texts.get('y_axis_title'),
        showgrid=False,
        zeroline=False,
        showline=False,
    ),
    margin=dict(l=130, r=60, b=80, t=50),
    annotations=[
        dict(
            text=source_note_text,
            showarrow=False,
            xref='paper', yref='paper',
            x=1, y=-0.18,
            xanchor='right', yanchor='top',
            align='right',
            font=dict(family="Arial", size=12, color='#888888')
        )
    ]
)

output_filename = f"{pathlib.Path(json_path).stem}.png"
fig.write_image(output_filename, scale=2)
print(f"Chart saved to {output_filename}")