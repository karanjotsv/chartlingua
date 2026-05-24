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
        chart_info = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_file_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_file_path}")
    sys.exit(1)

chart_data = chart_info['chart_data']
texts = chart_info['texts']
colors = chart_info['colors']['primary']

fig = go.Figure()

fig.add_trace(go.Bar(
    x=chart_data['categories'],
    y=chart_data['series'][0]['values'],
    marker_color=colors[0],
    text=chart_data['series'][0]['values'],
    textposition='outside',
    textfont=dict(color='black', size=12, family='Arial'),
    cliponaxis=False
))

# Add white vertical lines to mimic Statista's column separators
for i in range(len(chart_data['categories']) - 1):
    fig.add_vline(x=i + 0.5, line_width=2, line_color='white')

fig.update_layout(
    font=dict(family="Arial", size=12, color="black"),
    title_text=texts.get('title'),
    title_x=0.5,
    yaxis_title=texts.get('y_axis_title'),
    plot_bgcolor='#f0f0f0',
    paper_bgcolor='white',
    showlegend=False,
    margin=dict(l=80, r=40, t=40, b=80),
    xaxis=dict(
        showgrid=False,
        showline=True,
        linecolor='black',
        linewidth=1,
        tickfont=dict(size=12)
    ),
    yaxis=dict(
        range=[0, 300],
        tickvals=[0, 50, 100, 150, 200, 250, 300],
        showgrid=True,
        gridcolor='lightgrey',
        griddash='dot',
        zeroline=False,
        showline=False,
        tickfont=dict(size=12)
    )
)

if texts.get('source'):
    fig.add_annotation(
        text=texts['source'],
        xref="paper", yref="paper",
        x=0.98, y=-0.15,
        showarrow=False,
        xanchor='right',
        yanchor='top',
        font=dict(size=12, color="grey")
    )

base_filename = os.path.splitext(os.path.basename(json_file_path))[0]
output_filename = f"{base_filename}.png"

fig.write_image(output_filename, scale=2)