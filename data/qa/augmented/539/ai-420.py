import sys
import json
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print("Usage: python create_chart.py <json_file_path>")
    sys.exit(1)

json_filepath = sys.argv[1]

try:
    with open(json_filepath, 'r', encoding='utf-8') as f:
        chart_info = json.load(f)
except Exception as e:
    print(f"Error reading or parsing JSON file: {e}")
    sys.exit(1)

chart_data = chart_info.get('chart_data', [])
texts = chart_info.get('texts', {})
colors = chart_info.get('colors', [])

x_values = [d['x'] for d in chart_data]
y_values = [d['y'] for d in chart_data]

fig = go.Figure()

fig.add_trace(go.Bar(
    x=x_values,
    y=y_values,
    marker_color=colors[0] if colors else '#1f77b4',
    text=y_values,
    textposition='outside',
    cliponaxis=False
))

title_text = texts.get('title')
subtitle_text = texts.get('subtitle')
full_title = ''
if title_text:
    full_title = f"<b>{title_text}</b>"
    if subtitle_text:
        full_title += f"<br><sub>{subtitle_text}</sub>"

fig.update_layout(
    title=dict(
        text=full_title,
        x=0.01,
        xanchor='left',
        y=0.95,
        yanchor='top'
    ),
    xaxis=dict(
        title_text=texts.get('x_axis_title'),
        showgrid=False,
        showline=True,
        linecolor='black',
        linewidth=1
    ),
    yaxis=dict(
        title_text=texts.get('y_axis_title'),
        range=[0, 5],
        showgrid=True,
        gridcolor='#e0e0e0',
        zeroline=False
    ),
    plot_bgcolor='white',
    paper_bgcolor='white',
    font=dict(family="Arial", size=12, color="black"),
    showlegend=False,
    margin=dict(l=90, r=40, t=50, b=100),
    annotations=[
        dict(
            text=texts.get('source', ''),
            showarrow=False,
            xref="paper", yref="paper",
            x=1.0, y=-0.2,
            xanchor='right', yanchor='top',
            align='right',
            font=dict(size=10)
        )
    ]
)

fig.update_traces(
    textfont=dict(family="Arial", size=11, color='black'),
    texttemplate='%{text}'
)

base_name = json_filepath.rsplit('.', 1)[0]
output_filename = f"{base_name}.png"

fig.write_image(output_filename, scale=2)