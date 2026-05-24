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
        chart_data_json = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_file_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_file_path}")
    sys.exit(1)

chart_data = chart_data_json.get('chart_data', [])
texts = chart_data_json.get('texts', {})
colors = chart_data_json.get('colors', [])

categories = [item['category'] for item in chart_data]
values = [item['value'] for item in chart_data]
formatted_text = [f"{v:,}".replace(",", " ") for v in values]

fig = go.Figure()

fig.add_trace(go.Bar(
    x=categories,
    y=values,
    text=formatted_text,
    textposition='outside',
    marker_color=colors[0] if colors else '#2772d6',
    cliponaxis=False,
    textfont=dict(
        family="Arial",
        size=14,
        color='black'
    )
))

y_axis_max = 620000
fig.update_layout(
    font_family="Arial",
    plot_bgcolor='white',
    xaxis=dict(
        showgrid=False,
        showline=True,
        linecolor='black',
        linewidth=1,
        tickfont=dict(size=12),
        zeroline=False
    ),
    yaxis=dict(
        title=texts.get('y_axis_title'),
        showgrid=True,
        gridcolor='#e0e0e0',
        gridwidth=1,
        zeroline=False,
        range=[0, y_axis_max],
        tickvals=[0, 100000, 200000, 300000, 400000, 500000, 600000],
        ticktext=["0", "100 000", "200 000", "300 000", "400 000", "500 000", "600 000"],
        tickfont=dict(size=12)
    ),
    margin=dict(l=80, r=40, t=40, b=100),
    showlegend=False
)

if texts.get('source'):
    fig.add_annotation(
        text=texts['source'],
        align='right',
        showarrow=False,
        xref='paper',
        yref='paper',
        x=1,
        y=-0.15,
        xanchor='right',
        yanchor='top',
        font=dict(family='Arial', size=12)
    )

base_filename = os.path.splitext(json_file_path)[0]
output_filename = f"{base_filename}.png"

fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")