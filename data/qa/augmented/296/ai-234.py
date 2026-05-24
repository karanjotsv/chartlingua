import sys
import json
import pathlib
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print("Usage: python create_chart.py <path_to_json_file>", file=sys.stderr)
    sys.exit(1)

json_file_path = pathlib.Path(sys.argv[1])
output_image_path = json_file_path.with_suffix(".png")

try:
    with open(json_file_path, 'r', encoding='utf-8') as f:
        config = json.load(f)
except (FileNotFoundError, json.JSONDecodeError) as e:
    print(f"Error reading or parsing JSON file: {e}", file=sys.stderr)
    sys.exit(1)

chart_data = config.get('chart_data', [])
texts = config.get('texts', {})
colors = config.get('colors', [])

categories = [item['category'] for item in chart_data]
values = [item['value'] for item in chart_data]

fig = go.Figure()

fig.add_trace(go.Bar(
    x=categories,
    y=values,
    marker_color=colors[0] if colors else '#1f77b4',
    text=values,
    texttemplate='%{text}',
    textposition='outside',
    cliponaxis=False,
    textfont=dict(
        family="Arial",
        size=12,
        color='black'
    ),
    width=0.7
))

title_text = ""
if texts.get('title'):
    title_text += f"<b>{texts['title']}</b>"
if texts.get('subtitle'):
    title_text += f"<br><sub>{texts['subtitle']}</sub>"

source_text = texts.get('source', '')

fig.update_layout(
    font=dict(family="Arial", size=12, color='#333333'),
    title=dict(
        text=title_text if title_text else None,
        x=0.05,
        xanchor='left',
        y=0.95,
        yanchor='top'
    ),
    xaxis=dict(
        title_text=texts.get('x_axis_title'),
        showgrid=False,
        showline=True,
        linewidth=1,
        linecolor='black',
        tickfont=dict(size=12)
    ),
    yaxis=dict(
        title_text=texts.get('y_axis_title'),
        range=[0, 70],
        dtick=10,
        showline=False,
        gridcolor='#E0E0E0',
        griddash='dot',
        zeroline=False,
        tickfont=dict(size=12)
    ),
    plot_bgcolor='white',
    paper_bgcolor='#F8F9FA',
    showlegend=False,
    margin=dict(l=100, r=40, t=60, b=100),
    annotations=[
        dict(
            showarrow=False,
            text=source_text,
            xref="paper",
            yref="paper",
            x=1.0,
            y=-0.2,
            xanchor='right',
            yanchor='top',
            font=dict(size=10, color='#6c757d')
        )
    ]
)

fig.write_image(str(output_image_path), scale=2)

print(f"Chart saved to {output_image_path}")