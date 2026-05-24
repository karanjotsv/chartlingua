import sys
import json
import pathlib
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

chart_data = chart_details['chart_data']
texts = chart_details['texts']
colors = chart_details['colors']

categories = [d['category'] for d in chart_data]
values = [d['value'] for d in chart_data]
labels = [d['label'] for d in chart_data]

fig = go.Figure()

fig.add_trace(go.Bar(
    y=categories,
    x=values,
    orientation='h',
    marker=dict(color=colors[0]),
    text=labels,
    textposition='outside',
    texttemplate='%{text}',
    cliponaxis=False
))

fig.update_layout(
    font=dict(family="Arial", size=12, color="#000000"),
    plot_bgcolor='white',
    paper_bgcolor='white',
    showlegend=False,
    xaxis_title=texts.get('x_axis_title'),
    yaxis_title=texts.get('y_axis_title'),
    xaxis=dict(
        showgrid=True,
        gridcolor='#E0E0E0',
        griddash='dash',
        zeroline=False,
        range=[0, max(values) * 1.18]
    ),
    yaxis=dict(
        autorange="reversed",
        showgrid=False
    ),
    margin=dict(l=160, r=80, t=40, b=80),
    annotations=[
        dict(
            text=texts.get('source', ''),
            showarrow=False,
            xref="paper",
            yref="paper",
            x=0.98,
            y=-0.15,
            xanchor='right',
            yanchor='top',
            align='right',
            font=dict(size=12)
        )
    ]
)

base_filename = pathlib.Path(json_path).stem
output_filename = f"{base_filename}.png"
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")