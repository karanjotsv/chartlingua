import sys
import json
import plotly.graph_objects as go
import os

if len(sys.argv) != 2:
    print(f"Usage: python {os.path.basename(sys.argv[0])} <json_file_path>")
    sys.exit(1)

json_path = sys.argv[1]

try:
    with open(json_path, 'r', encoding='utf-8') as f:
        config = json.load(f)
except FileNotFoundError:
    print(f"Error: File not found at {json_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Invalid JSON format in {json_path}")
    sys.exit(1)

chart_data = config.get('chart_data', [])
texts = config.get('texts', {})
colors = config.get('colors', [])

fig = go.Figure()

for i, series in enumerate(chart_data):
    fig.add_trace(go.Scatter(
        x=series.get('x'),
        y=series.get('y'),
        mode='lines',
        line=dict(color=colors[i % len(colors)], width=2),
        showlegend=False
    ))

fig.update_layout(
    font=dict(family="Arial"),
    plot_bgcolor='white',
    paper_bgcolor='white',
    margin=dict(l=60, r=40, t=40, b=60),
    xaxis=dict(
        range=[0, 10.1],
        tickmode='linear',
        tick0=0,
        dtick=1,
        showline=True,
        linewidth=1.5,
        linecolor='black',
        mirror=True,
        showgrid=True,
        gridcolor='#aaaaaa',
        gridwidth=1,
        minor=dict(
            showgrid=True,
            gridcolor='#e0e0e0',
            gridwidth=0.5
        )
    ),
    yaxis=dict(
        range=[0, 10.1],
        tickmode='linear',
        tick0=0,
        dtick=1,
        showline=True,
        linewidth=1.5,
        linecolor='black',
        mirror=True,
        showgrid=True,
        gridcolor='#aaaaaa',
        gridwidth=1,
        minor=dict(
            showgrid=True,
            gridcolor='#e0e0e0',
            gridwidth=0.5
        )
    ),
    annotations=[
        dict(
            xref='paper', yref='paper',
            x=1.02, y=-0.08,
            text=texts.get('x_axis_title', ''),
            showarrow=False,
            xanchor='left', yanchor='top',
            font=dict(family="Arial", size=12)
        ),
        dict(
            xref='paper', yref='paper',
            x=-0.08, y=1.03,
            text=texts.get('y_axis_title', ''),
            showarrow=False,
            xanchor='left', yanchor='bottom',
            font=dict(family="Arial", size=12)
        )
    ]
)

base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_filename}.png"

fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")