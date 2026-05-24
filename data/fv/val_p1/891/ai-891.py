import sys
import json
import pathlib
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print("Usage: python <script_name>.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]

try:
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_path}")
    sys.exit(1)

chart_data = data.get('chart_data', [])
texts = data.get('texts', {})
colors = data.get('colors', {})
y_axis_config = data.get('y_axis_config', {})

x_values = [d['month'] for d in chart_data]
y_values = [d['value'] for d in chart_data]

fig = go.Figure()

fig.add_trace(go.Scatter(
    x=x_values,
    y=y_values,
    mode='lines+markers',
    line=dict(color=colors.get('series', ['#000000'])[0], width=2),
    marker=dict(
        color=colors.get('marker_fill', '#FFFFFF'),
        size=8,
        line=dict(color=colors.get('series', ['#000000'])[0], width=2)
    ),
    showlegend=False
))

title_text = texts.get('title', '')
if texts.get('subtitle'):
    title_text += f"<br><sub>{texts['subtitle']}</sub>"

source_text = texts.get('source', '')

fig.update_layout(
    title=dict(
        text=title_text,
        x=0.5,
        y=0.95,
        xanchor='center',
        yanchor='top',
        font=dict(size=16)
    ),
    xaxis=dict(
        title=texts.get('x_axis_title'),
        showline=True,
        linewidth=1,
        linecolor='black',
        showgrid=False,
        tickfont=dict(size=11)
    ),
    yaxis=dict(
        title=texts.get('y_axis_title'),
        range=y_axis_config.get('range'),
        tickvals=y_axis_config.get('tickvals'),
        showline=True,
        linewidth=1,
        linecolor='black',
        gridcolor=colors.get('grid', '#e0e0e0'),
        tickformat=',',
        tickfont=dict(size=11)
    ),
    font=dict(
        family="Arial",
        color="black"
    ),
    plot_bgcolor='white',
    paper_bgcolor='white',
    margin=dict(l=90, r=40, b=200, t=100),
    annotations=[
        dict(
            text=source_text,
            showarrow=False,
            xref="paper",
            yref="paper",
            x=0,
            y=-0.35,
            xanchor='left',
            yanchor='top',
            align='left',
            font=dict(size=10)
        )
    ]
)

base_name = pathlib.Path(json_path).stem
output_filename = f"{base_name}.png"
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")