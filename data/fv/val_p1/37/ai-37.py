import sys
import json
import os
import plotly.graph_objects as go

if len(sys.argv) != 2:
    sys.exit("Usage: python <script_name>.py <json_file_path>")

json_path = sys.argv[1]

try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_info = json.load(f)
except (FileNotFoundError, json.JSONDecodeError) as e:
    sys.exit(f"Error reading or parsing JSON file: {e}")

chart_data = chart_info.get('chart_data', [])
texts = chart_info.get('texts', {})
colors = chart_info.get('colors', [])

categories = [d['category'] for d in chart_data]
values = [d['value'] for d in chart_data]
currency_symbol = texts.get('currency_symbol', '')

bar_labels = [f"{currency_symbol}{v:.2f}" for v in values]

fig = go.Figure()

fig.add_trace(go.Bar(
    x=categories,
    y=values,
    text=bar_labels,
    textposition='outside',
    marker_color=colors[0] if colors else '#4F81BD',
    cliponaxis=False,
    showlegend=False
))

fig.update_layout(
    title=dict(
        text=texts.get('title'),
        x=0.5,
        font=dict(family="Arial", size=18, color='black')
    ),
    xaxis=dict(
        title_text=texts.get('x_axis_title'),
        showgrid=False,
        showline=True,
        linecolor='black',
        tickfont=dict(family="Arial", size=12)
    ),
    yaxis=dict(
        title_text=texts.get('y_axis_title'),
        range=[0, 8.5],
        tickvals=[i for i in range(9)],
        tickprefix=currency_symbol,
        tickformat=".2f",
        gridcolor='lightgrey',
        showline=True,
        linecolor='black',
        tickfont=dict(family="Arial", size=12),
        zeroline=False
    ),
    plot_bgcolor='white',
    paper_bgcolor='white',
    font_family="Arial",
    margin=dict(l=60, r=20, t=80, b=50)
)

fig.update_traces(
    textfont=dict(family="Arial", size=12, color='black')
)

output_filename_base = os.path.splitext(os.path.basename(json_path))[0]
fig.write_image(f"{output_filename_base}.png", scale=2)