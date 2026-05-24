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
        chart_info = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_path}")
    sys.exit(1)

data = chart_info['chart_data']
texts = chart_info['texts']
colors = chart_info['colors']
categories = data['categories']

fig = go.Figure()

for i, series in enumerate(data['series']):
    fig.add_trace(go.Bar(
        y=categories,
        x=series['values'],
        name=series['name'],
        orientation='h',
        marker=dict(color=colors[i]),
        text=series['values'],
        textposition='inside',
        insidetextanchor='middle',
        insidetextfont=dict(
            family="Arial",
            size=12,
            color="white"
        ),
        textfont=dict(
            family="Arial",
            size=12,
            color="white"
        )
    ))

title_text = ""
if texts.get("title"):
    title_text += texts["title"]
if texts.get("subtitle"):
    title_text += f"<br><sup>{texts['subtitle']}</sup>"

fig.update_layout(
    barmode='stack',
    title=dict(
        text=title_text,
        x=0.05,
        xanchor='left'
    ),
    xaxis=dict(
        title=texts.get('x_axis_label', ''),
        showgrid=True,
        gridcolor='#e0e0e0',
        gridwidth=1,
        griddash='dot',
        zeroline=False,
        ticks='outside',
        tickmode='linear',
        dtick=10,
        range=[0, 125]
    ),
    yaxis=dict(
        title=texts.get('y_axis_label', ''),
        autorange='reversed',
        showgrid=False,
        zeroline=False
    ),
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=-0.25,
        xanchor="center",
        x=0.5
    ),
    plot_bgcolor='white',
    paper_bgcolor='white',
    font=dict(
        family="Arial",
        size=12,
        color="black"
    ),
    margin=dict(l=120, r=40, t=50, b=100)
)

if texts.get("source"):
    fig.add_annotation(
        text=texts["source"],
        xref="paper",
        yref="paper",
        x=1,
        y=-0.3,
        showarrow=False,
        xanchor='right',
        yanchor='bottom',
        align='right',
        font=dict(
            family="Arial",
            size=10,
            color="grey"
        )
    )

base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_filename}.png"

fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")