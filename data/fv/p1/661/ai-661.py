import sys
import json
import os
import plotly.graph_objects as go

json_path = sys.argv[1]

with open(json_path, 'r', encoding='utf-8') as f:
    config = json.load(f)

chart_data = config['chart_data']
texts = config['texts']
colors = config['colors']

x_values = [d['category'] for d in chart_data]
y_values = [d['value'] for d in chart_data]

fig = go.Figure()

fig.add_trace(go.Bar(
    x=x_values,
    y=y_values,
    marker_color=colors[0],
    showlegend=False
))

title_text = texts.get('title', '')
if texts.get('subtitle'):
    title_text += f"<br><sub>{texts['subtitle']}</sub>"

source_parts = []
if texts.get('source'):
    source_parts.append(texts['source'])
if texts.get('note'):
    source_parts.append(texts['note'])
annotation_text = "<br>".join(source_parts)

fig.update_layout(
    title={
        'text': title_text,
        'y': 0.95,
        'x': 0.5,
        'xanchor': 'center',
        'yanchor': 'top',
        'font': {'size': 20}
    },
    xaxis_title=texts.get('x_axis_title'),
    yaxis_title=texts.get('y_axis_title'),
    font=dict(family="Arial", size=14),
    plot_bgcolor='white',
    xaxis=dict(
        categoryorder='array',
        categoryarray=x_values,
        showline=True,
        linewidth=1,
        linecolor='black',
        ticks='outside',
        showgrid=False
    ),
    yaxis=dict(
        range=[0, 35],
        dtick=5,
        showline=True,
        linewidth=1,
        linecolor='black',
        ticks='outside',
        showgrid=True,
        gridcolor='#C0C0C0'
    ),
    margin=dict(l=90, r=40, b=80, t=100)
)

if annotation_text:
    fig.add_annotation(
        text=annotation_text,
        xref="paper", yref="paper",
        x=0, y=-0.2,
        showarrow=False,
        align="left",
        xanchor="left",
        yanchor="top",
        font=dict(size=12)
    )

base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_filename}.png"

fig.write_image(output_filename, scale=2)