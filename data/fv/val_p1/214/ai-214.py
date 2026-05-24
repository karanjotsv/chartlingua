import sys
import json
import os
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print("Usage: python <script_name>.py <json_file_path>")
    sys.exit(1)

json_path = sys.argv[1]

try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_details = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_path}")
    sys.exit(1)

fig = go.Figure()

chart_data = chart_details.get('chart_data', [])
colors = chart_details.get('colors', [])
texts = chart_details.get('texts', {})
annotations_data = chart_details.get('annotations', [])

for i, series in enumerate(chart_data):
    fig.add_trace(go.Scatter(
        x=series.get('x'),
        y=series.get('y'),
        mode='lines',
        name=series.get('name', ''),
        line=dict(color=colors[i] if i < len(colors) else None, width=2)
    ))

title_text = f"<span style='font-size: 24px; font-weight: bold;'>{texts.get('title', '')}</span><br><span style='font-size: 16px;'>{texts.get('subtitle', '')}</span>"

layout_annotations = []
for ann in annotations_data:
    layout_annotations.append(
        go.layout.Annotation(
            x=ann['x'],
            y=ann['y'],
            text=ann['text'],
            showarrow=False,
            font=dict(family="Arial", size=12, color="#000000"),
            xanchor=ann.get('xanchor', 'center'),
            yanchor=ann.get('yanchor', 'bottom'),
            xshift=ann.get('xshift', 0),
            yshift=ann.get('yshift', 0)
        )
    )

fig.update_layout(
    title=dict(
        text=title_text,
        y=0.95,
        x=0.05,
        xanchor='left',
        yanchor='top'
    ),
    xaxis=dict(
        title_text=texts.get('x_axis_title'),
        showgrid=True,
        gridwidth=1,
        gridcolor='#E5E5E5',
        tickformat='%b %y',
        zeroline=False
    ),
    yaxis=dict(
        title_text=texts.get('y_axis_title'),
        showgrid=True,
        gridwidth=1,
        gridcolor='#E5E5E5',
        range=[0, 10000],
        dtick=2500,
        zeroline=True,
        zerolinecolor='#000000',
        zerolinewidth=1
    ),
    font=dict(
        family="Arial",
        size=12,
        color="black"
    ),
    plot_bgcolor='white',
    paper_bgcolor='white',
    showlegend=False,
    margin=dict(l=80, r=40, t=120, b=80),
    annotations=layout_annotations
)

base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_filename}.png"

fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")