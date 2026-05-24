import sys
import os
import json
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print("Usage: python create_chart.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]

if not os.path.exists(json_path):
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)

with open(json_path, 'r', encoding='utf-8') as f:
    chart_info = json.load(f)

chart_data = chart_info.get('chart_data', [])
texts = chart_info.get('texts', {})
colors = chart_info.get('colors', [])

fig = go.Figure()

for i, series in enumerate(chart_data):
    fig.add_trace(go.Scatter(
        x=series.get('x'),
        y=series.get('y'),
        name=series.get('name'),
        mode='lines',
        line=dict(color=colors[i % len(colors)], width=2.5)
    ))

title_text = f"<b>{texts.get('title', '')}</b>"
if texts.get('subtitle'):
    title_text += f"<br><sub>{texts.get('subtitle')}</sub>"

source_text = texts.get('source')
if source_text:
    fig.add_annotation(
        text=source_text,
        align='left',
        showarrow=False,
        xref='paper',
        yref='paper',
        x=0,
        y=-0.15,
        xanchor='left',
        yanchor='top'
    )

fig.update_layout(
    title_text=title_text,
    title_x=0.5,
    title_y=0.95,
    xaxis_title=texts.get('x_axis_title'),
    yaxis_title=texts.get('y_axis_title'),
    plot_bgcolor='black',
    paper_bgcolor='black',
    font=dict(
        family="Arial",
        size=14,
        color="white"
    ),
    legend=dict(
        x=0.98,
        y=0.98,
        xanchor='right',
        yanchor='top',
        font=dict(color='white'),
        bgcolor='rgba(0,0,0,0.5)',
        bordercolor='white',
        borderwidth=1
    ),
    xaxis=dict(
        gridcolor='rgba(255, 255, 255, 0.2)',
        zeroline=False,
        linecolor='white',
        ticks='outside',
        tickcolor='white'
    ),
    yaxis=dict(
        gridcolor='rgba(255, 255, 255, 0.2)',
        zeroline=False,
        linecolor='white',
        ticks='outside',
        tickcolor='white'
    ),
    margin=dict(t=100, b=100, l=80, r=40)
)

base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_filename}.png"

try:
    fig.write_image(output_filename, scale=2)
    print(f"Chart successfully saved to {output_filename}")
except Exception as e:
    print(f"Error saving image: {e}")
    print("Please ensure you have 'kaleido' installed (`pip install kaleido`)")
    sys.exit(1)