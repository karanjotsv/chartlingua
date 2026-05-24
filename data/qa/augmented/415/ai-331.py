import sys
import json
import os
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print("Usage: python recreate_chart.py <path_to_json_file>")
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

chart_data = chart_info['chart_data']
texts = chart_info['texts']
colors = chart_info['colors']

categories = [item['category'] for item in chart_data]
values = [item['value'] for item in chart_data]

fig = go.Figure()

fig.add_trace(go.Bar(
    x=categories,
    y=values,
    marker_color=colors[0],
    text=values,
    textposition='outside',
    texttemplate='%{text}',
    cliponaxis=False
))

title_text = ""
if texts.get('title'):
    title_text += f"<b>{texts['title']}</b>"
if texts.get('subtitle'):
    title_text += f"<br><sub>{texts['subtitle']}</sub>"

annotations = []
if texts.get('note'):
    annotations.append(
        dict(
            xref='paper', yref='paper',
            x=0, y=-0.2,
            xanchor='left', yanchor='top',
            text=texts['note'],
            showarrow=False,
            font=dict(family="Arial", size=12, color="blue")
        )
    )

if texts.get('source'):
    annotations.append(
        dict(
            xref='paper', yref='paper',
            x=1, y=-0.2,
            xanchor='right', yanchor='top',
            text=texts['source'],
            showarrow=False,
            font=dict(family="Arial", size=12, color="grey")
        )
    )

fig.update_layout(
    title=dict(
        text=title_text,
        x=0.05,
        xanchor='left'
    ),
    yaxis=dict(
        title=texts.get('y_axis_title'),
        range=[0, 150],
        tickvals=[0, 25, 50, 75, 100, 125, 150],
        gridcolor='#E5E5E5',
        zeroline=False
    ),
    xaxis=dict(
        title=texts.get('x_axis_title'),
        gridcolor='#F0F0F0'
    ),
    plot_bgcolor='white',
    paper_bgcolor='white',
    font=dict(family="Arial", size=12, color='#333333'),
    showlegend=False,
    margin=dict(l=80, r=40, t=50, b=120),
    annotations=annotations,
    bargap=0.3
)

fig.update_traces(
    textfont=dict(
        family="Arial",
        size=12
    )
)

base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_filename}.png"

fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")