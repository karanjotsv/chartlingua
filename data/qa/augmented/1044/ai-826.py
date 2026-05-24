import sys
import json
import os
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print("Usage: python recreate_chart.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]

try:
    with open(json_path, 'r', encoding='utf-8') as f:
        config = json.load(f)
except FileNotFoundError:
    print(f"Error: The file '{json_path}' was not found.")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Failed to decode JSON from '{json_path}'.")
    sys.exit(1)

chart_data = config.get('chart_data', [])
texts = config.get('texts', {})
colors = config.get('colors', [])

categories = [item['category'] for item in chart_data]
# This implementation assumes a single series bar chart as depicted
values = [item['values'][0] for item in chart_data]

fig = go.Figure()

fig.add_trace(go.Bar(
    x=categories,
    y=values,
    marker_color=colors[0] if colors else '#297ACC',
    text=values,
    textposition='outside',
    texttemplate='%{text}',
    cliponaxis=False,  # Prevent text on top bars from being clipped
))

title_str = ""
if texts.get("title"):
    title_str += f'<b>{texts["title"]}</b>'
if texts.get("subtitle"):
    title_str += f'<br><sub>{texts["subtitle"]}</sub>'

annotations = []
if texts.get("note"):
    annotations.append(
        dict(
            text=texts["note"],
            showarrow=False,
            xref="paper", yref="paper",
            x=0, y=-0.15,
            xanchor='left', yanchor='top',
            align="left",
            font=dict(size=12, color="#007bff")
        )
    )
if texts.get("source"):
    annotations.append(
        dict(
            text=texts["source"],
            showarrow=False,
            xref="paper", yref="paper",
            x=1, y=-0.15,
            xanchor='right', yanchor='top',
            align="right",
            font=dict(size=12, color="#6c757d")
        )
    )

fig.update_layout(
    title_text=title_str if title_str else None,
    font_family="Arial",
    plot_bgcolor='white',
    paper_bgcolor='white',
    showlegend=False,
    margin=dict(l=80, r=40, t=50, b=120),
    xaxis=dict(
        title_text=texts.get("x_axis_title"),
        showgrid=False,
        showline=True,
        linecolor='lightgrey',
        tickfont=dict(size=12)
    ),
    yaxis=dict(
        title_text=texts.get("y_axis_title"),
        range=[0, 250],
        tickvals=[0, 50, 100, 150, 200, 250],
        showgrid=True,
        gridcolor='#EAEAEA',
        showline=False,
        zeroline=False,
        tickfont=dict(size=12)
    ),
    annotations=annotations,
)

fig.update_traces(
    textfont=dict(
        family="Arial",
        size=12,
        color='black'
    )
)

base_name = os.path.splitext(json_path)[0]
output_filename = f"{base_name}.png"

fig.write_image(output_filename, scale=2)
print(f"Chart saved to {output_filename}")