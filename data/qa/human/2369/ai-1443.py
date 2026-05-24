import sys
import json
import os
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <json_file_path>")
    sys.exit(1)

json_path = sys.argv[1]

if not os.path.exists(json_path):
    print(f"Error: File not found at {json_path}")
    sys.exit(1)

with open(json_path, 'r', encoding='utf-8') as f:
    chart_info = json.load(f)

chart_data = chart_info["chart_data"]
texts = chart_info["texts"]
colors = chart_info["colors"]

fig = go.Figure()

for i, series in enumerate(chart_data):
    fig.add_trace(go.Bar(
        name=series['name'],
        x=series['x'],
        y=series['y'],
        marker_color=colors[i],
        texttemplate='%{y}%',
        textposition='outside',
        cliponaxis=False
    ))

title_text = texts.get("title", "")
if texts.get("subtitle"):
    title_text += f"<br><sub>{texts['subtitle']}</sub>"

fig.update_layout(
    barmode='group',
    font_family="Arial",
    title_text=title_text if title_text else None,
    yaxis_title=texts.get('y_axis_title'),
    xaxis_title=texts.get('x_axis_title'),
    legend=dict(
        orientation="h",
        yanchor="top",
        y=-0.2,
        xanchor="center",
        x=0.5
    ),
    template="plotly_white",
    margin=dict(t=60, b=120, l=80, r=40),
    yaxis=dict(
        range=[0, 41],
        ticksuffix='%',
        showgrid=True,
        gridcolor='lightgrey'
    ),
    xaxis=dict(
        showgrid=False
    )
)

fig.update_traces(
    textfont=dict(
        family="Arial",
        size=12,
        color='black'
    )
)

if texts.get("source"):
    fig.add_annotation(
        text=texts['source'],
        align='right',
        showarrow=False,
        xref='paper',
        yref='paper',
        x=1.0,
        y=-0.3,
        xanchor='right',
        yanchor='bottom',
        font=dict(size=10)
    )

base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_filename}.png"

fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")