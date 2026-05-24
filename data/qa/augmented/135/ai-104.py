import sys
import json
import plotly.graph_objects as go
from pathlib import Path

if len(sys.argv) != 2:
    print("Usage: python create_chart.py <path_to_json_file>")
    sys.exit(1)

json_path = Path(sys.argv[1])
if not json_path.is_file():
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)

with open(json_path, 'r', encoding='utf-8') as f:
    config = json.load(f)

chart_data = config['chart_data']
texts = config['texts']
colors = config['colors']

fig = go.Figure()

for i, series in enumerate(chart_data):
    # Format text labels to match original (e.g., 4.0 becomes 4)
    text_labels = [f'{y if y % 1 else int(y)}' for y in series['y']]
    
    fig.add_trace(go.Bar(
        x=series['x'],
        y=series['y'],
        marker_color=colors[i % len(colors)],
        text=text_labels,
        textposition='outside',
        cliponaxis=False,
        textfont=dict(family="Arial", size=12, color='#000000')
    ))

annotations = []
if texts.get('source'):
    annotations.append(
        dict(
            text=texts['source'],
            align='right',
            showarrow=False,
            xref='paper',
            yref='paper',
            x=1,
            y=-0.15,
            xanchor='right',
            yanchor='top',
            font=dict(family="Arial", size=12, color='grey')
        )
    )

fig.update_layout(
    font=dict(family="Arial"),
    title_text=texts.get('title'),
    yaxis_title_text=texts.get('y_axis_title'),
    showlegend=False,
    plot_bgcolor='white',
    paper_bgcolor='white',
    yaxis=dict(
        range=[0, 6],
        showgrid=True,
        gridcolor='#EAEAEA',
        gridwidth=1,
        griddash='dot',
        zeroline=False,
        tickfont=dict(size=12),
        title_font=dict(size=14)
    ),
    xaxis=dict(
        showgrid=False,
        zeroline=False,
        tickfont=dict(size=12)
    ),
    margin=dict(l=90, r=40, t=40, b=100),
    annotations=annotations
)

output_path = json_path.with_suffix('.png')
fig.write_image(output_path, scale=2)

print(f"Chart saved to {output_path}")