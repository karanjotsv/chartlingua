import sys
import json
import os
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print(f"Usage: python {os.path.basename(__file__)} <json_file_path>")
    sys.exit(1)

json_path = sys.argv[1]

try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_info = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_path}")
    sys.exit(1)

chart_data = chart_info.get('chart_data', [])
texts = chart_info.get('texts', {})
colors = chart_info.get('colors', [])

y_values = [d['category'] for d in chart_data]
x_values = [d['value'] for d in chart_data]

fig = go.Figure()

fig.add_trace(go.Bar(
    y=y_values,
    x=x_values,
    orientation='h',
    marker=dict(color=colors[0]),
    text=x_values,
    textposition='outside',
    texttemplate='%{text}',
    cliponaxis=False 
))

title_text = texts.get('title') or ''
if texts.get('subtitle'):
    title_text += f"<br><sub>{texts['subtitle']}</sub>"

source_text = texts.get('source') or ''
if texts.get('note'):
    source_text += f"<br>{texts['note']}"

fig.update_layout(
    title_text=title_text,
    title_x=0.05,
    xaxis_title=texts.get('x_axis_title'),
    yaxis_title=texts.get('y_axis_title'),
    font=dict(family="Arial", size=12, color="black"),
    showlegend=False,
    plot_bgcolor='white',
    paper_bgcolor='white',
    margin=dict(l=100, r=60, t=50, b=80),
    xaxis=dict(
        showgrid=True,
        gridcolor='#dddddd',
        gridwidth=1,
        zeroline=False,
        showline=False,
        griddash='dot'
    ),
    yaxis=dict(
        showgrid=False,
        showline=True,
        linecolor='black',
        linewidth=1
    ),
    annotations=[
        dict(
            text=source_text,
            showarrow=False,
            xref="paper",
            yref="paper",
            x=1,
            y=-0.18,
            xanchor='right',
            yanchor='top',
            align='right',
            font=dict(family="Arial", size=10)
        )
    ]
)

base_name = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_name}.png"

fig.write_image(output_filename, scale=2)
print(f"Chart saved to {output_filename}")