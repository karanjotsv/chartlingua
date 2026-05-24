import sys
import json
import os
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <json_file_path>")
    sys.exit(1)

json_file_path = sys.argv[1]

try:
    with open(json_file_path, 'r', encoding='utf-8') as f:
        chart_data = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_file_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_file_path}")
    sys.exit(1)

fig = go.Figure()

# Add traces for each data series
for i, series in enumerate(chart_data['chart_data']):
    color = chart_data['colors'][i]
    fig.add_trace(go.Scatter(
        x=series['x'],
        y=series['y'],
        name=series['name'],
        mode='lines+markers',
        line=dict(color=color, width=2),
        marker=dict(color=color, size=5),
        showlegend=False
    ))

# Add annotations for series labels at the end of each line
for i, series in enumerate(chart_data['chart_data']):
    fig.add_annotation(
        x=series['x'][-1],
        y=series['y'][-1],
        text=series['name'],
        showarrow=False,
        xanchor='left',
        xshift=8,
        font=dict(
            family="Arial",
            size=14,
            color=chart_data['colors'][i]
        )
    )

texts = chart_data['texts']
title_text = f"<b>{texts['title']}</b><br><span style='font-size: 16px; color: #555555;'>{texts['subtitle']}</span>"

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
        title_text=texts['x_axis_title'],
        tickvals=[1990, 1992, 1994, 1996, 1998, 1999],
        showgrid=False,
        zeroline=False,
        tickfont=dict(size=14),
        range=[1989.5, 2002.5] 
    ),
    yaxis=dict(
        title_text=texts['y_axis_title'],
        tickvals=[0, 20, 40, 60, 80],
        ticksuffix='%',
        showgrid=True,
        gridcolor='#e0e0e0',
        gridwidth=1,
        griddash='dot',
        zeroline=False,
        tickfont=dict(size=14),
        range=[-5, 90]
    ),
    font=dict(
        family="Arial",
        size=12,
        color="#333333"
    ),
    plot_bgcolor='white',
    paper_bgcolor='white',
    margin=dict(l=60, r=200, t=110, b=90),
    width=900,
    height=600,
    showlegend=False
)

# Add source and note annotations
fig.add_annotation(
    text=texts['source'],
    xref="paper",
    yref="paper",
    x=0.0,
    y=-0.15,
    showarrow=False,
    xanchor='left',
    yanchor='top',
    font=dict(size=12, color='#555555')
)

fig.add_annotation(
    text=texts['note'],
    xref="paper",
    yref="paper",
    x=1.0,
    y=-0.15,
    showarrow=False,
    xanchor='right',
    yanchor='top',
    font=dict(size=12, color='#555555')
)


base_filename = os.path.splitext(os.path.basename(json_file_path))[0]
output_image_path = f"{base_filename}.png"

fig.write_image(output_image_path, scale=2)

print(f"Chart saved to {output_image_path}")