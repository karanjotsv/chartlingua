import sys
import json
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print("Usage: python script.py <path_to_json_file>")
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

chart_data = chart_info.get('chart_data', [])
texts = chart_info.get('texts', {})
colors = chart_info.get('colors', [])

categories = [item['category'] for item in chart_data]
values = [item['value'] for item in chart_data]

fig = go.Figure()

fig.add_trace(go.Bar(
    x=categories,
    y=values,
    marker_color=colors[0] if colors else '#A42222',
    showlegend=False
))

title_text = f"<b>{texts.get('title', '')}</b>"
if texts.get('subtitle'):
    title_text += f"<br><sub>{texts.get('subtitle')}</sub>"

fig.update_layout(
    title=dict(
        text=title_text,
        x=0.5,
        font=dict(
            family="Arial",
            size=28,
            color='black'
        )
    ),
    xaxis=dict(
        title_text=texts.get('x_axis_title'),
        tickfont=dict(family="Arial"),
        title_font=dict(family="Arial"),
        showline=True,
        linecolor='black'
    ),
    yaxis=dict(
        title_text=texts.get('y_axis_title'),
        range=[0, 12500000],
        tickvals=[0, 2500000, 5000000, 7500000, 10000000, 12500000],
        tickformat=',',
        gridcolor='lightgrey',
        tickfont=dict(family="Arial"),
        title_font=dict(family="Arial")
    ),
    plot_bgcolor='white',
    showlegend=False,
    font=dict(family="Arial"),
    margin=dict(l=90, r=40, t=100, b=80)
)

output_filename_base = json_path.rsplit('.', 1)[0]
output_filename_png = f"{output_filename_base}.png"

fig.write_image(output_filename_png, scale=2)
print(f"Chart saved to {output_filename_png}")