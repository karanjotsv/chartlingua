import sys
import json
import plotly.graph_objects as go
import os

if len(sys.argv) != 2:
    print("Usage: python script.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]

try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_config = json.load(f)
except (FileNotFoundError, json.JSONDecodeError) as e:
    print(f"Error reading or parsing JSON file: {e}")
    sys.exit(1)

chart_data = chart_config.get('chart_data', [])
texts = chart_config.get('texts', {})
colors = chart_config.get('colors', [])

if not chart_data or not colors:
    print("Error: JSON must contain 'chart_data' and 'colors'.")
    sys.exit(1)

categories = [item['category'] for item in chart_data]
values = [item['value'] for item in chart_data]

fig = go.Figure()

fig.add_trace(go.Bar(
    x=categories,
    y=values,
    marker_color=colors[0],
    text=values,
    textposition='outside',
    texttemplate='%{text:.2f}',
    cliponaxis=False,
    textfont=dict(family="Arial", size=12, color='#000000'),
    showlegend=False
))

full_title = ""
if texts.get("title"):
    full_title += f"<b>{texts['title']}</b>"
if texts.get("subtitle"):
    full_title += f"<br><sub>{texts['subtitle']}</sub>"

full_source = ""
if texts.get("source"):
    full_source += texts["source"]
if texts.get("note"):
    full_source += f"<br>{texts['note']}"

fig.update_layout(
    title_text=full_title,
    title_x=0.05,
    title_font_family="Arial",
    yaxis=dict(
        title=texts.get('y_axis_title'),
        range=[0, 2.25],
        tickvals=[0, 0.25, 0.5, 0.75, 1, 1.25, 1.5, 1.75, 2, 2.25],
        showgrid=True,
        gridcolor='#e0e0e0',
        griddash='dot',
        zeroline=False
    ),
    xaxis=dict(
        title=texts.get('x_axis_title'),
        showgrid=False,
        zeroline=False
    ),
    plot_bgcolor='white',
    paper_bgcolor='white',
    font=dict(family="Arial", color='#333333'),
    showlegend=False,
    margin=dict(l=80, r=40, t=60, b=100),
    annotations=[
        dict(
            text=full_source,
            showarrow=False,
            xref='paper',
            yref='paper',
            x=1,
            y=-0.2,
            xanchor='right',
            yanchor='top',
            align='right',
            font=dict(family="Arial", size=10, color='#666666')
        )
    ]
)

output_filename_base = os.path.splitext(os.path.basename(json_path))[0]
output_path = f"{output_filename_base}.png"

fig.write_image(output_path, scale=2)

print(f"Chart saved to {output_path}")