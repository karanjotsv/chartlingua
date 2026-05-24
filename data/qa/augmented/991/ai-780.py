import sys
import json
import os
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print("Usage: python recreate_chart.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]

try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_details = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_path}")
    sys.exit(1)

chart_data = chart_details.get('chart_data', [])
texts = chart_details.get('texts', {})
colors = chart_details.get('colors', [])

fig = go.Figure()

for i, series in enumerate(chart_data):
    fig.add_trace(go.Bar(
        x=series.get('x'),
        y=series.get('y'),
        name=series.get('name'),
        marker_color=colors[i % len(colors)] if colors else None,
        text=series.get('y'),
        textposition='inside',
        insidetextanchor='middle',
        textfont=dict(
            family="Arial",
            color='white'
        ),
        texttemplate='<b>%{text}</b>'
    ))

fig.update_layout(
    barmode='stack',
    title_text=texts.get('title'),
    xaxis_title_text=texts.get('xlabel'),
    yaxis_title_text=texts.get('ylabel'),
    font=dict(
        family="Arial",
        size=12
    ),
    plot_bgcolor='white',
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=-0.25,
        xanchor="center",
        x=0.5
    ),
    xaxis=dict(
        type='category',
        showgrid=True,
        gridcolor='#f0f0f0',
        gridwidth=1
    ),
    yaxis=dict(
        range=[0, 55],
        tickvals=[0, 10, 20, 30, 40, 50],
        showgrid=True,
        gridcolor='#e9e9e9'
    ),
    margin=dict(l=60, r=40, t=50, b=120)
)

if texts.get('source'):
    fig.add_annotation(
        text=texts['source'],
        align='right',
        showarrow=False,
        xref='paper',
        yref='paper',
        x=0.99,
        y=-0.3,
        font=dict(
            family="Arial",
            size=12,
            color="#666666"
        )
    )

base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_filename}.png"

fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")