import sys
import json
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print(f"Usage: python {sys.argv[0]} <json_file_path>")
    sys.exit(1)

json_file_path = sys.argv[1]

try:
    with open(json_file_path, 'r', encoding='utf-8') as f:
        config = json.load(f)
except FileNotFoundError:
    print(f"Error: File not found at {json_file_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Invalid JSON format in {json_file_path}")
    sys.exit(1)

chart_data = config['chart_data']
texts = config['texts']
colors = config['colors']

x_values = [d['x'] for d in chart_data]
y_values = [d['y'] for d in chart_data]

fig = go.Figure()

fig.add_trace(go.Bar(
    x=x_values,
    y=y_values,
    text=[f'{val}' for val in y_values],
    textposition='outside',
    cliponaxis=False,
    marker_color=colors[0],
    textfont=dict(family="Arial", size=12, color='black')
))

fig.update_layout(
    font=dict(family="Arial", size=12),
    title_text=texts.get('title') or '',
    yaxis_title_text=texts.get('y_axis_title'),
    xaxis_title_text=texts.get('x_axis_title'),
    plot_bgcolor='white',
    paper_bgcolor='white',
    showlegend=False,
    margin=dict(l=80, r=40, t=40, b=150),
    xaxis=dict(
        showline=True,
        linewidth=1,
        linecolor='black',
        showgrid=True,
        gridcolor='#f0f0f0',
        gridwidth=1
    ),
    yaxis=dict(
        showgrid=True,
        gridcolor='#e0e0e0',
        range=[0, 26],
        tickvals=[0, 5, 10, 15, 20, 25],
        zeroline=False
    ),
    annotations=[
        dict(
            showarrow=False,
            text=texts.get('source', ''),
            xref='paper',
            yref='paper',
            x=1,
            y=-0.28,
            xanchor='right',
            yanchor='top',
            font=dict(family="Arial", size=12, color='grey')
        )
    ]
)

if json_file_path.endswith('.json'):
    output_filename = json_file_path[:-5] + '.png'
else:
    output_filename = json_file_path + '.png'

fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")