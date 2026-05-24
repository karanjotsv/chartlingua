import sys
import json
import pathlib
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print(f"Usage: python {sys.argv[0]} <json_file_path>")
    sys.exit(1)

json_path = sys.argv[1]

with open(json_path, 'r', encoding='utf-8') as f:
    config = json.load(f)

chart_data = config.get('chart_data', [])
texts = config.get('texts', {})
colors = config.get('colors', [])

categories = [item['category'] for item in chart_data]
values = [item['value'] for item in chart_data]
bar_color = colors[0] if colors else '#1F77B4'

fig = go.Figure()

fig.add_trace(go.Bar(
    x=categories,
    y=values,
    text=values,
    textposition='outside',
    marker_color=bar_color,
    textfont=dict(family="Arial", size=12, color='black', weight='bold'),
    cliponaxis=False
))

fig.update_layout(
    font=dict(family="Arial", size=12, color="black"),
    plot_bgcolor='white',
    showlegend=False,
    xaxis=dict(
        tickangle=-45,
        showline=False,
        showgrid=False
    ),
    yaxis=dict(
        title_text=texts.get('y_axis_title'),
        range=[0, 80],
        tickvals=[0, 20, 40, 60, 80],
        showgrid=True,
        gridcolor='#EAEAEA',
        gridwidth=1,
        zeroline=False,
        showline=False
    ),
    margin=dict(l=80, r=20, t=40, b=120),
    annotations=[
        dict(
            showarrow=False,
            text=texts.get('source', ''),
            xref="paper", yref="paper",
            x=1, y=-0.32,
            xanchor='right', yanchor='bottom',
            align='right',
            font=dict(family="Arial", size=12)
        )
    ]
)

output_filename_base = pathlib.Path(json_path).stem
output_filename = f"{output_filename_base}.png"

fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")