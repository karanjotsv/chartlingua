import sys
import json
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print(f"Usage: python {sys.argv[0]} <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]
output_filename = json_path.rsplit('.', 1)[0] + '.png'

try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_spec = json.load(f)
except FileNotFoundError:
    print(f"Error: File not found at {json_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print("Error: Invalid JSON format.")
    sys.exit(1)

data = chart_spec['chart_data']
texts = chart_spec['texts']
colors = chart_spec['colors']
categories = data['categories']
series_values = data['series'][0]['values']

fig = go.Figure()

text_positions = ['outside' if v == 0 else 'inside' for v in series_values]

fig.add_trace(go.Bar(
    x=categories,
    y=series_values,
    text=series_values,
    textposition=text_positions,
    texttemplate='%{text}',
    marker_color=colors[0],
    insidetextanchor='end',
    textfont=dict(family="Arial", size=12, color='black'),
    hoverinfo='none'
))

fig.update_layout(
    font=dict(family="Arial", size=12, color="black"),
    title_text=texts['title'],
    plot_bgcolor='white',
    paper_bgcolor='#f5f5f5',
    showlegend=False,
    xaxis=dict(
        title_text=texts['x_axis_title'],
        showline=True,
        linewidth=1,
        linecolor='black',
        tickfont=dict(size=11)
    ),
    yaxis=dict(
        title_text=texts['y_axis_title'],
        range=[0, 26],
        dtick=5,
        gridcolor='#e0e0e0',
        zeroline=False,
        tickfont=dict(size=11)
    ),
    margin=dict(l=80, r=40, t=40, b=100),
    annotations=[
        dict(
            text=texts['source'],
            align='right',
            showarrow=False,
            xref='paper',
            yref='paper',
            x=1.0,
            y=-0.22,
            xanchor='right',
            yanchor='top',
            font=dict(family="Arial", size=10)
        )
    ]
)

fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")