import sys
import json
import os
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print("Usage: python script.py <path_to_json_file>")
    sys.exit(1)

json_file_path = sys.argv[1]

with open(json_file_path, 'r', encoding='utf-8') as f:
    config = json.load(f)

chart_data = config['chart_data']
categories = config['categories']
texts = config['texts']
colors = config['colors']

fig = go.Figure()

for i, series in enumerate(chart_data):
    fig.add_trace(go.Bar(
        name=series['name'],
        x=categories,
        y=series['values'],
        marker_color=colors[i]
    ))

fig.update_layout(
    barmode='group',
    plot_bgcolor='white',
    font=dict(family="Arial", size=12),
    xaxis=dict(
        title_text=texts['x_axis_title'],
        showgrid=False,
        showline=True,
        linewidth=1,
        linecolor='black',
    ),
    yaxis=dict(
        title_text=texts['y_axis_title'],
        gridcolor='#dddddd',
        range=[0, 5000],
        zeroline=False,
    ),
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=-0.3,
        xanchor="center",
        x=0.5
    ),
    margin=dict(l=80, r=40, b=150, t=40),
)

if texts.get('note'):
    fig.add_annotation(
        text=texts['note'],
        align='left',
        showarrow=False,
        xref='paper',
        yref='paper',
        x=0,
        y=-0.45,
        xanchor='left',
        yanchor='bottom'
    )

if texts.get('source'):
    fig.add_annotation(
        text=texts['source'],
        align='right',
        showarrow=False,
        xref='paper',
        yref='paper',
        x=1.0,
        y=-0.45,
        xanchor='right',
        yanchor='bottom'
    )

output_filename_base = os.path.splitext(os.path.basename(json_file_path))[0]
output_path = f"{output_filename_base}.png"

fig.write_image(output_path, scale=2)
print(f"Chart saved to {output_path}")