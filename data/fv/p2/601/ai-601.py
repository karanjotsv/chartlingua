import sys
import json
import os
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print(f"Usage: python {os.path.basename(sys.argv[0])} <json_file_path>")
    sys.exit(1)

json_path = sys.argv[1]

try:
    with open(json_path, 'r', encoding='utf-8') as f:
        config = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at '{json_path}'")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from '{json_path}'")
    sys.exit(1)

chart_data = config.get('chart_data', [])
texts = config.get('texts', {})
colors = config.get('colors', [])

labels = [item['category'] for item in chart_data]
values = [item['value'] for item in chart_data]

custom_texts = []
for item in chart_data:
    category = item.get('category', '')
    value = item.get('value', 0)
    if value == 1.9:
        value_str = '1,9%'
    else:
        value_str = f'{value}%'
    custom_texts.append(f'{category}<br>{value_str}')

trace = go.Pie(
    labels=labels,
    values=values,
    hole=0.4,
    marker=dict(colors=colors, line=dict(color='white', width=2)),
    text=custom_texts,
    textinfo='text',
    textposition='outside',
    sort=False,
    direction='clockwise',
    hoverinfo='label+percent',
    textfont=dict(
        family="Arial",
        size=16,
        color='#444444'
    )
)

title_text = ""
if texts.get('title'):
    title_text += f"<b>{texts['title']}</b>"
if texts.get('subtitle'):
    title_text += f"<br><sub>{texts['subtitle']}</sub>"

layout = go.Layout(
    showlegend=False,
    title=dict(
        text=title_text,
        x=0.5,
        font=dict(family="Arial")
    ),
    font=dict(family="Arial"),
    paper_bgcolor='white',
    plot_bgcolor='white',
    margin=dict(l=120, r=120, t=80, b=80)
)

annotations = []
if texts.get('source'):
    annotations.append(
        go.layout.Annotation(
            text=texts['source'],
            align='left',
            showarrow=False,
            xref='paper',
            yref='paper',
            x=0,
            y=-0.15,
            xanchor='left',
            yanchor='top',
            font=dict(family="Arial", size=12, color='#666666')
        )
    )
layout.annotations = annotations

fig = go.Figure(data=[trace], layout=layout)

base_name = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_name}.png"

fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")