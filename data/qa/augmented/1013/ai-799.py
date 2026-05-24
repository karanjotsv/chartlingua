import sys
import json
import pathlib
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print(f"Usage: python {sys.argv[0]} <json_file_path>")
    sys.exit(1)

json_path = sys.argv[1]
with open(json_path, 'r', encoding='utf-8') as f:
    chart_spec = json.load(f)

chart_data = chart_spec['chart_data']
texts = chart_spec['texts']
colors = chart_spec['colors']

fig = go.Figure()

fig.add_trace(go.Bar(
    x=chart_data['x'],
    y=chart_data['y'],
    text=[str(val) for val in chart_data['y']],
    textposition='outside',
    marker_color=colors[0],
    cliponaxis=False
))

fig.update_layout(
    font=dict(family="Arial", size=12, color="black"),
    title_text=texts.get('title'),
    yaxis_title_text=texts.get('y_axis_title'),
    xaxis_title_text=texts.get('x_axis_title'),
    plot_bgcolor='white',
    paper_bgcolor='white',
    showlegend=False,
    margin=dict(l=80, r=20, t=50, b=100),
    xaxis=dict(
        showgrid=False,
        showline=False,
        showticklabels=True
    ),
    yaxis=dict(
        range=[0, 520],
        tickvals=[0, 100, 200, 300, 400, 500],
        showgrid=True,
        gridcolor='#EAEAEA',
        gridwidth=1,
        showline=False,
        zeroline=False,
        showticklabels=True
    ),
    annotations=[
        dict(
            xref='paper', yref='paper',
            x=0, y=-0.22,
            text=texts.get('note', ''),
            showarrow=False,
            xanchor='left',
            yanchor='bottom',
            align='left',
            font=dict(size=12, color='#007bff')
        ),
        dict(
            xref='paper', yref='paper',
            x=1, y=-0.22,
            text=texts.get('source', ''),
            showarrow=False,
            xanchor='right',
            yanchor='bottom',
            align='right',
            font=dict(size=12, color='#666666')
        )
    ]
)

fig.update_traces(
    textfont=dict(
        family="Arial",
        size=12,
        color='black'
    )
)

output_filename_base = pathlib.Path(json_path).stem
output_png_path = f"{output_filename_base}.png"

fig.write_image(output_png_path, scale=2)

print(f"Chart saved to {output_png_path}")