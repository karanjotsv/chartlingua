import sys
import json
import pathlib
import plotly.graph_objects as go

if len(sys.argv) != 2:
    sys.exit("Usage: python <script.py> <path_to_json>")

json_path = pathlib.Path(sys.argv[1])

with open(json_path, 'r', encoding='utf-8') as f:
    chart_info = json.load(f)

chart_data = chart_info['chart_data']
texts = chart_info['texts']
colors = chart_info['colors']

labels = [item['label'] for item in chart_data]
values = [item['value'] for item in chart_data]

fig = go.Figure()

fig.add_trace(go.Pie(
    labels=labels,
    values=values,
    marker=dict(colors=colors, line=dict(color='black', width=1)),
    sort=False,
    direction='clockwise',
    hoverinfo='label+percent',
    textinfo='none'
))

title_text = texts.get('title', '')
source_text = texts.get('source', '')

caption_parts = []
if title_text:
    caption_parts.append(f"<b>{title_text}</b>")
if source_text:
    caption_parts.append(source_text)
caption = "<br><br>".join(caption_parts)

fig.update_layout(
    showlegend=True,
    legend=dict(
        x=1.02,
        y=0.95,
        xanchor='left',
        yanchor='top',
        bgcolor='white'
    ),
    font=dict(
        family="Arial"
    ),
    plot_bgcolor='#E5E5E5',
    paper_bgcolor='white',
    margin=dict(l=20, r=20, t=20, b=250),
    annotations=[
        dict(
            text=caption,
            showarrow=False,
            xref="paper",
            yref="paper",
            x=0,
            y=0.01,
            xanchor='left',
            yanchor='top',
            align='left'
        )
    ]
)

output_filename = f"{json_path.stem}.png"
fig.write_image(output_filename, scale=2)