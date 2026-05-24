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

chart_data = chart_config['chart_data']
texts = chart_config['texts']
colors = chart_config['colors']

x_values = [d['x'] for d in chart_data]
y_values = [d['y'] for d in chart_data]

fig = go.Figure()

fig.add_trace(go.Bar(
    x=x_values,
    y=y_values,
    text=y_values,
    textposition='outside',
    texttemplate='%{y}',
    cliponaxis=False,
    marker_color=colors[0],
    hoverinfo='none'
))

fig.update_layout(
    font=dict(family="Arial", size=12),
    plot_bgcolor='white',
    paper_bgcolor='white',
    showlegend=False,
    xaxis=dict(
        title_text=texts.get('x_axis_title'),
        type='category',
        showgrid=False,
        showline=False,
        tickfont=dict(size=12),
        zeroline=False
    ),
    yaxis=dict(
        title_text=texts.get('y_axis_title'),
        range=[0, 45000],
        tickformat=' ',
        gridcolor='#e0e0e0',
        showline=False,
        zeroline=True,
        zerolinecolor='black',
        zerolinewidth=1
    ),
    margin=dict(l=90, r=30, t=30, b=80),
)

if texts.get('source'):
    fig.add_annotation(
        text=texts['source'],
        align='left',
        showarrow=False,
        xref='paper',
        yref='paper',
        x=0.99,
        y=-0.15,
        xanchor='right',
        yanchor='top',
        font=dict(size=12)
    )

fig.update_traces(textfont=dict(family="Arial", size=12, color='black'))

filename_base = pathlib.Path(json_path).stem
output_filename = f"{filename_base}.png"

fig.write_image(output_filename, scale=2, width=800, height=600)

print(f"Chart saved to {output_filename}")