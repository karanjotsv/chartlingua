import sys
import json
import os
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print("Usage: python create_chart.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]
if not os.path.exists(json_path):
    print(f"Error: File not found at {json_path}")
    sys.exit(1)
    
base_name = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_name}.png"

with open(json_path, 'r', encoding='utf-8') as f:
    config = json.load(f)

fig = go.Figure()

chart_data = config.get('chart_data', [])
colors = config.get('colors', [])
texts = config.get('texts', {})

marker_symbols = ['square', 'diamond']

for i, series in enumerate(chart_data):
    fig.add_trace(go.Scatter(
        x=series.get('x'),
        y=series.get('y'),
        name=series.get('name'),
        mode='lines+markers',
        line=dict(color=colors[i], width=2),
        marker=dict(
            symbol=marker_symbols[i % len(marker_symbols)],
            color=colors[i],
            size=8
        )
    ))

title_text = texts.get('title', '')
if texts.get('subtitle'):
    title_text += f"<br><sub>{texts['subtitle']}</sub>"

fig.update_layout(
    title=dict(
        text=title_text,
        x=0.5,
        y=0.95,
        xanchor='center',
        yanchor='top'
    ),
    xaxis=dict(
        title=texts.get('x_axis_title'),
        tickmode='array',
        tickvals=chart_data[0]['x'] if chart_data and 'x' in chart_data[0] else None,
        showgrid=False,
        showline=True,
        linewidth=1,
        linecolor='black'
    ),
    yaxis=dict(
        title=texts.get('y_axis_title'),
        range=[0, 25000],
        tickvals=[0, 5000, 10000, 15000, 20000, 25000],
        gridcolor='lightgray',
        showline=True,
        linewidth=1,
        linecolor='black'
    ),
    font=dict(
        family="Arial",
        size=12
    ),
    legend=dict(
        x=0.98,
        y=0.65,
        xanchor='right',
        yanchor='top'
    ),
    plot_bgcolor='white',
    paper_bgcolor='white',
    margin=dict(l=80, r=50, t=80, b=180)
)

if texts.get('source'):
    fig.add_annotation(
        text=texts['source'],
        showarrow=False,
        xref='paper',
        yref='paper',
        x=0.5,
        y=-0.35,
        xanchor='center',
        yanchor='top',
        align='left',
        font=dict(size=10),
        bordercolor='black',
        borderwidth=1,
        borderpad=4
    )

fig.write_image(output_filename, scale=2)
print(f"Chart saved to {output_filename}")