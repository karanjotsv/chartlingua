import sys
import json
import os
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print("Usage: python <script.py> <path_to_json>")
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

data = chart_info['chart_data']
texts = chart_info['texts']
colors = chart_info['colors']

fig = go.Figure()

for i, series in enumerate(data):
    fig.add_trace(go.Scatter(
        x=series['x'],
        y=series['y'],
        mode='lines+markers+text',
        name=series.get('name', ''),
        line=dict(color=colors[i % len(colors)], width=2.5),
        marker=dict(color=colors[i % len(colors)], size=7),
        text=series.get('text', []),
        textposition=series.get('text_positions', 'top center'),
        textfont=dict(
            family="Arial",
            size=12,
            color='black'
        ),
        hoverinfo='skip'
    ))

fig.update_layout(
    font=dict(family="Arial"),
    title_text=texts.get('title') if texts.get('title') else None,
    xaxis=dict(
        title_text=texts.get('x_axis_title'),
        showgrid=True,
        gridcolor='#f0f0f0',
        zeroline=False,
        showline=False
    ),
    yaxis=dict(
        title_text=texts.get('y_axis_title'),
        range=[13.5, 19.5],
        tickmode='array',
        tickvals=[14, 15, 16, 17, 18, 19],
        ticktext=[f"{v}%" for v in [14, 15, 16, 17, 18, 19]],
        showgrid=True,
        gridcolor='#e9e9e9',
        zeroline=False,
        showline=False
    ),
    plot_bgcolor='white',
    paper_bgcolor='white',
    showlegend=False,
    margin=dict(l=60, r=40, t=40, b=80)
)

if texts.get('source'):
    fig.add_annotation(
        text=texts['source'],
        xref="paper", yref="paper",
        x=0.99, y=-0.15,
        showarrow=False,
        xanchor='right', yanchor='top',
        font=dict(size=12, color="#888888")
    )

base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_filename}.png"

fig.write_image(output_filename, scale=2)