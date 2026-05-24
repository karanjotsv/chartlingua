import sys
import json
import pathlib
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <json_file_path>")
    sys.exit(1)

json_path = pathlib.Path(sys.argv[1])
if not json_path.is_file():
    print(f"Error: JSON file not found at '{json_path}'")
    sys.exit(1)

with open(json_path, 'r', encoding='utf-8') as f:
    chart_data = json.load(f)

data = chart_data['chart_data']
categories = chart_data['categories']
texts = chart_data['texts']
colors = chart_data['colors']

fig = go.Figure()

for i, series in enumerate(data):
    fig.add_trace(go.Bar(
        x=categories,
        y=series['y'],
        name=series['name'],
        marker_color=colors[i],
        text=[f"{val}%" for val in series['y']],
        textposition='inside',
        textfont=dict(color='white', family='Arial', size=12, weight='bold'),
        insidetextanchor='middle'
    ))

fig.update_layout(
    barmode='stack',
    bargap=0.35,
    plot_bgcolor='white',
    paper_bgcolor='white',
    font=dict(family="Arial", size=12, color='#000000'),
    margin=dict(l=60, r=40, b=120, t=40, pad=4),
    yaxis=dict(
        title=texts['y_axis_title'],
        range=[0, 125],
        tickvals=[0, 25, 50, 75, 100, 125],
        ticksuffix='%',
        showgrid=True,
        gridcolor='#e0e0e0',
        zeroline=False
    ),
    xaxis=dict(
        title=texts['x_axis_title'],
        showgrid=False,
        tickfont=dict(size=12)
    ),
    legend=dict(
        orientation='h',
        yanchor='bottom',
        y=-0.25,
        xanchor='center',
        x=0.5
    )
)

fig.add_shape(type="line", x0=-0.5, y0=0, x1=2.5, y1=0,
              line=dict(color="black", width=1))

fig.add_vline(x=0.5, line_width=1, line_color='lightgrey')
fig.add_vline(x=1.5, line_width=1, line_color='lightgrey')

if texts.get('source'):
    fig.add_annotation(
        text=texts['source'],
        align='right',
        showarrow=False,
        xref='paper',
        yref='paper',
        x=1,
        y=-0.35,
        font=dict(family="Arial", size=12, color='#666666')
    )

output_filename = json_path.stem + ".png"
fig.write_image(output_filename, scale=2)
print(f"Chart saved as {output_filename}")