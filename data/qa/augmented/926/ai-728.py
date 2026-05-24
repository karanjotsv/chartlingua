import sys
import json
import os
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print("Usage: python create_chart.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]

if not os.path.exists(json_path):
    print(f"Error: File not found at {json_path}")
    sys.exit(1)

with open(json_path, 'r', encoding='utf-8') as f:
    chart_info = json.load(f)

chart_data = chart_info.get("chart_data", [])
texts = chart_info.get("texts", {})
colors = chart_info.get("colors", [])

categories = [item['category'] for item in chart_data]
values = [item['value'] for item in chart_data]

fig = go.Figure()

fig.add_trace(go.Bar(
    x=categories,
    y=values,
    marker_color=colors[0] if colors else None,
    text=values,
    textposition='outside',
    cliponaxis=False,
    textfont=dict(
        family="Arial",
        size=12,
        color='black'
    )
))

annotations = []
source_left_text = texts.get('source_left')
if source_left_text:
    annotations.append(
        dict(
            xref='paper', yref='paper',
            x=0, y=-0.15,
            xanchor='left', yanchor='top',
            text=source_left_text,
            showarrow=False,
            font=dict(family="Arial", size=12, color="#0066cc")
        )
    )

source_right_text = texts.get('source_right')
if source_right_text:
    annotations.append(
        dict(
            xref='paper', yref='paper',
            x=1, y=-0.15,
            xanchor='right', yanchor='top',
            text=source_right_text,
            showarrow=False,
            font=dict(family="Arial", size=12, color='#666666')
        )
    )

fig.update_layout(
    font=dict(family="Arial", size=12),
    plot_bgcolor='white',
    paper_bgcolor='white',
    showlegend=False,
    xaxis=dict(
        title_text=texts.get('x_axis_title'),
        showgrid=False,
        zeroline=True,
        zerolinecolor='#cccccc',
        zerolinewidth=1,
        linecolor='black',
        tickfont=dict(size=12)
    ),
    yaxis=dict(
        title_text=texts.get('y_axis_title'),
        range=[0, 1200],
        tickvals=[0, 200, 400, 600, 800, 1000, 1200],
        showgrid=True,
        gridcolor='#E0E0E0',
        zeroline=False,
        linecolor='black',
        tickformat=" ",
        tickfont=dict(size=12)
    ),
    margin=dict(l=90, r=30, t=50, b=100),
    annotations=annotations
)

fig.update_traces(textfont_weight="bold")

base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_filename}.png"

fig.write_image(output_filename, scale=2)
print(f"Chart saved to {output_filename}")