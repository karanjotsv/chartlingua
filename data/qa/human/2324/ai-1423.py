import sys
import json
import os
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print("Usage: python script.py <path_to_json_file>")
    sys.exit(1)

json_file_path = sys.argv[1]

try:
    with open(json_file_path, 'r', encoding='utf-8') as f:
        chart_config = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_file_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_file_path}")
    sys.exit(1)

data = chart_config['chart_data']
texts = chart_config['texts']
colors = chart_config['colors']

fig = go.Figure()

for i, series in enumerate(data):
    fig.add_trace(go.Scatter(
        x=series['x'],
        y=series['y'],
        name=series['name'],
        mode='lines+markers+text',
        line=dict(color=colors[i]),
        marker=dict(color=colors[i], size=6),
        text=series['y'],
        textposition='top center',
        texttemplate='%{y:.2f}',
        textfont=dict(
            family="Arial",
            size=12,
            color='#555555'
        )
    ))

fig.update_layout(
    font=dict(family="Arial"),
    plot_bgcolor='white',
    paper_bgcolor='white',
    xaxis=dict(
        title_text=texts['x_axis_title'],
        showgrid=False,
        showline=False,
        tickmode='array',
        tickvals=data[0]['x'],
        ticktext=[str(year) for year in data[0]['x']],
        tickfont=dict(size=12),
        linecolor='#cccccc'
    ),
    yaxis=dict(
        title_text=texts['y_axis_title'],
        showgrid=True,
        gridcolor='#e0e0e0',
        gridwidth=1,
        zeroline=False,
        showline=False,
        range=[73.5, 84.5],
        tickfont=dict(size=12)
    ),
    legend=dict(
        orientation="h",
        yanchor="top",
        y=-0.15,
        xanchor="center",
        x=0.5,
        font=dict(size=12)
    ),
    margin=dict(l=80, r=40, t=40, b=100)
)

if texts.get('source'):
    fig.add_annotation(
        text=texts['source'],
        align='right',
        showarrow=False,
        xref='paper',
        yref='paper',
        x=1,
        y=-0.2,
        xanchor='right',
        yanchor='top',
        font=dict(size=10, color='#666666')
    )

base_filename = os.path.splitext(os.path.basename(json_file_path))[0]
output_filename = f"{base_filename}.png"

fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")