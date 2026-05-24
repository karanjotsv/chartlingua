import sys
import json
from pathlib import Path
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print("Usage: python create_chart.py <json_file_path>")
    sys.exit(1)

json_file_path = sys.argv[1]
base_filename = Path(json_file_path).stem

try:
    with open(json_file_path, 'r', encoding='utf-8') as f:
        chart_info = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_file_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_file_path}")
    sys.exit(1)

chart_data = chart_info.get('chart_data', [])
texts = chart_info.get('texts', {})
colors = chart_info.get('colors', [])

fig = go.Figure()

for i, series in enumerate(chart_data):
    y_values = series.get('y', [])
    text_labels = [f"{y:.2f}".rstrip('0').rstrip('.') for y in y_values]
    
    fig.add_trace(go.Scatter(
        x=series.get('x', []),
        y=y_values,
        mode='lines+markers+text',
        line=dict(color=colors[i % len(colors)], width=3),
        marker=dict(color=colors[i % len(colors)], size=8),
        text=text_labels,
        textposition='top center',
        textfont=dict(
            family="Arial",
            size=12,
            color='black'
        ),
        hoverinfo='none'
    ))

annotations = []
if texts.get('source'):
    annotations.append(
        dict(
            text=texts['source'],
            showarrow=False,
            xref="paper",
            yref="paper",
            x=0.99,
            y=-0.15,
            xanchor='right',
            yanchor='top',
            font=dict(family="Arial", size=12)
        )
    )

fig.update_layout(
    font=dict(family="Arial", size=12),
    title=dict(
        text=texts.get('title'),
        x=0.05,
        xanchor='left'
    ),
    xaxis=dict(
        title_text=texts.get('x_axis_title'),
        showgrid=True,
        gridcolor='#EAEAEA',
        gridwidth=1,
        zeroline=False,
        type='category'
    ),
    yaxis=dict(
        title_text=texts.get('y_axis_title'),
        showgrid=True,
        gridcolor='#EAEAEA',
        gridwidth=1,
        zeroline=False,
        tickformat=".1f"
    ),
    showlegend=False,
    plot_bgcolor='white',
    paper_bgcolor='#F8F9FA',
    margin=dict(l=80, r=40, t=40, b=80),
    annotations=annotations
)

output_filename = f"{base_filename}.png"
fig.write_image(output_filename, scale=2)
print(f"Chart saved to {output_filename}")