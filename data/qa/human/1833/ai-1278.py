import sys
import json
import pathlib
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print(f"Usage: python {pathlib.Path(__file__).name} <json_file_path>", file=sys.stderr)
    sys.exit(1)

json_path = pathlib.Path(sys.argv[1])
if not json_path.is_file():
    print(f"Error: File not found at {json_path}", file=sys.stderr)
    sys.exit(1)

with open(json_path, 'r', encoding='utf-8') as f:
    config = json.load(f)

fig = go.Figure()

for i, series in enumerate(config['chart_data']):
    fig.add_trace(go.Scatter(
        x=series['x'],
        y=series['y'],
        name=series['name'],
        mode='lines+markers',
        line=dict(color=config['colors'][i], width=2),
        marker=dict(color=config['colors'][i], size=6)
    ))

annotations = []
for series in config['chart_data']:
    annotations.append(go.layout.Annotation(
        x=series['x'][-1],
        y=series['y'][-1],
        text=series['name'],
        showarrow=False,
        xanchor='left',
        yanchor='middle',
        xshift=10,
        font=dict(family="Arial", size=12),
        bgcolor='rgba(255, 255, 255, 0.85)',
        borderpad=4,
        borderwidth=1,
        bordercolor='#cccccc'
    ))

annotations.append(go.layout.Annotation(
    text=config['texts']['source'],
    xref="paper", yref="paper",
    x=1.0, y=1.0,
    showarrow=False,
    xanchor="right", yanchor="bottom",
    font=dict(family="Arial", size=12, color='#555555')
))

fig.update_layout(
    font_family="Arial",
    title=dict(
        text=f"<b>{config['texts']['title']}</b><span style='font-size:15px;color:grey;'>  {config['texts']['subtitle']}</span>",
        x=0,
        y=1.0,
        xanchor='left',
        yanchor='bottom',
        font=dict(size=22)
    ),
    xaxis=dict(
        tickmode='array',
        tickvals=[2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012],
        range=[2003.5, 2012.9],
        showgrid=False,
        zeroline=False,
        showline=False
    ),
    yaxis=dict(
        range=[42, 69],
        showgrid=True,
        gridcolor='#e5e5e5',
        zeroline=False,
        showline=False,
        ticks='outside',
        tickfont=dict(size=12)
    ),
    plot_bgcolor='#eff6f9',
    paper_bgcolor='white',
    showlegend=False,
    margin=dict(t=100, b=50, l=50, r=50),
    shapes=[
        dict(
            type='line',
            xref='paper', yref='paper',
            x0=0, y0=0.91, x1=1, y1=0.91,
            line=dict(color='black', width=1)
        )
    ],
    annotations=annotations
)

output_filename = json_path.with_suffix('.png').name
fig.write_image(output_filename, scale=2)
print(f"Chart saved to {output_filename}")