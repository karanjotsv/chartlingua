import sys
import json
import plotly.graph_objects as go
import pathlib

if len(sys.argv) != 2:
    sys.exit("Usage: python <script_name>.py <json_file_path>")

json_path = sys.argv[1]
output_filename_base = pathlib.Path(json_path).stem

with open(json_path, 'r', encoding='utf-8') as f:
    config = json.load(f)

data = config['chart_data']
texts = config['texts']
colors = config['colors']

x_values = [d['year'] for d in data]
y_values = [d['value'] for d in data]

fig = go.Figure()

fig.add_trace(go.Bar(
    x=x_values,
    y=y_values,
    text=y_values,
    textposition='outside',
    marker_color=colors[0],
    cliponaxis=False,
    textfont=dict(family="Arial", size=12, color='black')
))

fig.update_layout(
    font_family="Arial",
    plot_bgcolor='white',
    showlegend=False,
    margin=dict(l=90, r=40, t=60, b=80),
    xaxis=dict(
        tickmode='array',
        tickvals=x_values,
        ticktext=[str(x) for x in x_values],
        showline=False,
        showgrid=False
    ),
    yaxis=dict(
        title_text=texts['y_axis_title'],
        range=[0, 1550],
        tickmode='array',
        tickvals=[0, 250, 500, 750, 1000, 1250, 1500],
        gridcolor='#e5e5e5',
        showline=False,
        zeroline=False
    ),
    annotations=[
        dict(
            text=texts.get('source'),
            align='right',
            showarrow=False,
            xref='paper',
            yref='paper',
            x=1.0,
            y=-0.18,
            xanchor='right',
            yanchor='top',
            font=dict(family="Arial", size=12)
        )
    ] if texts.get('source') else []
)

output_image_path = f"{output_filename_base}.png"
fig.write_image(output_image_path, scale=2)

print(f"Chart saved to {output_image_path}")