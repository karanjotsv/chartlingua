import sys
import json
import plotly.graph_objects as go
import os

if len(sys.argv) != 2:
    print("Usage: python <script_name>.py <path_to_json>")
    sys.exit(1)

json_file_path = sys.argv[1]

with open(json_file_path, 'r', encoding='utf-8') as f:
    config = json.load(f)

chart_data = config['chart_data']
texts = config['texts']
colors = config['colors']

labels = [item['label'] for item in chart_data]
values = [item['value'] for item in chart_data]
slice_text = [item['text'] for item in chart_data]

fig = go.Figure()

fig.add_trace(go.Pie(
    labels=labels,
    values=values,
    text=slice_text,
    textinfo='text',
    textposition='inside',
    insidetextorientation='horizontal',
    marker=dict(
        colors=colors,
        line=dict(color='#000000', width=1.5)
    ),
    hoverinfo='label+percent',
    sort=False,
    direction='clockwise',
    rotation=105
))

title_text = texts['title']
if texts.get('subtitle'):
    title_text += f"<br><sub>{texts['subtitle']}</sub>"

fig.update_layout(
    title=dict(
        text=title_text,
        y=0.95,
        x=0.5,
        xanchor='center',
        yanchor='top',
        font=dict(size=22)
    ),
    font=dict(
        family="Arial",
        size=14
    ),
    legend=dict(
        orientation="v",
        yanchor="top",
        y=0.8,
        xanchor="left",
        x=1.0,
        itemsizing='constant',
        font=dict(size=14)
    ),
    margin=dict(l=40, r=320, t=100, b=40),
    showlegend=True
)

fig.update_traces(
    textfont=dict(
        family="Arial",
        size=14,
        color='black'
    )
)

base_filename = os.path.splitext(os.path.basename(json_file_path))[0]
output_filename = f"{base_filename}.png"

fig.write_image(output_filename, scale=2, width=800, height=600)

print(f"Chart saved to {output_filename}")