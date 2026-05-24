import sys
import json
import os
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <path_to_json>")
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

chart_data = chart_info.get('chart_data', [])
chart_texts = chart_info.get('texts', {})
colors = chart_info.get('colors', [])

categories = [item['category'] for item in chart_data]
values = [item['value'] for item in chart_data]
x_axis_suffix = chart_texts.get('x_axis_suffix', '')

fig = go.Figure()

fig.add_trace(go.Bar(
    y=categories,
    x=values,
    orientation='h',
    marker=dict(color=colors),
    text=[f"{v:.2f}{x_axis_suffix}" for v in values],
    textposition='outside',
    textfont=dict(family="Arial", size=14, color='black'),
    hoverinfo='none',
    cliponaxis=False
))

title_text = f"<b>{chart_texts.get('title', '')}</b><br><span style='font-size:0.8em;color:#555555'>{chart_texts.get('subtitle', '')}</span>"

fig.update_layout(
    title=dict(
        text=title_text,
        x=0.01,
        y=0.95,
        xanchor='left',
        yanchor='top',
        font=dict(size=24)
    ),
    xaxis=dict(
        showgrid=True,
        gridcolor='#E5E5E5',
        gridwidth=1,
        griddash='dash',
        zeroline=False,
        showline=False,
        showticklabels=True,
        ticksuffix=x_axis_suffix,
        range=[0, max(values) * 1.15]
    ),
    yaxis=dict(
        autorange='reversed',
        showline=False,
        showgrid=False,
        ticks='',
        tickfont=dict(size=14)
    ),
    font=dict(
        family="Arial",
        size=12,
        color="black"
    ),
    plot_bgcolor='white',
    paper_bgcolor='white',
    showlegend=False,
    margin=dict(l=170, r=60, t=150, b=80),
)

fig.add_annotation(
    text=f"{chart_texts.get('source', '')}<br>{chart_texts.get('note', '')}",
    xref="paper",
    yref="paper",
    x=0.0,
    y=-0.1,
    xanchor='left',
    yanchor='top',
    align='left',
    showarrow=False,
    font=dict(size=12, color='#7f7f7f')
)

output_filename_base, _ = os.path.splitext(json_path)
output_filename = f"{output_filename_base}.png"

fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")