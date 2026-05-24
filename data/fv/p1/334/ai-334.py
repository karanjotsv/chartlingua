import sys
import json
import pathlib
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print("Usage: python script.py <path_to_json_file>")
    sys.exit(1)

json_path_str = sys.argv[1]
json_path = pathlib.Path(json_path_str)

if not json_path.is_file():
    print(f"Error: JSON file not found at '{json_path_str}'")
    sys.exit(1)

with open(json_path, 'r', encoding='utf-8') as f:
    chart_spec = json.load(f)

chart_data = chart_spec['chart_data']
texts = chart_spec['texts']
colors = chart_spec['colors']

fig = go.Figure()

for i, series in enumerate(chart_data['series']):
    fig.add_trace(go.Bar(
        name=series['name'],
        x=chart_data['categories'],
        y=series['values'],
        marker_color=colors[i]
    ))

fig.update_layout(
    barmode='group',
    title=dict(
        text=texts['title'],
        x=0.5,
        font=dict(
            color='white'
        )
    ),
    xaxis=dict(
        tickangle=-90,
        showgrid=False,
        tickfont=dict(color='white')
    ),
    yaxis=dict(
        range=[0, 220],
        gridcolor='rgba(255, 255, 255, 0.2)',
        showline=False,
        zeroline=False,
        tickfont=dict(color='white')
    ),
    plot_bgcolor='black',
    paper_bgcolor='black',
    font=dict(family="Arial"),
    showlegend=False,
    margin=dict(l=50, r=50, t=80, b=200),
    annotations=[
        dict(
            text=texts['note'],
            showarrow=False,
            xref='paper',
            yref='paper',
            x=0,
            y=-0.4,  
            xanchor='left',
            yanchor='bottom',
            font=dict(color='white', size=12)
        ),
        dict(
            text=texts['source'],
            showarrow=False,
            xref='paper',
            yref='paper',
            x=1,
            y=-0.4,
            xanchor='right',
            yanchor='bottom',
            font=dict(color='white', size=12)
        )
    ]
)

output_filename = f"{json_path.stem}.png"
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")