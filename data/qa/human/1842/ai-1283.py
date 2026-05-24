import sys
import json
import os
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print("Usage: python recreate_chart.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]

with open(json_path, 'r', encoding='utf-8') as f:
    chart_info = json.load(f)

fig = go.Figure()

for i, series in enumerate(chart_info["chart_data"]):
    fig.add_trace(go.Scatter(
        x=series["x"],
        y=series["y"],
        mode='lines+markers',
        name=series["name"],
        line=dict(color=chart_info["colors"][i], width=2),
        marker=dict(color=chart_info["colors"][i], size=6, symbol='circle')
    ))

texts = chart_info["texts"]
title_text = f"<span style='font-size:22px'><b>{texts['title']}</b></span><br><span style='font-size:15px;color:#444444'>{texts['subtitle']}</span>"

annotations = chart_info.get("annotations", [])
annotations.append(
    dict(
        text=texts['source'],
        xref="paper", yref="paper",
        x=1, y=1.03,
        showarrow=False,
        xanchor='right', yanchor='bottom',
        font=dict(size=12, color="#444444")
    )
)

fig.update_layout(
    height=600,
    width=1000,
    font_family="Arial",
    title=dict(
        text=title_text,
        x=0.01, y=0.98,
        xanchor='left', yanchor='top'
    ),
    xaxis=dict(
        range=[1986.5, 2003.5],
        tickvals=[1988, 1990, 1992, 1994, 1996, 1998, 2000, 2002],
        showgrid=False,
        showline=True,
        linecolor='#2f80b9',
        linewidth=2,
        mirror=True,
        ticks='outside'
    ),
    yaxis=dict(
        range=[1.2, 4.2],
        tickvals=[1.5, 2.0, 2.5, 3.0, 3.5, 4.0],
        showgrid=True,
        gridcolor='white',
        gridwidth=1.5,
        zeroline=False,
        showline=False,
        ticks='outside'
    ),
    plot_bgcolor='#e5f0f9',
    paper_bgcolor='white',
    showlegend=False,
    margin=dict(l=50, r=40, t=110, b=50),
    annotations=annotations
)

fig.add_shape(
    type="line",
    xref="paper", yref="paper",
    x0=0, y0=0.90, x1=1, y1=0.90,
    line=dict(color="#2f80b9", width=2)
)

base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_filename}.png"

fig.write_image(output_filename, scale=2)