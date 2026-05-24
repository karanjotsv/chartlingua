import sys
import json
import os
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print("Usage: python create_chart.py <json_file_path>")
    sys.exit(1)

json_path = sys.argv[1]

try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_config = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at '{json_path}'")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from '{json_path}'")
    sys.exit(1)

chart_data = chart_config.get('chart_data', [])
texts = chart_config.get('texts', {})
colors = chart_config.get('colors', [])

if not chart_data:
    print("Error: 'chart_data' is missing or empty in the JSON file.")
    sys.exit(1)

fig = go.Figure()

x_values = [item['x'] for item in chart_data]
y_values = [item['y'] for item in chart_data]

bar_color = colors[0] if colors else '#337ab7'

fig.add_trace(go.Bar(
    x=x_values,
    y=y_values,
    marker_color=bar_color,
    text=[f'{val:,}'.replace(',', ' ') for val in y_values],
    textposition='outside',
    cliponaxis=False
))

title_parts = []
if texts.get('title'):
    title_parts.append(texts['title'])
if texts.get('subtitle'):
    title_parts.append(f"<span style='font-size:0.8em;color:gray;'>{texts['subtitle']}</span>")
full_title = "<br>".join(title_parts)

source_parts = []
if texts.get('source'):
    source_parts.append(texts['source'])
if texts.get('note'):
    source_parts.append(texts['note'])
full_source = "<br>".join(source_parts)

fig.update_layout(
    title_text=full_title,
    title_x=0.05,
    title_font_family="Arial",
    font_family="Arial",
    plot_bgcolor='white',
    paper_bgcolor='white',
    showlegend=False,
    xaxis=dict(
        title_text=texts.get('x_axis_title'),
        showline=True,
        linewidth=1,
        linecolor='black',
        tickmode='array',
        tickvals=x_values,
        ticktext=[str(x) for x in x_values]
    ),
    yaxis=dict(
        title_text=texts.get('y_axis_title'),
        range=[0, 50000],
        showgrid=True,
        gridcolor='#e0e0e0',
        tickformat=' ',
        zeroline=False
    ),
    margin=dict(l=80, r=40, t=50, b=80),
    annotations=[
        dict(
            text=full_source,
            showarrow=False,
            xref="paper",
            yref="paper",
            x=1.0,
            y=-0.15,
            xanchor='right',
            yanchor='top',
            align='right',
            font=dict(size=10, color="#666666")
        )
    ]
)

base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_filename}.png"

fig.write_image(output_filename, scale=2)

print(f"Chart saved as '{output_filename}'")