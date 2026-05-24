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
        chart_info = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_path}")
    sys.exit(1)

chart_data = chart_info['chart_data']
texts = chart_info['texts']
colors = chart_info['colors']

# Reverse data for Plotly's top-to-bottom rendering of horizontal bars
chart_data.reverse()
colors.reverse()

categories = [item['category'] for item in chart_data]
values = [item['value'] for item in chart_data]

fig = go.Figure()

fig.add_trace(go.Bar(
    y=categories,
    x=values,
    orientation='h',
    marker=dict(color=colors),
    text=values,
    textposition='outside',
    cliponaxis=False,
    texttemplate='%{x}'
))

fig.update_layout(
    font=dict(family="Arial", size=12),
    xaxis=dict(
        title=texts.get('x_axis_title'),
        range=[0, 56],
        showgrid=False,
        zeroline=True,
        zerolinecolor='black',
        zerolinewidth=1,
        tickmode='linear',
        tick0=0,
        dtick=5,
        title_font=dict(size=14),
    ),
    yaxis=dict(
        title=texts.get('y_axis_title'),
        showgrid=True,
        gridcolor='lightgray',
    ),
    plot_bgcolor='white',
    paper_bgcolor='white',
    margin=dict(l=120, r=50, t=50, b=80),
    showlegend=False
)

if texts.get('source'):
    fig.add_annotation(
        text=texts['source'],
        align='left',
        showarrow=False,
        xref='paper',
        yref='paper',
        x=1.0,
        y=-0.15,
        xanchor='right',
        yanchor='top',
        font=dict(family="Arial", size=10, color="dimgray")
    )


base_filename = pathlib.Path(json_path).stem
output_filename = f"{base_filename}.png"

fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")