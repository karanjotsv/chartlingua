import sys
import json
import os
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print("Usage: python <script_name>.py <json_file_path>")
    sys.exit(1)

json_file_path = sys.argv[1]

try:
    with open(json_file_path, 'r', encoding='utf-8') as f:
        chart_spec = json.load(f)
except FileNotFoundError:
    print(f"Error: File not found at {json_file_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Invalid JSON in {json_file_path}")
    sys.exit(1)

chart_data = chart_spec['chart_data']
texts = chart_spec['texts']
colors = chart_spec['colors']

categories = [item['category'] for item in chart_data]
values = [item['value'] for item in chart_data]

fig = go.Figure()

fig.add_trace(go.Bar(
    x=categories,
    y=values,
    marker_color=colors,
    cliponaxis=False
))

annotations = []
for item in chart_data:
    if item.get('value') is not None and item['value'] > 0 and item.get('text'):
        annotations.append(
            go.layout.Annotation(
                x=item['category'],
                y=item['value'],
                text=item['text'],
                showarrow=False,
                font=dict(
                    family="Arial",
                    size=12,
                    color="black"
                ),
                bgcolor='rgba(220, 220, 220, 0.85)',
                borderpad=4,
                yshift=10
            )
        )

fig.update_layout(
    title=dict(
        text=texts.get('title', ''),
        x=0.05,
        y=0.95,
        xanchor='left',
        yanchor='top',
        font=dict(
            family="Arial",
            size=16,
            color='black'
        )
    ),
    xaxis=dict(
        title_text=texts.get('x_axis_title'),
        showgrid=False,
        zeroline=True,
        zerolinecolor='black',
        zerolinewidth=1,
        tickfont=dict(family="Arial", size=12)
    ),
    yaxis=dict(
        title_text=texts.get('y_axis_title'),
        range=[0, 5],
        tickvals=[0, 1, 2, 3, 4, 5],
        showgrid=True,
        gridcolor='lightgrey',
        zeroline=True,
        zerolinecolor='black',
        zerolinewidth=1,
        tickfont=dict(family="Arial", size=12)
    ),
    font=dict(
        family="Arial",
        size=12,
        color='black'
    ),
    showlegend=False,
    plot_bgcolor='white',
    paper_bgcolor='white',
    margin=dict(l=60, r=40, t=80, b=120),
    annotations=annotations
)

base_filename = os.path.splitext(os.path.basename(json_file_path))[0]
output_image_path = f"{base_filename}.png"

fig.write_image(output_image_path, scale=2)
print(f"Chart saved to {output_image_path}")