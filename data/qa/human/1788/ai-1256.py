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
        config = json.load(f)
except FileNotFoundError:
    print(f"Error: File not found at {json_file_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Invalid JSON format in {json_file_path}")
    sys.exit(1)

chart_data = config['chart_data']
texts = config['texts']
colors = config['colors']
annotations_data = config.get('annotations', [])

x_values = [d['category'] for d in chart_data]
y_values = [d['value'] for d in chart_data]

fig = go.Figure()

fig.add_trace(go.Bar(
    x=x_values,
    y=y_values,
    marker_color=colors,
    text=[f'{val:.1f}' for val in y_values],
    textposition='outside',
    textfont=dict(family="Arial", size=12, color=colors),
    hoverinfo='none',
    width=0.6
))

title_text = f"<b>{texts['title']}</b><span style='font-size: 18px; color: #555555;'> {texts['subtitle']}</span>"

fig.update_layout(
    title=dict(
        text=title_text,
        y=0.95,
        x=0.01,
        xanchor='left',
        yanchor='top',
        font=dict(size=24)
    ),
    xaxis=dict(
        showgrid=False,
        showline=False,
        showticklabels=False,
        zeroline=False
    ),
    yaxis=dict(
        showgrid=True,
        gridcolor='#D3D3D3',
        zeroline=False,
        range=[0, 60],
        tickvals=[0, 10, 20, 30, 40, 50]
    ),
    plot_bgcolor='#EBF4F8',
    paper_bgcolor='white',
    font=dict(family="Arial", size=12, color='#333333'),
    showlegend=False,
    margin=dict(l=50, r=50, t=120, b=100)
)

fig.add_annotation(
    text=texts['source'],
    align='right',
    showarrow=False,
    xref='paper', yref='paper',
    x=0.99, y=0.98,
    xanchor='right', yanchor='top'
)

for i, category in enumerate(x_values):
    fig.add_annotation(
        x=category,
        y=0,
        text=category,
        showarrow=False,
        yshift=-45,
        textangle=-30,
        font=dict(color=colors[i], size=14)
    )

for ann in annotations_data:
    fig.add_annotation(
        x=ann['x'],
        y=ann['y'],
        text=ann['text'],
        showarrow=True,
        arrowhead=7,
        arrowsize=0.8,
        arrowwidth=1,
        arrowcolor='#636363',
        ax=-70,
        ay=0,
        align=ann.get('align', 'center'),
        bgcolor='white',
        bordercolor='#B0B0B0',
        borderwidth=1,
        borderpad=5
    )

fig.add_shape(
    type="line",
    xref="paper", yref="paper",
    x0=0, y0=0.88, x1=1, y1=0.88,
    line=dict(color="#0095DA", width=2)
)

fig.add_shape(
    type="line",
    xref="paper", yref="paper",
    x0=0, y0=-0.17, x1=1, y1=-0.17,
    line=dict(color="#0095DA", width=4)
)

base_filename = os.path.splitext(os.path.basename(json_file_path))[0]
output_filename = f"{base_filename}.png"

fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")