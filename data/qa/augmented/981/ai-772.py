import sys
import json
import pathlib
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print("Usage: python script.py <path_to_json>")
    sys.exit(1)

json_path = sys.argv[1]

try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_config = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_path}")
    sys.exit(1)


chart_data = chart_config.get('chart_data', [])
texts = chart_config.get('texts', {})
colors = chart_config.get('colors', [])

categories = [item['category'] for item in chart_data]
values = [item['value'] for item in chart_data]

fig = go.Figure()

fig.add_trace(go.Bar(
    x=categories,
    y=values,
    text=values,
    textposition='outside',
    marker_color=colors[0] if colors else None,
    cliponaxis=False 
))

fig.update_layout(
    font=dict(family="Arial"),
    title_text=texts.get('title'),
    yaxis_title_text=texts.get('yaxis_title'),
    xaxis_title_text=texts.get('xaxis_title'),
    plot_bgcolor='white',
    paper_bgcolor='white',
    showlegend=False,
    xaxis=dict(
        showgrid=True,
        gridcolor='#e9e9e9',
        zeroline=False,
        tickmode='array',
        tickvals=categories,
        ticktext=[str(c) for c in categories]
    ),
    yaxis=dict(
        range=[0, 400],
        showgrid=True,
        gridcolor='#e9e9e9',
        zeroline=False
    ),
    margin=dict(l=80, r=40, t=50, b=80),
    annotations=[
        dict(
            showarrow=False,
            text=texts.get('source', ''),
            xref='paper',
            yref='paper',
            x=1.0,
            y=-0.20,
            xanchor='right',
            yanchor='top',
            font=dict(size=12, color='#666666')
        )
    ]
)

output_filename = pathlib.Path(json_path).stem + '.png'
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")