import sys
import json
import os
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print("Usage: python recreate_chart.py <path_to_json_file>")
    sys.exit(1)

json_filepath = sys.argv[1]

try:
    with open(json_filepath, 'r', encoding='utf-8') as f:
        chart_info = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_filepath}")
    sys.exit(1)

chart_data = chart_info['chart_data']
texts = chart_info['texts']
colors = chart_info['colors']

categories = [item['category'] for item in chart_data]
values = [item['value'] for item in chart_data]

fig = go.Figure()

fig.add_trace(go.Bar(
    x=categories,
    y=values,
    marker_color=colors[0],
    text=values,
    textposition='outside',
    textfont=dict(family="Arial", size=12, color='black'),
    cliponaxis=False
))

annotations = []
if texts.get("note"):
    annotations.append(
        dict(
            xref="paper", yref="paper",
            x=0, y=-0.15,
            xanchor="left", yanchor="top",
            text=texts["note"],
            showarrow=False,
            align="left",
            font=dict(family="Arial", size=12, color="#0073e5")
        )
    )

if texts.get("source"):
    annotations.append(
        dict(
            xref="paper", yref="paper",
            x=1, y=-0.15,
            xanchor="right", yanchor="top",
            text=texts["source"],
            showarrow=False,
            align="right",
            font=dict(family="Arial", size=11, color="grey")
        )
    )

fig.update_layout(
    font=dict(family="Arial"),
    plot_bgcolor='white',
    paper_bgcolor='white',
    showlegend=False,
    yaxis=dict(
        title=texts.get('y_axis_title'),
        range=[0, 125],
        tickmode='linear',
        tick0=0,
        dtick=20,
        gridcolor='#e0e0e0',
        zeroline=False
    ),
    xaxis=dict(
        title=texts.get('x_axis_title'),
        showgrid=True,
        gridwidth=1,
        gridcolor='#f0f0f0'
    ),
    margin=dict(l=80, r=40, t=40, b=120),
    annotations=annotations
)

output_filename_base = os.path.splitext(json_filepath)[0]
output_filename_png = f"{output_filename_base}.png"
fig.write_image(output_filename_png, scale=2)

print(f"Chart saved to {output_filename_png}")