import sys
import json
import os
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print(f"Usage: python {os.path.basename(__file__)} <json_file_path>")
    sys.exit(1)

json_path = sys.argv[1]

try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_config = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_path}")
    sys.exit(1)

chart_data = chart_config.get('chart_data', [])
texts = chart_config.get('texts', {})
colors = chart_config.get('colors', [])

fig = go.Figure()

for i, series in enumerate(chart_data):
    fig.add_trace(go.Scatter(
        x=series.get('x'),
        y=series.get('y'),
        mode='lines',
        name=series.get('name'),
        line=dict(color=colors[i] if i < len(colors) else None, width=1.5)
    ))

fig.update_layout(
    font=dict(family="Arial", size=12, color="black"),
    title_text=texts.get('title'),
    plot_bgcolor='white',
    paper_bgcolor='white',
    xaxis=dict(
        title_text=texts.get('x_axis_title'),
        range=[0, 500],
        tickmode='linear',
        dtick=100,
        showline=True,
        linewidth=1,
        linecolor='black',
        mirror=True,
        ticks='inside',
        showgrid=False
    ),
    yaxis=dict(
        title_text=texts.get('y_axis_title'),
        range=[-100, 0],
        tickmode='linear',
        dtick=10,
        showline=True,
        linewidth=1,
        linecolor='black',
        mirror=True,
        ticks='inside',
        showgrid=False,
        zeroline=False
    ),
    legend=dict(
        x=0.98,
        y=0.98,
        xanchor='right',
        yanchor='top',
        bgcolor='rgba(255, 255, 255, 0)',
        bordercolor='rgba(0,0,0,0)',
        borderwidth=0
    ),
    margin=dict(l=40, r=20, t=40, b=40)
)

base_name = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_name}.png"

fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")