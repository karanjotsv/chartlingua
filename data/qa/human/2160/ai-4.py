import sys
import json
from pathlib import Path
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print("Usage: python recreate_chart.py <path_to_json_file>")
    sys.exit(1)

json_path = Path(sys.argv[1])
if not json_path.is_file():
    print(f"Error: File not found at {json_path}")
    sys.exit(1)

with open(json_path, 'r', encoding='utf-8') as f:
    chart_info = json.load(f)

chart_data = chart_info['chart_data']
texts = chart_info['texts']
colors = chart_info['colors']

fig = go.Figure()

for i, series in enumerate(chart_data):
    color = colors[i]
    fig.add_trace(go.Scatter(
        x=series['x'],
        y=series['y'],
        name=series['name'],
        mode='lines+markers',
        line=dict(color=color, width=2),
        marker=dict(color=color, size=6)
    ))

    # Add data point annotations
    for ann in series.get('annotations', []):
        fig.add_annotation(
            x=ann['x'],
            y=ann['y'],
            text=ann['text'],
            showarrow=False,
            font=dict(
                family="Arial",
                size=11,
                color=color
            ),
            yshift=12 if series['name'] == 'Female' else -12
        )

fig.update_layout(
    plot_bgcolor='white',
    font=dict(family="Arial", size=12, color='#555555'),
    xaxis=dict(
        tickmode='array',
        tickvals=chart_data[0]['x'],
        ticktext=[str(year) for year in chart_data[0]['x']],
        showgrid=True,
        gridcolor='#F0F0F0',
        gridwidth=1,
        linecolor='lightgray'
    ),
    yaxis=dict(
        title=texts['y_axis_title'],
        range=[50, 85],
        dtick=5,
        ticksuffix='%',
        showgrid=True,
        gridcolor='#F0F0F0',
        griddash='dash',
        gridwidth=1,
        linecolor='lightgray'
    ),
    legend=dict(
        orientation="h",
        yanchor="top",
        y=-0.2,
        xanchor="center",
        x=0.5
    ),
    margin=dict(l=80, r=40, t=40, b=120),
    height=600
)

# Add source text as an annotation
if texts.get('source'):
    fig.add_annotation(
        text=texts['source'],
        xref="paper", yref="paper",
        x=1, y=-0.25,
        xanchor='right', yanchor='bottom',
        showarrow=False,
        font=dict(size=12, color='gray')
    )

output_filename = json_path.with_suffix(".png")
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")