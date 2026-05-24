import sys
import os
import json
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print("Usage: python <script_name>.py <path_to_json>")
    sys.exit(1)

json_path = sys.argv[1]

try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_info = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_path}")
    sys.exit(1)

data = chart_info['chart_data']
texts = chart_info['texts']
colors = chart_info['colors']

x_values = [d['year'] for d in data]
y_values = [d['value'] for d in data]

fig = go.Figure()

fig.add_trace(go.Bar(
    x=x_values,
    y=y_values,
    text=[f'{v:g}' for v in y_values],
    textposition='auto',
    marker_color=colors[0],
    hoverinfo='none'
))

title_text = ""
if texts.get('title'):
    title_text += f"<b>{texts['title']}</b>"
if texts.get('subtitle'):
    title_text += f"<br><sub>{texts['subtitle']}</sub>"

source_parts = []
if texts.get('source'):
    source_parts.append(texts['source'])
if texts.get('note'):
    source_parts.append(texts['note'])
source_text = "<br>".join(source_parts)

fig.update_layout(
    title=dict(
        text=title_text,
        x=0.05,
        xanchor='left'
    ),
    xaxis=dict(
        title_text=texts.get('x_axis_title'),
        tickvals=x_values,
        tickangle=0,
        showgrid=True,
        gridcolor='#f0f0f0',
        linecolor='lightgray'
    ),
    yaxis=dict(
        title_text=texts.get('y_axis_title'),
        range=[0, 120],
        tickvals=[0, 20, 40, 60, 80, 100, 120],
        showgrid=True,
        gridcolor='#e9e9e9',
        zeroline=False
    ),
    plot_bgcolor='white',
    paper_bgcolor='#f8f9fa',
    font=dict(
        family="Arial",
        size=12,
        color="black"
    ),
    margin=dict(l=90, r=40, t=60, b=100),
    showlegend=False,
    annotations=[
        dict(
            text=source_text,
            showarrow=False,
            xref="paper",
            yref="paper",
            x=1.0,
            y=-0.22,
            xanchor='right',
            yanchor='top',
            align='right',
            font=dict(
                family="Arial",
                size=12
            )
        )
    ]
)

fig.update_traces(textfont_size=12, textangle=0)

base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_filename}.png"

fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")