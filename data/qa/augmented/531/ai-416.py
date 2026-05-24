import sys
import json
import pathlib
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print("Usage: python <script_name>.py <path_to_json>")
    sys.exit(1)

json_path = pathlib.Path(sys.argv[1])
if not json_path.is_file():
    print(f"Error: File not found at {json_path}")
    sys.exit(1)

with open(json_path, 'r', encoding='utf-8') as f:
    config = json.load(f)

chart_data = config['chart_data']
texts = config['texts']
colors = config['colors']

x_values = [item['x'] for item in chart_data]
y_values = [item['y'] for item in chart_data]

fig = go.Figure()

fig.add_trace(go.Bar(
    x=x_values,
    y=y_values,
    text=y_values,
    textposition='outside',
    marker_color=colors[0],
    cliponaxis=False
))

fig.update_traces(
    texttemplate='%{text}',
    textfont=dict(family="Arial", size=12, color='black')
)

fig.update_layout(
    font=dict(family="Arial", size=12, color="#333"),
    plot_bgcolor='white',
    paper_bgcolor='white',
    showlegend=False,
    margin=dict(l=80, r=40, b=80, t=50),
    xaxis=dict(
        title_text=texts.get('x_axis_title'),
        showgrid=False,
        showline=True,
        linewidth=1,
        linecolor='black',
        zeroline=False,
        tickvals=x_values,
        ticktext=[str(x) for x in x_values]
    ),
    yaxis=dict(
        title_text=texts.get('y_axis_title'),
        gridcolor='#e5e5e5',
        showline=False,
        zeroline=False,
        range=[0, 50000]
    ),
    annotations=[
        dict(
            text=texts.get('source', ''),
            align='right',
            showarrow=False,
            xref='paper',
            yref='paper',
            x=1.0,
            y=-0.18,
            xanchor='right',
            yanchor='top',
            font=dict(size=10, color="#666")
        )
    ]
)

# Add faint vertical separator lines between the bars
for year in [x + 0.5 for x in x_values[:-1]]:
    fig.add_shape(
        type="line",
        x0=year, y0=0, x1=year, y1=1,
        xref="x", yref="paper",
        line=dict(color="#f0f0f0", width=1)
    )

output_filename = json_path.stem + '.png'
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")