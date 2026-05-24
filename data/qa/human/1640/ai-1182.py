import sys
import json
import pathlib
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print("Usage: python script.py <path_to_json>")
    sys.exit(1)

json_path = sys.argv[1]
filename_base = pathlib.Path(json_path).stem

with open(json_path, 'r', encoding='utf-8') as f:
    chart_info = json.load(f)

chart_data = chart_info['chart_data']
texts = chart_info['texts']
colors = chart_info['colors']

fig = go.Figure()

for i, series in enumerate(chart_data):
    color = colors[i]
    fig.add_trace(go.Scatter(
        x=series['x'],
        y=series['y'],
        name=series['name'],
        mode='lines+markers',
        line=dict(color=color, width=2),
        marker=dict(color=color, size=4)
    ))

# Add annotations for series labels
fig.add_annotation(
    x=chart_data[0]['x'][-1],
    y=chart_data[0]['y'][-1],
    text=chart_data[0]['name'],
    showarrow=False,
    xshift=10,
    xanchor="left",
    yanchor="middle",
    font=dict(
        family="Arial",
        size=14,
        color=colors[0]
    )
)

fig.add_annotation(
    x=2004,
    y=50,
    text=chart_data[1]['name'],
    showarrow=False,
    xanchor="right",
    yanchor="bottom",
    font=dict(
        family="Arial",
        size=14,
        color=colors[1]
    )
)

# Combine title and subtitle
title_text = f"<b style='font-size:24px'>{texts['title']}</b><br><span style='font-size:16px; color:#555'>{texts['subtitle']}</span>"

fig.update_layout(
    title=dict(
        text=title_text,
        y=0.95,
        x=0.01,
        xanchor='left',
        yanchor='top'
    ),
    xaxis=dict(
        title_text=texts['x_axis_title'],
        tickvals=[1990, 1992, 1994, 1996, 1998, 2000, 2002, 2004],
        showgrid=False,
        zeroline=False,
        tickfont=dict(size=14)
    ),
    yaxis=dict(
        title_text=texts['y_axis_title'],
        range=[-50, 2250],
        tickvals=[0, 500, 1000, 1500, 2000],
        ticksuffix=" t",
        gridcolor='#e0e0e0',
        griddash='dash',
        zeroline=False,
        tickfont=dict(size=14)
    ),
    font=dict(
        family="Arial",
        size=12
    ),
    plot_bgcolor='white',
    paper_bgcolor='white',
    showlegend=False,
    margin=dict(l=60, r=40, t=130, b=80),
)

# Add source and note annotations
fig.add_annotation(
    text=texts['source'],
    xref="paper", yref="paper",
    x=0, y=-0.15,
    xanchor='left', yanchor='top',
    showarrow=False,
    font=dict(size=12, color="#666")
)

fig.add_annotation(
    text=texts['note'],
    xref="paper", yref="paper",
    x=1, y=-0.15,
    xanchor='right', yanchor='top',
    showarrow=False,
    font=dict(size=12, color="#666")
)

fig.write_image(f"{filename_base}.png", scale=2, width=900, height=600)
print(f"Chart saved to {filename_base}.png")