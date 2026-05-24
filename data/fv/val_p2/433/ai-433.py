import sys
import json
import os
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print(f"Usage: python {os.path.basename(sys.argv[0])} <json_file_path>")
    sys.exit(1)

json_path = sys.argv[1]

if not os.path.exists(json_path):
    print(f"Error: File not found at {json_path}")
    sys.exit(1)

with open(json_path, 'r', encoding='utf-8') as f:
    config = json.load(f)

chart_data = config['chart_data']
texts = config['texts']
colors = config['colors']

fig = go.Figure()

for i, series in enumerate(chart_data):
    fig.add_trace(go.Bar(
        x=series['x'],
        y=series['y'],
        name=series['name'],
        marker=dict(
            color=colors[i % len(colors)],
            line=dict(
                color='#303050',
                width=1.5
            )
        ),
        text=texts.get('data_labels'),
        textposition='outside',
        textfont=dict(family="Arial", size=12, color='black'),
        cliponaxis=False
    ))

title_text = ""
if texts.get("title"):
    title_text += texts["title"]
if texts.get("subtitle"):
    title_text += f"<br><sub>{texts['subtitle']}</sub>"

fig.update_layout(
    font=dict(family="Arial", size=12, color="black"),
    title_text=title_text if title_text else None,
    title_x=0.5,
    xaxis=dict(
        title_text=texts.get("x_axis_title"),
        showgrid=False,
        showline=True,
        linewidth=1,
        linecolor='black'
    ),
    yaxis=dict(
        title_text=texts.get("y_axis_title"),
        range=[0, 50000],
        dtick=5000,
        tickprefix="$",
        tickformat=',.0f',
        gridcolor='white',
        showline=True,
        linewidth=1,
        linecolor='black'
    ),
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=-0.3,
        xanchor="center",
        x=0.5
    ),
    plot_bgcolor='#D3D3D3',
    paper_bgcolor='white',
    margin=dict(l=80, r=40, t=50, b=100),
    bargap=0.25
)

if texts.get("source"):
    fig.add_annotation(
        showarrow=False,
        text=texts.get("source"),
        xref="paper",
        yref="paper",
        x=0,
        y=-0.38,
        xanchor="left",
        yanchor="bottom",
        align="left"
    )

base_name = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_name}.png"

fig.write_image(output_filename, scale=2)
print(f"Chart saved to {output_filename}")