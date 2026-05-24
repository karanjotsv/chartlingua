import sys
import json
import os
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print("Usage: python script.py <json_file_path>")
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

fig = go.Figure()

fig.add_trace(go.Bar(
    x=categories,
    y=values,
    text=[f'{v:,}'.replace(',', ' ') for v in values],
    textposition='outside',
    cliponaxis=False,
    marker_color=colors[0] if colors else None,
    hoverinfo='none'
))

fig.update_traces(textfont_size=12)

y_axis_tick_vals = list(range(0, 6000001, 1000000))
y_axis_tick_text = [f'{v:,}'.replace(',', ' ') for v in y_axis_tick_vals]

fig.update_layout(
    font_family="Arial",
    plot_bgcolor='white',
    showlegend=False,
    margin=dict(l=90, r=40, t=60, b=80),
    xaxis=dict(
        title_text=texts.get('x_axis_title'),
        showgrid=False,
        linecolor='black',
        linewidth=1,
        tickfont=dict(size=12)
    ),
    yaxis=dict(
        title_text=texts.get('y_axis_title'),
        title_standoff=25,
        showgrid=True,
        gridcolor='#EAEAEA',
        gridwidth=1,
        griddash='dot',
        zeroline=False,
        range=[0, 6000000],
        tickvals=y_axis_tick_vals,
        ticktext=y_axis_tick_text,
        tickfont=dict(size=12)
    ),
    annotations=[
        dict(
            text=texts.get('source'),
            showarrow=False,
            xref='paper',
            yref='paper',
            x=1.0,
            y=-0.18,
            xanchor='right',
            yanchor='top',
            font=dict(size=11, color='#666666')
        )
    ]
)

base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_filename}.png"

fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")