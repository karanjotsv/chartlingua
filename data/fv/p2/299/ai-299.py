import sys
import json
import os
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print("Usage: python <script_name>.py <json_file_path>")
    sys.exit(1)

json_path = sys.argv[1]

try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_data = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_path}")
    sys.exit(1)

data = chart_data['chart_data']
texts = chart_data['texts']
colors = chart_data['colors']

fig = go.Figure()

for i, series in enumerate(data):
    fig.add_trace(go.Scatter(
        x=series['x'],
        y=series['y'],
        mode='lines+markers',
        name=series.get('name', ''),
        line=dict(
            color=colors['series'][i % len(colors['series'])],
            width=3,
            shape='spline',
            smoothing=1.3
        ),
        marker=dict(
            symbol='circle',
            size=10,
            color=colors['marker_fill'],
            line=dict(
                color=colors['series'][i % len(colors['series'])],
                width=2
            )
        ),
        showlegend=False
    ))

title_text = ""
if texts.get('title'):
    title_text += texts['title']
if texts.get('subtitle'):
    title_text += f"<br><sub>{texts['subtitle']}</sub>"

source_text = ""
if texts.get('source'):
    source_text += texts['source']
if texts.get('note'):
    source_text += f"<br>{texts['note']}"

fig.update_layout(
    font=dict(family="Arial", color=colors['text']),
    title=dict(
        text=title_text,
        x=0.05,
        xanchor='left'
    ),
    plot_bgcolor=colors['background'],
    paper_bgcolor=colors['background'],
    xaxis=dict(
        title_text=texts.get('x_axis_title'),
        showgrid=True,
        gridcolor=colors['grid'],
        gridwidth=1,
        showline=False,
        zeroline=False,
        showticklabels=False,
        dtick=1,
        range=[-1, 25.5]
    ),
    yaxis=dict(
        title_text=texts.get('y_axis_title'),
        showgrid=True,
        gridcolor=colors['grid'],
        gridwidth=1,
        showline=False,
        zeroline=False,
        showticklabels=False,
        dtick=1,
        range=[-0.5, 26.5]
    ),
    margin=dict(l=10, r=10, t=20, b=20),
    annotations=[
        dict(
            showarrow=False,
            text=source_text,
            xref="paper",
            yref="paper",
            x=0,
            y=-0.08,
            xanchor="left",
            yanchor="top",
            align="left"
        )
    ]
)

base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_filename}.png"

fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")