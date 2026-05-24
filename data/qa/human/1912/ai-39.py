import sys
import json
import os
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print("Usage: python create_chart.py <path_to_json>")
    sys.exit(1)

json_path = sys.argv[1]

try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_info = json.load(f)
except FileNotFoundError:
    print(f"Error: File not found at {json_path}")
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
    y=categories,
    x=values,
    orientation='h',
    marker=dict(color=colors[0]),
    texttemplate='%{x}%',
    textposition='outside',
    textfont=dict(family="Arial", size=12, color='black'),
    cliponaxis=False
))

title_text = ""
if texts.get('title'):
    title_text += f"<b>{texts['title']}</b>"
if texts.get('subtitle'):
    title_text += f"<br><sup>{texts['subtitle']}</sup>" if title_text else f"<sup>{texts['subtitle']}</sup>"

fig.update_layout(
    font=dict(family="Arial", size=12),
    title=dict(
        text=title_text,
        x=0.05,
        xanchor='left'
    ),
    xaxis=dict(
        title=dict(
            text=texts['x_axis_title'],
            standoff=15
        ),
        ticksuffix='%',
        showgrid=True,
        gridcolor='#e0e0e0',
        griddash='dot',
        zeroline=False,
        range=[0, max(values) * 1.25]
    ),
    yaxis=dict(
        showgrid=False,
        zeroline=False
    ),
    plot_bgcolor='white',
    paper_bgcolor='white',
    margin=dict(l=200, r=40, t=50, b=80),
    showlegend=False
)

annotations = []
if texts.get('source'):
    annotations.append(
        dict(
            text=texts['source'],
            xref="paper", yref="paper",
            x=1.0, y=-0.15,
            xanchor='right', yanchor='top',
            showarrow=False,
            font=dict(family="Arial", size=10, color="grey")
        )
    )

fig.update_layout(annotations=annotations)

base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_filename}.png"

fig.write_image(output_filename, scale=2)
print(f"Chart saved to {output_filename}")