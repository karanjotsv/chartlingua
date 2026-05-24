import sys
import json
import os
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print("Usage: python create_chart.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]
if not os.path.exists(json_path):
    print(f"Error: File not found at {json_path}")
    sys.exit(1)

with open(json_path, 'r', encoding='utf-8') as f:
    config = json.load(f)

chart_data = config.get('chart_data', [])
texts = config.get('texts', {})
colors = config.get('colors', [])

labels = [item['label'] for item in chart_data]
values = [item['value'] for item in chart_data]

fig = go.Figure()

fig.add_trace(go.Pie(
    labels=labels,
    values=values,
    marker=dict(colors=colors, line=dict(color='#000000', width=1)),
    hoverinfo='label+percent',
    textinfo='none',
    sort=False,
    direction='clockwise',
    startangle=90
))

title_text = ""
if texts.get("title"):
    title_text += f'<b>{texts["title"]}</b>'
if texts.get("subtitle"):
    title_text += f'<br><sub>{texts["subtitle"]}</sub>'

source_text = ""
if texts.get("source"):
    source_text += texts["source"]
if texts.get("note"):
    source_text += f'<br>{texts["note"]}'

fig.update_layout(
    title=dict(
        text=title_text,
        y=0.95,
        x=0.5,
        xanchor='center',
        yanchor='top'
    ),
    font=dict(
        family="Arial",
        size=12,
        color="white"
    ),
    paper_bgcolor='black',
    plot_bgcolor='black',
    showlegend=True,
    legend=dict(
        orientation="v",
        yanchor="top",
        y=0.9,
        xanchor="left",
        x=1.02,
        traceorder='normal'
    ),
    margin=dict(l=50, r=200, t=100, b=50),
    autosize=False,
    width=700,
    height=500
)

if source_text:
    fig.add_annotation(
        text=source_text,
        align='left',
        showarrow=False,
        xref='paper',
        yref='paper',
        x=0,
        y=-0.1,
        xanchor='left',
        yanchor='top'
    )

base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_filename}.png"

fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")