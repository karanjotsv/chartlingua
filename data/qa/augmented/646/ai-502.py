import sys
import json
import os
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print(f"Usage: python {os.path.basename(__file__)} <json_file_path>")
    sys.exit(1)

json_file_path = sys.argv[1]

try:
    with open(json_file_path, 'r', encoding='utf-8') as f:
        chart_config = json.load(f)
except FileNotFoundError:
    print(f"Error: The file '{json_file_path}' was not found.")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Failed to decode JSON from '{json_file_path}'.")
    sys.exit(1)


data = chart_config.get('chart_data', [])
texts = chart_config.get('texts', {})
colors = chart_config.get('colors', [])

categories = [item['category'] for item in data]
values = [item['value'] for item in data]

fig = go.Figure()

fig.add_trace(go.Bar(
    y=categories,
    x=values,
    orientation='h',
    marker=dict(
        color=colors[0] if colors else '#3379E0'
    )
))

title_text = ""
if texts.get('title'):
    title_text += f"<b>{texts['title']}</b>"
if texts.get('subtitle'):
    if title_text:
        title_text += "<br>"
    title_text += texts['subtitle']

fig.update_layout(
    font=dict(family="Arial", size=12, color="black"),
    title=dict(
        text=title_text,
        x=0.05,
        xanchor='left',
        y=0.95,
        yanchor='top'
    ),
    xaxis=dict(
        title=texts.get('x_axis_title', None),
        range=[0, 150],
        showgrid=True,
        gridcolor='#e9e9e9',
        gridwidth=1,
        griddash='dot',
        zeroline=False,
        showline=False,
        tickfont=dict(size=12)
    ),
    yaxis=dict(
        title=texts.get('y_axis_title', None),
        autorange='reversed',
        showgrid=False,
        tickfont=dict(size=12)
    ),
    plot_bgcolor='white',
    paper_bgcolor='white',
    margin=dict(l=100, r=40, t=50, b=80),
    showlegend=False
)

if texts.get('source'):
    fig.add_annotation(
        text=texts['source'],
        xref="paper",
        yref="paper",
        x=1,
        y=-0.18,
        showarrow=False,
        xanchor='right',
        yanchor='bottom',
        align='right',
        font=dict(size=10, color="#7f7f7f")
    )

base_filename = os.path.splitext(os.path.basename(json_file_path))[0]
output_image_path = f"{base_filename}.png"

fig.write_image(output_image_path, scale=2)

print(f"Chart saved to {output_image_path}")