import sys
import json
import os
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <json_file_path>")
    sys.exit(1)

json_path = sys.argv[1]

try:
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_path}")
    sys.exit(1)

fig = go.Figure()

chart_data = data.get('chart_data', [])
colors = data.get('colors', [])
texts = data.get('texts', {})

for i, series in enumerate(chart_data):
    color = colors[i] if i < len(colors) else None
    if series.get('name') == 'Other Countries':
        fig.add_trace(go.Scatter(
            x=series.get('x'),
            y=series.get('y'),
            mode='markers',
            marker=dict(color=color, size=6),
            name=''
        ))
    elif series.get('name') == 'Highlighted Countries':
        fig.add_trace(go.Scatter(
            x=series.get('x'),
            y=series.get('y'),
            mode='markers+text',
            marker=dict(color=color, size=10),
            text=series.get('labels'),
            textposition=series.get('text_positions'),
            textfont=dict(family="Arial", size=12, color='black'),
            name=''
        ))
    elif series.get('name') == 'Trendline':
        fig.add_trace(go.Scatter(
            x=series.get('x'),
            y=series.get('y'),
            mode='lines',
            line=dict(color=color, width=2),
            name=''
        ))

fig.update_layout(
    title=dict(
        text=texts.get('title'),
        x=0.5,
        font=dict(size=20)
    ),
    xaxis=dict(
        title=texts.get('x_axis_title'),
        range=[-5000, 120000],
        tickvals=[0, 30000, 60000, 90000, 120000],
        tickformat='$,.0f',
        showgrid=False,
        zeroline=False
    ),
    yaxis=dict(
        title=texts.get('y_axis_title'),
        range=[-5, 105],
        tickvals=[0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100],
        gridcolor='lightgrey',
        zeroline=False
    ),
    font=dict(family="Arial"),
    plot_bgcolor='white',
    paper_bgcolor='white',
    showlegend=False,
    margin=dict(l=90, r=40, t=80, b=80),
    annotations=[
        dict(
            text=texts.get('source'),
            showarrow=False,
            xref='paper',
            yref='paper',
            x=0,
            y=-0.15,
            xanchor='left',
            yanchor='top',
            font=dict(size=12)
        )
    ]
)

base_filename, _ = os.path.splitext(json_path)
output_filename = f"{base_filename}.png"

fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")