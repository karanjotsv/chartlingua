import sys
import json
import os
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print(f"Usage: python {os.path.basename(__file__)} <json_file_path>")
    sys.exit(1)

json_path = sys.argv[1]

try:
    with open(json_path, 'r', encoding='utf-8') as f:
        config = json.load(f)
except FileNotFoundError:
    print(f"Error: The file '{json_path}' was not found.")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Failed to decode JSON from '{json_path}'.")
    sys.exit(1)

chart_data = config.get('chart_data', [])
texts = config.get('texts', {})
colors = config.get('colors', [])

labels = [item['label'] for item in chart_data]
values = [item['value'] for item in chart_data]

fig = go.Figure()

fig.add_trace(go.Pie(
    labels=labels,
    values=values,
    marker=dict(colors=colors, line=dict(color='#FFFFFF', width=1)),
    sort=False,
    direction='clockwise',
    textinfo='none',
    hoverinfo='label+percent',
    hole=0
))

title_text = f"<b>{texts.get('title', '')}</b>"
if texts.get('subtitle'):
    title_text += f"<br><sub>{texts.get('subtitle')}</sub>"

fig.update_layout(
    title=dict(
        text=title_text,
        y=0.95,
        x=0.5,
        xanchor='center',
        yanchor='top',
        font=dict(size=18)
    ),
    font=dict(
        family="Arial",
        size=12
    ),
    legend=dict(
        orientation="v",
        yanchor="top",
        y=0.9,
        xanchor="left",
        x=1.02,
        traceorder="normal"
    ),
    margin=dict(l=40, r=180, t=80, b=40),
    showlegend=True
)

if texts.get('source'):
    fig.add_annotation(
        text=texts['source'],
        align='left',
        showarrow=False,
        xref='paper',
        yref='paper',
        x=0,
        y=-0.1,
        xanchor='left',
        yanchor='top',
        font=dict(size=10)
    )

base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_filename}.png"

fig.write_image(output_filename, scale=2, width=700, height=450)

print(f"Chart saved to {output_filename}")