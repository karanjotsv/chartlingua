import sys
import json
import pathlib
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print("Usage: python script.py <path_to_json_file>")
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
    marker_color=colors[0] if colors else None,
    texttemplate='%{y}%',
    textposition='outside',
    hoverinfo='none',
    cliponaxis=False 
))

fig.update_traces(
    textfont=dict(
        family="Arial",
        size=12,
        color='black'
    )
)
# Manually make the text on top of the bars bold
fig.data[0].textfont.family = "Arial, bold"

fig.update_layout(
    font=dict(family="Arial"),
    plot_bgcolor='white',
    paper_bgcolor='white',
    showlegend=False,
    margin=dict(l=80, r=40, t=40, b=150),
    xaxis=dict(
        title_text=texts.get('x_axis_title'),
        tickangle=-45,
        showgrid=False,
        linecolor='black'
    ),
    yaxis=dict(
        title_text=texts.get('y_axis_title'),
        range=[0, 80],
        tickvals=[0, 20, 40, 60, 80],
        ticksuffix='%',
        gridcolor='#e0e0e0'
    ),
    annotations=[
        dict(
            text=texts.get('source'),
            showarrow=False,
            xref='paper',
            yref='paper',
            x=1.0,
            y=-0.3,
            xanchor='right',
            yanchor='top',
            align='right',
            font=dict(size=10)
        )
    ]
)

output_filename = pathlib.Path(json_path).stem + ".png"
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")