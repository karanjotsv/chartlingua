import sys
import json
import os
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print("Usage: python script.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]

try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_details = json.load(f)
except FileNotFoundError:
    print(f"Error: The file {json_path} was not found.")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: The file {json_path} is not a valid JSON file.")
    sys.exit(1)

chart_data = chart_details.get('chart_data', {})
texts = chart_details.get('texts', {})
colors = chart_details.get('colors', [])

fig = go.Figure()

for i, series in enumerate(chart_data.get('series', [])):
    fig.add_trace(go.Bar(
        x=chart_data.get('categories', []),
        y=series.get('data', []),
        name=series.get('name', ''),
        marker_color=colors[i % len(colors)],
        text=[f"{val}%" for val in series.get('data', [])],
        textposition='inside',
        insidetextanchor='end',
        textfont=dict(
            family="Arial",
            size=12,
            color='black'
        )
    ))

title_text = texts.get('title') or ''
if texts.get('subtitle'):
    title_text += f"<br><sub>{texts.get('subtitle')}</sub>"

fig.update_layout(
    barmode='group',
    plot_bgcolor='white',
    font=dict(family="Arial", size=12),
    title=dict(
        text=title_text,
        x=0.05,
        xanchor='left'
    ),
    xaxis=dict(
        title_text=texts.get('x_axis_title'),
        showgrid=False,
        showline=True,
        linewidth=1,
        linecolor='black',
        tickfont=dict(size=12)
    ),
    yaxis=dict(
        title_text=texts.get('y_axis_title'),
        range=[0, 35],
        dtick=5,
        ticksuffix='%',
        showgrid=True,
        gridcolor='#E0E0E0',
        gridwidth=1,
        griddash='dash',
        showline=False,
        zeroline=False
    ),
    legend=dict(
        orientation='h',
        yanchor='bottom',
        y=-0.25,
        xanchor='center',
        x=0.5
    ),
    margin=dict(l=60, r=40, b=100, t=40),
    bargroupgap=0.2
)

annotations = []
if texts.get('source'):
    annotations.append(
        dict(
            xref='paper', yref='paper',
            x=1, y=-0.3,
            xanchor='right', yanchor='bottom',
            text=texts.get('source'),
            showarrow=False,
            font=dict(size=10)
        )
    )

fig.update_layout(annotations=annotations)

output_filename_base = os.path.splitext(json_path)[0]
fig.write_image(f"{output_filename_base}.png", scale=2)

print(f"Chart saved to {output_filename_base}.png")