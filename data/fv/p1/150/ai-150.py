import sys
import json
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print("Usage: python <script_name>.py <json_file_path>")
    sys.exit(1)

json_file_path = sys.argv[1]

# Derive the base filename from the input JSON path
base_filename = json_file_path.split('/')[-1].split('\\')[-1].rsplit('.', 1)[0]
output_image_path = f"{base_filename}.png"

try:
    with open(json_file_path, 'r', encoding='utf-8') as f:
        config = json.load(f)
except FileNotFoundError:
    print(f"Error: The file '{json_file_path}' was not found.")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: The file '{json_file_path}' is not a valid JSON file.")
    sys.exit(1)

chart_data = config.get('chart_data', [])
texts = config.get('texts', {})
colors = config.get('colors', [])

fig = go.Figure()

for i, series in enumerate(chart_data):
    color = colors[i % len(colors)] if colors else None
    fig.add_trace(go.Scatter(
        x=series.get('x'),
        y=series.get('y'),
        name=series.get('name'),
        mode='lines',
        line=dict(
            color=color,
            width=3,
            shape=series.get('line_shape', 'linear')
        )
    ))

title_text = texts.get('title', '')
subtitle_text = texts.get('subtitle')
if subtitle_text:
    title_text = f"{title_text}<br><sub>{subtitle_text}</sub>"

fig.update_layout(
    title=dict(
        text=title_text,
        x=0.5,
        xanchor='center',
        yanchor='top',
        pad=dict(t=20)
    ),
    xaxis=dict(
        title=texts.get('x_axis_title'),
        range=[0, 300],
        showgrid=True,
        gridcolor='#CCCCCC',
        zeroline=False,
        linecolor='black',
        linewidth=1
    ),
    yaxis=dict(
        title=texts.get('y_axis_title'),
        range=[0, 125],
        dtick=20,
        showgrid=True,
        gridcolor='#CCCCCC',
        zeroline=False,
        linecolor='black',
        linewidth=1
    ),
    font=dict(
        family="Arial",
        size=12
    ),
    legend=dict(
        x=1.02,
        y=0.5,
        xanchor='left',
        yanchor='middle',
        bgcolor='rgba(0,0,0,0)',
        bordercolor='black',
        borderwidth=0
    ),
    plot_bgcolor='white',
    paper_bgcolor='white',
    margin=dict(l=80, r=200, t=100, b=80),
    autosize=False,
    width=800,
    height=500
)

fig.write_image(output_image_path, scale=2)

print(f"Chart saved to {output_image_path}")