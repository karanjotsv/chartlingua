import sys
import json
import os
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print("Usage: python create_chart.py <path_to_json_file>")
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

categories = [item['category'] for item in chart_data]
values = [item['value'] for item in chart_data]
text_values = [str(v) for v in values]

fig = go.Figure()

fig.add_trace(go.Bar(
    x=categories,
    y=values,
    text=text_values,
    textposition='outside',
    marker_color=colors[0] if colors else '#1f77b4',
    cliponaxis=False,
    texttemplate='%{text}'
))

source_text_parts = [texts.get('source'), texts.get('note')]
source_text = "<br>".join(filter(None, source_text_parts))

fig.update_layout(
    font=dict(family="Arial", size=12),
    plot_bgcolor='white',
    showlegend=False,
    margin=dict(l=80, r=40, t=50, b=100),
    yaxis=dict(
        title_text=texts.get('y_axis_title'),
        range=[0, 1550],
        tickmode='linear',
        dtick=250,
        gridcolor='#e5e5e5',
        zeroline=False
    ),
    xaxis=dict(
        title_text=texts.get('x_axis_title'),
        showgrid=False,
        showline=True,
        linewidth=1,
        linecolor='black',
        tickfont=dict(size=12)
    ),
    annotations=[
        dict(
            showarrow=False,
            text=source_text,
            xref="paper",
            yref="paper",
            x=1.0,
            y=-0.2,
            xanchor='right',
            yanchor='top',
            align='right'
        )
    ]
)

fig.update_traces(textfont_size=12)

base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_filename}.png"

fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")