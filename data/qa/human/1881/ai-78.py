import sys
import json
import plotly.graph_objects as go
import os

if len(sys.argv) != 2:
    print("Usage: python create_chart.py <json_file_path>")
    sys.exit(1)

json_file_path = sys.argv[1]

try:
    with open(json_file_path, 'r', encoding='utf-8') as f:
        chart_info = json.load(f)
except FileNotFoundError:
    print(f"Error: File not found at {json_file_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Invalid JSON format in {json_file_path}")
    sys.exit(1)

chart_data = chart_info['chart_data']
texts = chart_info['texts']
colors = chart_info['colors']

fig = go.Figure()

for i, series in enumerate(chart_data):
    fig.add_trace(go.Bar(
        x=series['x'],
        y=series['y'],
        marker_color=colors[i],
        text=series['y'],
        textposition='outside',
        texttemplate='%{text}',
        textfont=dict(
            family="Arial",
            size=12,
            color='black'
        ),
        cliponaxis=False
    ))

fig.update_layout(
    font=dict(
        family="Arial",
        size=12,
        color='black'
    ),
    yaxis_title=texts['y_axis_title'],
    xaxis_title=texts['x_axis_title'],
    showlegend=False,
    plot_bgcolor='white',
    xaxis=dict(
        showgrid=False,
        zeroline=False,
        type='category'
    ),
    yaxis=dict(
        showgrid=True,
        gridcolor='#e9e9e9',
        zeroline=False,
        range=[0, 750]
    ),
    margin=dict(l=80, r=40, t=40, b=120),
    annotations=[
        dict(
            text=texts.get('note', ''),
            align='left',
            showarrow=False,
            xref='paper',
            yref='paper',
            x=0,
            y=-0.2,
            xanchor='left',
            yanchor='top'
        ),
        dict(
            text=texts.get('source', ''),
            align='right',
            showarrow=False,
            xref='paper',
            yref='paper',
            x=1,
            y=-0.2,
            xanchor='right',
            yanchor='top'
        )
    ]
)

base_name = os.path.splitext(os.path.basename(json_file_path))[0]
output_filename = f"{base_name}.png"

fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")