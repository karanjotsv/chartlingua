import sys
import json
import os
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print("Usage: python create_chart.py <path_to_json_file>")
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

chart_data = config['chart_data']
texts = config['texts']
colors = config['colors']

fig = go.Figure()

x_values = [d['x'] for d in chart_data]
y_values = [d['y'] for d in chart_data]

fig.add_trace(go.Bar(
    x=x_values,
    y=y_values,
    texttemplate='%{y}%',
    textposition='outside',
    marker_color=colors[0],
    cliponaxis=False,
    width=0.7
))

fig.update_traces(
    textfont=dict(
        family='Arial',
        size=12,
        color='black',
        weight='bold'
    )
)

max_y_value = max(y_values)

fig.update_layout(
    font=dict(family="Arial", size=12, color="#333333"),
    plot_bgcolor='white',
    showlegend=False,
    xaxis=dict(
        title_text=texts.get('x_axis_title'),
        showgrid=False,
        linecolor='black',
        zeroline=False,
        tickfont=dict(size=12)
    ),
    yaxis=dict(
        title_text=texts.get('y_axis_title'),
        showgrid=True,
        gridcolor='#e9e9e9',
        range=[0, max_y_value * 1.15],
        ticksuffix='%',
        dtick=1,
        zeroline=False
    ),
    margin=dict(l=60, r=20, t=30, b=100),
    annotations=[]
)

annotations = []
if texts.get('note'):
    annotations.append(
        go.layout.Annotation(
            xref='paper', yref='paper',
            x=0, y=0,
            xanchor='left', yanchor='top',
            yshift=-25,
            text=texts['note'],
            showarrow=False,
            font=dict(family="Arial", size=12)
        )
    )

if texts.get('source'):
    annotations.append(
        go.layout.Annotation(
            xref='paper', yref='paper',
            x=1, y=0,
            xanchor='right', yanchor='top',
            yshift=-25,
            text=texts['source'],
            align='right',
            showarrow=False,
            font=dict(family="Arial", size=12, color="#888888")
        )
    )

fig.update_layout(annotations=annotations)

base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_image_path = f"{base_filename}.png"

fig.write_image(output_image_path, scale=2)

print(f"Chart saved to {output_image_path}")