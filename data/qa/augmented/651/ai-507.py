import sys
import json
import os
import plotly.graph_objects as go

# This script requires plotly and kaleido to be installed:
# pip install plotly kaleido

if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <path_to_json_file>")
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

fig = go.Figure()

for i, series in enumerate(chart_info['chart_data']):
    fig.add_trace(go.Bar(
        x=series['x'],
        y=series['y'],
        name=series.get('name', ''),
        marker_color=chart_info['colors'][i]
    ))

title_text = ""
if chart_info['texts'].get('title'):
    title_text += f"<b>{chart_info['texts']['title']}</b>"
if chart_info['texts'].get('subtitle'):
    title_text += f"<br><sub>{chart_info['texts']['subtitle']}</sub>"

fig.update_layout(
    title_text=title_text if title_text else None,
    title_x=0.05,
    font_family="Arial",
    xaxis_title_text=chart_info['texts'].get('x_axis_title'),
    yaxis_title_text=chart_info['texts'].get('y_axis_title'),
    yaxis=dict(
        range=[0, 600],
        tickmode='linear',
        dtick=100,
        showgrid=True,
        gridcolor='#e0e0e0',
        gridwidth=1
    ),
    xaxis=dict(
        showgrid=False,
        tickfont=dict(size=12),
        type='category'
    ),
    plot_bgcolor='white',
    showlegend=False,
    margin=dict(l=90, r=40, t=50, b=100),
    bargap=0.2
)

if chart_info['texts'].get('source'):
    fig.add_annotation(
        text=chart_info['texts']['source'],
        xref="paper",
        yref="paper",
        x=0.98,
        y=-0.18,
        showarrow=False,
        xanchor='right',
        yanchor='top',
        align='right',
        font=dict(
            family="Arial",
            size=10,
            color="#666666"
        )
    )

base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_filename}.png"

fig.write_image(output_filename, scale=2)
print(f"Chart saved to {output_filename}")