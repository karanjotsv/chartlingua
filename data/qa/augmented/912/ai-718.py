import sys
import json
import os
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print("Usage: python create_chart.py <json_file_path>", file=sys.stderr)
    sys.exit(1)

json_path = sys.argv[1]

try:
    with open(json_path, 'r', encoding='utf-8') as f:
        config = json.load(f)
except FileNotFoundError:
    print(f"Error: File not found at {json_path}", file=sys.stderr)
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Invalid JSON format in {json_path}", file=sys.stderr)
    sys.exit(1)

chart_data = config.get('chart_data', {})
texts = config.get('texts', {})
colors = config.get('colors', [])
categories = chart_data.get('categories', [])

fig = go.Figure()

for i, series in enumerate(chart_data.get('series', [])):
    fig.add_trace(go.Bar(
        x=categories,
        y=series.get('data', []),
        name=series.get('name', ''),
        marker_color=colors[i % len(colors)] if colors else None,
        text=series.get('data', []),
        textposition='inside',
        textfont=dict(color='white', family='Arial', size=12),
        insidetextanchor='middle'
    ))

title_text = texts.get('title') or ''
if texts.get('subtitle'):
    title_text += f"<br><sub>{texts.get('subtitle')}</sub>"

source_text = texts.get('source', '')

fig.update_layout(
    barmode='stack',
    title_text=title_text if title_text else None,
    xaxis=dict(
        title_text=texts.get('x_axis_title'),
        showgrid=False,
        zeroline=False
    ),
    yaxis=dict(
        title_text=texts.get('y_axis_title'),
        range=[0, 801],
        tickvals=[0, 200, 400, 600, 800],
        gridcolor='#e9e9e9',
        showgrid=True,
        zeroline=False
    ),
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=-0.25,
        xanchor="center",
        x=0.5
    ),
    plot_bgcolor='white',
    paper_bgcolor='white',
    font=dict(family="Arial", size=12),
    margin=dict(l=80, r=20, b=120, t=40),
    bargap=0.3,
    annotations=[
        dict(
            text=source_text,
            showarrow=False,
            xref='paper',
            yref='paper',
            x=1,
            y=-0.3,
            xanchor='right',
            yanchor='bottom',
            font=dict(family="Arial", size=10, color='#666666'),
            align='right'
        )
    ] if source_text else []
)

base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_filename}.png"

fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")