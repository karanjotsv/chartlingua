import sys
import json
import os
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print("Usage: python this_script.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]

if not os.path.exists(json_path):
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)

base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_filename}.png"

with open(json_path, 'r', encoding='utf-8') as f:
    chart_info = json.load(f)

chart_data = chart_info['chart_data']
texts = chart_info['texts']
colors = chart_info['colors']

categories = [item['category'] for item in chart_data]
values = [item['value'] for item in chart_data]

fig = go.Figure()

fig.add_trace(go.Bar(
    y=categories,
    x=values,
    orientation='h',
    marker=dict(color=colors[0]),
    text=values,
    textposition='outside',
    textfont=dict(family='Arial', size=12, color='black'),
    cliponaxis=False
))

fig.update_layout(
    xaxis_title=texts['x_axis_title'],
    yaxis_title=texts['y_axis_title'],
    font=dict(family="Arial", size=12, color='black'),
    showlegend=False,
    plot_bgcolor='white',
    paper_bgcolor='white',
    margin=dict(l=220, r=60, t=30, b=80),
    xaxis=dict(
        showgrid=True,
        gridcolor='#e9e9e9',
        gridwidth=1,
        griddash='dot',
        zeroline=False,
        showline=False,
        range=[0, max(values) * 1.3]
    ),
    yaxis=dict(
        showgrid=False,
        showline=True,
        linewidth=1,
        linecolor='black',
        autorange='reversed'
    ),
    annotations=[
        dict(
            text=texts['source'],
            showarrow=False,
            xref='paper',
            yref='paper',
            x=0.98,
            y=-0.15,
            xanchor='right',
            yanchor='top',
            font=dict(family="Arial", size=12, color='#666666')
        )
    ]
)

fig.write_image(output_filename, scale=2, width=800, height=600)

print(f"Chart saved to {output_filename}")