import sys
import json
import os
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print("Usage: python <script_name>.py <path_to_json>")
    sys.exit(1)

json_path = sys.argv[1]

try:
    with open(json_path, 'r', encoding='utf-8') as f:
        config = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_path}")
    sys.exit(1)

chart_data = config.get('chart_data', [])
texts = config.get('texts', {})
colors = config.get('colors', [])

fig = go.Figure()

for i, series in enumerate(chart_data):
    fig.add_trace(go.Bar(
        name=series['name'],
        x=series['x'],
        y=series['y'],
        marker_color=colors[i],
        text=series['y'],
        textposition='inside',
        insidetextanchor='middle',
        textfont=dict(
            family='Arial',
            size=12,
            color='white',
            weight='bold'
        ),
        hoverinfo='skip'
    ))

fig.update_layout(
    barmode='stack',
    paper_bgcolor='white',
    plot_bgcolor='white',
    font=dict(
        family="Arial",
        size=12
    ),
    title=dict(
        text=texts.get('title'),
        x=0.05,
        xanchor='left'
    ),
    yaxis=dict(
        title=texts.get('ytitle'),
        range=[0, 10],
        tickmode='linear',
        dtick=2.5,
        showgrid=True,
        gridcolor='lightgray',
        gridwidth=1
    ),
    xaxis=dict(
        title=texts.get('xtitle'),
        tickangle=-45,
        showgrid=False
    ),
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=-0.4,
        xanchor="center",
        x=0.5
    ),
    margin=dict(l=60, r=20, t=40, b=180),
    annotations=[
        dict(
            text=texts.get('source'),
            showarrow=False,
            xref='paper',
            yref='paper',
            x=1,
            y=-0.45,
            xanchor='right',
            yanchor='bottom',
            font=dict(
                family="Arial",
                size=12
            )
        )
    ]
)

base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_filename}.png"

fig.write_image(output_filename, scale=2)
print(f"Chart saved to {output_filename}")