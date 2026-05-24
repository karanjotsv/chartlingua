import sys
import json
import os
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print(f"Usage: python {os.path.basename(__file__)} <json_file_path>")
    sys.exit(1)

json_path = sys.argv[1]

if not os.path.exists(json_path):
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)

with open(json_path, 'r', encoding='utf-8') as f:
    config = json.load(f)

chart_data = config['chart_data']
texts_data = config['texts']
colors = config['colors']

labels = [d['label'] for d in chart_data]
values = [d['value'] for d in chart_data]
texts = [d['text'] for d in chart_data]
text_positions = [d['text_position'] for d in chart_data]
pulls = [d['pull'] for d in chart_data]

trace = go.Pie(
    labels=labels,
    values=values,
    text=texts,
    textposition=text_positions,
    pull=pulls,
    marker=dict(colors=colors, line=dict(color='white', width=1)),
    hoverinfo='none',
    textinfo='text',
    sort=False,
    direction='clockwise',
    rotation=90,
    insidetextfont=dict(family="Arial", color='black'),
    outsidetextfont=dict(family="Arial", color='black', size=11),
    textfont=dict(size=11)
)

fig = go.Figure(data=[trace])

title_text = ""
if texts_data.get("title"):
    title_text += f"<b>{texts_data['title']}</b>"
if texts_data.get("subtitle"):
    title_text += f"<br>{texts_data['subtitle']}" if title_text else texts_data['subtitle']

source_text = ""
if texts_data.get("source"):
    source_text += f"Source: {texts_data['source']}"
if texts_data.get("note"):
    if source_text:
        source_text += "<br>"
    source_text += f"Note: {texts_data['note']}"

fig.update_layout(
    title_text=title_text if title_text else None,
    title_x=0.5,
    font=dict(family="Arial"),
    showlegend=False,
    paper_bgcolor='white',
    plot_bgcolor='white',
    margin=dict(l=100, r=100, t=60, b=60),
)

if source_text:
    fig.add_annotation(
        text=source_text,
        align='left',
        showarrow=False,
        xref='paper',
        yref='paper',
        x=0,
        y=-0.05,
        xanchor='left',
        yanchor='top'
    )

base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_path = f"{base_filename}.png"

fig.write_image(output_path, scale=2)

print(f"Chart saved to {output_path}")