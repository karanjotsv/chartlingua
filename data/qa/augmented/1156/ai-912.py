import sys
import json
import os
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print("Usage: python recreate_chart.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]

if not os.path.exists(json_path):
    print(f"Error: File not found at {json_path}")
    sys.exit(1)

with open(json_path, 'r', encoding='utf-8') as f:
    config = json.load(f)

chart_data = config['chart_data']
texts = config['texts']
colors = config['colors']

categories = [item['category'] for item in chart_data]
values = [item['value'] for item in chart_data]

text_labels = []
for v in values:
    if v == int(v):
        label = f"{int(v):,}".replace(",", " ")
    else:
        label = f"{v:,.2f}".replace(",", " ").rstrip('0').rstrip('.')
    text_labels.append(label)

fig = go.Figure()

fig.add_trace(go.Bar(
    y=categories,
    x=values,
    orientation='h',
    marker=dict(color=colors),
    text=text_labels,
    textposition='outside',
    textfont=dict(
        family="Arial",
        size=12,
        color='black'
    ),
    cliponaxis=False
))

title_text = ""
if texts.get('title') and texts.get('subtitle'):
    title_text = f"<b>{texts['title']}</b><br>{texts['subtitle']}"
elif texts.get('title'):
    title_text = f"<b>{texts['title']}</b>"
elif texts.get('subtitle'):
    title_text = texts['subtitle']

fig.update_layout(
    title={
        'text': title_text,
        'y': 0.95,
        'x': 0.5,
        'xanchor': 'center',
        'yanchor': 'top'
    },
    xaxis=dict(
        title=texts.get('x_axis_title', ''),
        showgrid=True,
        gridcolor='#E5E5E5',
        gridwidth=1,
        zeroline=False,
        dtick=2000,
        range=[0, 14500]
    ),
    yaxis=dict(
        showgrid=False,
        zeroline=False
    ),
    plot_bgcolor='white',
    paper_bgcolor='white',
    font=dict(
        family="Arial",
        size=12,
        color="black"
    ),
    showlegend=False,
    margin=dict(l=150, r=80, t=40, b=60),
)

if texts.get('source'):
    fig.add_annotation(
        text=texts['source'],
        align='left',
        showarrow=False,
        xref='paper',
        yref='paper',
        x=0,
        y=-0.15,
        xanchor='left',
        yanchor='top'
    )

base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_filename}.png"

fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")