import sys
import json
import os
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print(f"Usage: python {os.path.basename(sys.argv[0])} <json_file_path>")
    sys.exit(1)

json_file_path = sys.argv[1]

with open(json_file_path, 'r', encoding='utf-8') as f:
    config = json.load(f)

chart_data = config['chart_data']
texts = config['texts']
colors = config['colors']

labels = [d['label'] for d in chart_data]
values = [d['value'] for d in chart_data]
pie_text = [f"{d['label']}<br>{d['value']}%" for d in chart_data]

fig = go.Figure(data=[go.Pie(
    labels=labels,
    values=values,
    text=pie_text,
    textinfo='text',
    textfont=dict(
        family="Arial",
        size=14,
        color='white'
    ),
    marker=dict(
        colors=colors
    ),
    hole=0,
    sort=False,
    direction='clockwise'
)])

title_text = f"<b>{texts['title']}</b>"

fig.update_layout(
    title_text=title_text,
    title_x=0.5,
    font=dict(
        family="Arial"
    ),
    showlegend=False,
    margin=dict(t=80, b=40, l=40, r=40),
    paper_bgcolor='white',
    plot_bgcolor='white'
)

base_filename = os.path.splitext(os.path.basename(json_file_path))[0]
output_filename = f"{base_filename}.png"

fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")