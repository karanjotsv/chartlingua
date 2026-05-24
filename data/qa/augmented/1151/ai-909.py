import sys
import json
import plotly.graph_objects as go
from pathlib import Path

if len(sys.argv) != 2:
    print("Usage: python <script.py> <path_to_json_file>")
    sys.exit(1)

json_path_str = sys.argv[1]
json_path = Path(json_path_str)
output_filename = json_path.stem + ".png"

try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_info = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_path_str}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_path_str}")
    sys.exit(1)

chart_data = chart_info['chart_data']
texts = chart_info['texts']
colors = chart_info['colors']

categories = [item['category'] for item in chart_data]
values = [item['value'] for item in chart_data]

# Reverse data for correct top-to-bottom display in Plotly horizontal bar chart
categories.reverse()
values.reverse()

# Format numeric labels with spaces as thousand separators
text_labels = [f'{v:,}'.replace(',', ' ') for v in values]

fig = go.Figure()

fig.add_trace(go.Bar(
    y=categories,
    x=values,
    orientation='h',
    marker=dict(
        color=colors[0],
        line=dict(width=0)
    ),
    text=text_labels,
    textposition='outside',
    cliponaxis=False,
    hoverinfo='none',
    textfont=dict(
        family="Arial",
        size=12
    )
))

fig.update_layout(
    plot_bgcolor='white',
    paper_bgcolor='white',
    font=dict(family="Arial", size=12),
    xaxis=dict(
        title=texts.get('xaxis_title'),
        showgrid=True,
        gridcolor='#EAEAEA',
        gridwidth=1,
        zeroline=False,
        tickangle=-45,
        range=[0, 950000]
    ),
    yaxis=dict(
        showgrid=False,
        zeroline=False,
        showline=True,
        linecolor='black',
        linewidth=1
    ),
    margin=dict(l=260, r=50, t=30, b=80),
    showlegend=False
)

if texts.get('source'):
    fig.add_annotation(
        text=texts['source'],
        showarrow=False,
        xref="paper",
        yref="paper",
        x=1,
        y=-0.18,
        xanchor='right',
        yanchor='top',
        align='right',
        font=dict(size=12)
    )

fig.write_image(output_filename, scale=2)
print(f"Chart saved to {output_filename}")