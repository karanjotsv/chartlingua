import sys
import json
import pathlib
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <json_file_path>")
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
    y=categories,
    x=values,
    orientation='h',
    marker=dict(color=colors[0]),
    text=[f"{v}%" for v in values],
    textposition='outside',
    cliponaxis=False,
    hoverinfo='none'
))

fig.update_layout(
    font=dict(
        family="Arial",
        size=12,
        color="black"
    ),
    plot_bgcolor='#F8F8F8',
    paper_bgcolor='white',
    margin=dict(l=100, r=50, t=30, b=80),
    xaxis=dict(
        title=texts.get('x_axis_title'),
        title_font=dict(size=12),
        showgrid=True,
        gridcolor='#E0E0E0',
        gridwidth=1,
        range=[0, 27.5],
        dtick=2.5,
        ticksuffix='%',
        zeroline=False
    ),
    yaxis=dict(
        autorange='reversed',
        showgrid=False,
        ticks='outside',
        ticklen=5,
        tickcolor='lightgrey'
    ),
    showlegend=False,
    annotations=[
        dict(
            text=texts.get('source'),
            showarrow=False,
            xref="paper",
            yref="paper",
            x=0.98,
            y=-0.15,
            xanchor='right',
            yanchor='top',
            font=dict(size=11, color='#666666')
        )
    ]
)

base_filename = pathlib.Path(json_path).stem
output_filename = f"{base_filename}.png"
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")