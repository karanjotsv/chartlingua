import sys
import json
import pathlib
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print(f"Usage: python {sys.argv[0]} <json_file_path>")
    sys.exit(1)

json_file_path = sys.argv[1]
json_path = pathlib.Path(json_file_path)
output_png_path = json_path.with_suffix('.png')

try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_info = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_path}")
    sys.exit(1)

data = chart_info['chart_data']
texts = chart_info['texts']
colors = chart_info['colors']

x_values = [d['x'] for d in data]
y_values = [d['y'] for d in data]

fig = go.Figure()

fig.add_trace(go.Bar(
    x=x_values,
    y=y_values,
    marker_color=colors[0],
    text=y_values,
    texttemplate='%{text:.2f}',
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
    plot_bgcolor='white',
    paper_bgcolor='white',
    showlegend=False,
    margin=dict(l=80, r=40, t=40, b=80),
    xaxis=dict(
        tickmode='array',
        tickvals=x_values,
        tickangle=0,
        showgrid=False,
        linecolor='black',
        linewidth=1
    ),
    yaxis=dict(
        title_text=texts['y_axis_title'],
        range=[0, 250],
        showgrid=True,
        gridcolor='#E5E5E5',
        zeroline=False,
        linecolor='black',
        linewidth=1
    )
)

fig.add_annotation(
        text=texts['source'],
        align='right',
        showarrow=False,
        xref='paper',
        yref='paper',
        x=1.0,
        y=-0.15,
        xanchor='right',
        yanchor='top'
)

fig.write_image(str(output_png_path), scale=2)

print(f"Chart saved to {output_png_path}")