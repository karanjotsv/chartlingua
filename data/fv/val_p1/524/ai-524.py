import sys
import json
import os
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print(f"Usage: python {os.path.basename(sys.argv[0])} <json_file_path>")
    sys.exit(1)

json_path = sys.argv[1]

if not os.path.exists(json_path):
    print(f"Error: File not found at {json_path}")
    sys.exit(1)

output_filename = os.path.splitext(json_path)[0] + '.png'

with open(json_path, 'r', encoding='utf-8') as f:
    chart_info = json.load(f)

chart_data = chart_info['chart_data']
texts = chart_info['texts']
colors = chart_info['colors']

labels = [d['label'] for d in chart_data]
values = [d['value'] for d in chart_data]

fig = go.Figure()

pie_text_labels = [f"{v:.2f}%" for v in values]

fig.add_trace(go.Pie(
    labels=labels,
    values=values,
    marker=dict(colors=colors, line=dict(color='#000000', width=1)),
    text=pie_text_labels,
    textinfo='text',
    textfont=dict(size=12, color='black'),
    hoverinfo='label+percent',
    sort=False 
))

title_text = texts['title']
if texts.get('subtitle'):
    title_text += f"<br><sup>{texts['subtitle']}</sup>"

fig.update_layout(
    title_text=title_text,
    title_x=0.5,
    font=dict(
        family="Arial",
        size=14
    ),
    margin=dict(t=100, b=60, l=40, r=40),
    showlegend=True,
    legend=dict(
        x=0.8, 
        y=0.7,
        traceorder='normal',
        font=dict(
            family='Arial',
            size=12,
            color='black'
        ),
        bgcolor='rgba(255, 255, 255, 0)',
        bordercolor='rgba(255, 255, 255, 0)'
    )
)

fig.write_image(output_filename, scale=2)