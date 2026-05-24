import sys
import json
import os
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print("Usage: python script.py <path_to_json_file>")
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

fig = go.Figure()

fig.add_trace(go.Bar(
    x=[d['x'] for d in chart_data],
    y=[d['y'] for d in chart_data],
    marker_color=colors[0],
    name=''
))

fig.update_layout(
    title_text=f"<b>{texts['title']}</b>",
    title_x=0.5,
    title_font_size=28,
    yaxis_title_text=texts['y_axis_title'],
    font=dict(
        family="Arial",
        size=14
    ),
    showlegend=False,
    plot_bgcolor='white',
    xaxis=dict(
        showline=True,
        linewidth=1,
        linecolor='black',
        mirror=True,
        tickmode='array',
        tickvals=[d['x'] for d in chart_data],
        ticktext=[str(d['x']) for d in chart_data],
        title_text=texts['x_axis_title']
    ),
    yaxis=dict(
        showline=True,
        linewidth=1,
        linecolor='black',
        mirror=True,
        gridcolor='#dddddd',
        range=[0, 20000000],
        zeroline=False
    ),
    margin=dict(l=90, r=40, t=100, b=80)
)

base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_image_path = f"{base_filename}.png"

fig.write_image(output_image_path, scale=2)

print(f"Chart saved to {output_image_path}")