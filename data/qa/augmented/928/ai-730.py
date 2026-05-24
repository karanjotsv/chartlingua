import sys
import json
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print(f"Usage: python {sys.argv[0]} <json_file_path>")
    sys.exit(1)

json_path = sys.argv[1]

try:
    with open(json_path, 'r', encoding='utf-8') as f:
        config = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at '{json_path}'")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from '{json_path}'")
    sys.exit(1)

chart_data = config.get('chart_data', [])
texts = config.get('texts', {})
colors = config.get('colors', [])

fig = go.Figure()

fig.add_trace(go.Bar(
    x=[d['x'] for d in chart_data],
    y=[d['y'] for d in chart_data],
    marker_color=colors[0] if colors else '#1f77b4',
    name=''
))

fig.update_layout(
    font=dict(family="Arial"),
    showlegend=False,
    plot_bgcolor='white',
    paper_bgcolor='white',
    margin=dict(l=90, r=40, t=40, b=120),
    xaxis=dict(
        title_text=texts.get('x_axis_title'),
        tickangle=0,
        showgrid=False,
        showline=False,
        zeroline=False,
        tickfont=dict(size=12)
    ),
    yaxis=dict(
        title_text=texts.get('y_axis_title'),
        title_standoff=15,
        showgrid=True,
        gridcolor='lightgrey',
        griddash='dot',
        gridwidth=1,
        showline=False,
        zeroline=False,
        range=[0, 250],
        tickvals=[0, 50, 100, 150, 200, 250],
        tickfont=dict(size=12)
    )
)

if texts.get('source'):
    fig.add_annotation(
        text=texts['source'],
        align='right',
        showarrow=False,
        xref='paper',
        yref='paper',
        x=1.0,
        y=-0.22,
        xanchor='right',
        yanchor='top',
        font=dict(size=12, color='#808080')
    )

base_name_with_ext = json_path.split('/')[-1]
base_name = base_name_with_ext.rsplit('.', 1)[0]
output_filename = f"{base_name}.png"

fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")