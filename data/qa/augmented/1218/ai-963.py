import sys
import json
from pathlib import Path
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print("Usage: python script.py <path_to_json_file>")
    sys.exit(1)

json_path = Path(sys.argv[1])
if not json_path.is_file():
    print(f"Error: File not found at {json_path}")
    sys.exit(1)

with open(json_path, 'r', encoding='utf-8') as f:
    chart_info = json.load(f)

chart_data = chart_info.get("chart_data", [])
texts = chart_info.get("texts", {})
colors = chart_info.get("colors", [])

categories = [item['category'] for item in chart_data]
values = [item['value'] for item in chart_data]

fig = go.Figure()

fig.add_trace(go.Bar(
    x=categories,
    y=values,
    text=[f'{v:.2f}' if v < 1 else f'{v:.1f}' if v == 3.9 else f'{v:.2f}' for v in values],
    textposition='outside',
    marker_color=colors[0] if colors else '#3678D1',
    hoverinfo='none',
    cliponaxis=False
))

title_text = texts.get("title")
if texts.get("subtitle"):
    title_text = f"<b>{title_text}</b><br>{texts.get('subtitle')}" if title_text else texts.get('subtitle')

fig.update_layout(
    title_text=title_text,
    yaxis_title=texts.get("y_axis_title"),
    xaxis_title=texts.get("x_axis_title"),
    font=dict(family="Arial", size=12, color="black"),
    plot_bgcolor='white',
    paper_bgcolor='white',
    bargap=0.35,
    margin=dict(l=80, r=40, t=40, b=80),
    xaxis=dict(
        showgrid=False,
        showline=False,
        zeroline=False,
        tickfont=dict(size=12)
    ),
    yaxis=dict(
        showgrid=True,
        gridcolor='#EAEAEA',
        griddash='dot',
        zeroline=False,
        range=[0, 5],
        dtick=1,
        tickfont=dict(size=12)
    ),
    showlegend=False
)

if texts.get("source"):
    fig.add_annotation(
        text=texts.get("source"),
        xref="paper", yref="paper",
        x=1, y=-0.15,
        xanchor="right", yanchor="top",
        showarrow=False,
        font=dict(family="Arial", size=12, color="#666666")
    )

output_filename = f"{json_path.stem}.png"
fig.write_image(output_filename, scale=2)
print(f"Chart saved to {output_filename}")