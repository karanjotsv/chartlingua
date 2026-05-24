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

chart_data = chart_info["chart_data"]
texts = chart_info["texts"]
colors = chart_info["colors"]

x_values = [d['x'] for d in chart_data]
y_values = [d['y'] for d in chart_data]

fig = go.Figure()

bar_text = [f"{y:.1f}".replace('.0', '') for y in y_values]

fig.add_trace(go.Bar(
    x=x_values,
    y=y_values,
    marker_color=colors[0],
    text=bar_text,
    textposition='outside',
    cliponaxis=False,
    textfont=dict(
        family="Arial",
        size=14,
        color='black'
    )
))

# Combine title and subtitle
title_text = ""
if texts.get("title"):
    title_text += texts["title"]
if texts.get("subtitle"):
    title_text += f"<br><sub>{texts['subtitle']}</sub>"

fig.update_layout(
    title=dict(
        text=title_text,
        x=0.05,
        xanchor='left'
    ),
    xaxis=dict(
        title_text=texts.get("xaxis_title"),
        tickmode='array',
        tickvals=x_values,
        showgrid=False,
        zeroline=False,
        showline=True,
        linecolor='black',
        linewidth=1
    ),
    yaxis=dict(
        title_text=texts.get("yaxis_title"),
        range=[0, 20],
        showgrid=True,
        gridcolor='#E5E5E5',
        zeroline=False,
        showline=False,
        ticks='',
        tickformat=','
    ),
    font=dict(
        family="Arial",
        size=12
    ),
    plot_bgcolor='white',
    paper_bgcolor='white',
    showlegend=False,
    margin=dict(l=80, r=40, t=50, b=100),
    annotations=[
        dict(
            showarrow=False,
            text=texts.get("source", ""),
            xref="paper",
            yref="paper",
            x=1.0,
            y=-0.2,
            xanchor="right",
            yanchor="bottom",
            align="right",
            font=dict(size=10)
        ),
        dict(
            showarrow=False,
            text=texts.get("note", ""),
            xref="paper",
            yref="paper",
            x=0.0,
            y=-0.2,
            xanchor="left",
            yanchor="bottom",
            align="left",
            font=dict(size=12, color=colors[0])
        )
    ]
)

output_filename = json_path.with_suffix('.png')
fig.write_image(output_filename, scale=2)
print(f"Chart saved to {output_filename}")