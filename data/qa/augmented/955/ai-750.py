import sys
import json
import os
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <json_file_path>")
    sys.exit(1)

json_path = sys.argv[1]

try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_config = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_path}")
    sys.exit(1)

chart_data = chart_config.get('chart_data', [])
texts = chart_config.get('texts', {})
colors = chart_config.get('colors', [])

categories = [d['category'] for d in chart_data]
values = [d['value'] for d in chart_data]

text_labels = [f"{v:.2f}%".replace('.00%', '%') for v in values]

fig = go.Figure()

fig.add_trace(go.Bar(
    x=categories,
    y=values,
    text=text_labels,
    textposition='outside',
    marker_color=colors[0] if colors else '#2875D3',
    textfont=dict(family="Arial", size=12, color='black'),
    cliponaxis=False
))

fig.update_layout(
    font=dict(family="Arial", size=12, color="black"),
    title=dict(
        text=texts.get('title'),
        x=0.05,
        xanchor='left'
    ),
    paper_bgcolor='#F5F5F5',
    plot_bgcolor='white',
    showlegend=False,
    xaxis=dict(
        title_text=texts.get('x_axis_title'),
        showgrid=False,
        showline=False,
        tickfont=dict(size=12)
    ),
    yaxis=dict(
        title_text=texts.get('y_axis_title'),
        range=[0, 7],
        tickvals=[i for i in range(8)],
        ticksuffix='%',
        gridcolor='#E0E0E0',
        gridwidth=1,
        zeroline=False,
        tickfont=dict(size=12)
    ),
    margin=dict(l=80, r=40, t=50, b=100),
    annotations=[
        dict(
            text=texts.get('source', ''),
            showarrow=False,
            xref='paper',
            yref='paper',
            x=0.99,
            y=-0.15,
            xanchor='right',
            yanchor='top',
            align='right',
            font=dict(family="Arial", size=12, color="grey")
        )
    ]
)

base_name = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_name}.png"

fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")