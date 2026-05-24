import sys
import json
import os
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print("Usage: python <script_name>.py <json_file_path>")
    sys.exit(1)

json_file_path = sys.argv[1]

try:
    with open(json_file_path, 'r', encoding='utf-8') as f:
        config = json.load(f)
except FileNotFoundError:
    print(f"Error: The file {json_file_path} was not found.")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Failed to decode JSON from {json_file_path}.")
    sys.exit(1)

chart_data = config.get('chart_data', [])
texts = config.get('texts', {})
colors = config.get('colors', [])

labels = [d['category'] for d in chart_data]
values = [d['value'] for d in chart_data]

fig = go.Figure()

fig.add_trace(go.Pie(
    labels=labels,
    values=values,
    marker=dict(colors=colors, line=dict(color='#ffffff', width=1)),
    textposition='outside',
    texttemplate='%{label} %{value}%',
    hoverinfo='label+percent',
    sort=False,
    direction='clockwise'
))

title_text = texts.get('title') or ""
if texts.get('subtitle'):
    title_text += f"<br><sub>{texts['subtitle']}</sub>"

fig.update_layout(
    title_text=title_text if title_text else None,
    title_x=0.5,
    showlegend=False,
    font=dict(family="Arial", size=12, color='black'),
    margin=dict(l=80, r=80, t=60, b=60),
    paper_bgcolor='white',
    plot_bgcolor='white',
    autosize=False,
    width=800,
    height=600
)

if texts.get('source'):
    fig.add_annotation(
        text=texts['source'],
        align='right',
        showarrow=False,
        xref='paper',
        yref='paper',
        x=0.99,
        y=0.01,
        xanchor='right',
        yanchor='bottom',
        font=dict(family="Arial", size=10, color='grey')
    )

base_filename = os.path.splitext(os.path.basename(json_file_path))[0]
output_image_path = f"{base_filename}.png"
fig.write_image(output_image_path, scale=2)

print(f"Chart saved to {output_image_path}")