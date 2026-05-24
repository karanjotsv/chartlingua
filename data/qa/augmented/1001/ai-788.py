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
        chart_info = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)

chart_data = chart_info['chart_data']
texts = chart_info['texts']
colors = chart_info['colors']

fig = go.Figure()

for i, series in enumerate(chart_data):
    fig.add_trace(go.Scatter(
        x=series['x'],
        y=series['y'],
        mode='lines+markers+text',
        line=dict(color=colors[i], width=2.5),
        marker=dict(color=colors[i], size=6),
        text=series['labels'],
        textposition='top center',
        textfont=dict(
            family="Arial",
            size=12,
            color='black'
        ),
        name=''
    ))

x_tick_vals = [val for idx, val in enumerate(chart_data[0]['x']) if idx % 2 == 0]

fig.update_layout(
    font=dict(family="Arial"),
    plot_bgcolor='white',
    xaxis=dict(
        type='category',
        tickvals=x_tick_vals,
        showgrid=False,
        zeroline=False,
        linecolor='lightgray',
        tickfont=dict(size=12)
    ),
    yaxis=dict(
        title=texts['y_axis_title'],
        range=[0, 4.2],
        tickvals=[0, 0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4],
        showgrid=True,
        gridcolor='#EAEAEA',
        gridwidth=1,
        zeroline=False,
        linecolor='lightgray'
    ),
    showlegend=False,
    margin=dict(l=90, r=40, t=40, b=120)
)

if texts['source']:
    fig.add_annotation(
        text=texts['source'],
        align='right',
        showarrow=False,
        xref='paper', yref='paper',
        x=1.0, y=-0.2,
        xanchor='right', yanchor='top',
        font=dict(family="Arial", size=12)
    )

base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_filename}.png"

fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")