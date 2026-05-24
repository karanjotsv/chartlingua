import sys
import json
import os
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print(f"Usage: python {os.path.basename(sys.argv[0])} <json_file_path>")
    sys.exit(1)

json_file_path = sys.argv[1]

try:
    with open(json_file_path, 'r', encoding='utf-8') as f:
        chart_info = json.load(f)
except Exception as e:
    print(f"Error reading or parsing JSON file: {e}")
    sys.exit(1)

data = chart_info['chart_data']
texts = chart_info['texts']
colors = chart_info['colors']

x_values = [item['x'] for item in data]
y_values = [item['y'] for item in data]

fig = go.Figure()

fig.add_trace(go.Bar(
    x=x_values,
    y=y_values,
    text=y_values,
    textposition='outside',
    marker_color=colors['bar_color'],
    width=0.5,
    textfont=dict(family="Arial", size=12, color='#333333'),
    hoverinfo='none'
))

title_html = (f"<span style='font-size:24pt; color:{colors['title_color']};'><b>{texts['title']}</b></span>"
              f"<br><span style='font-size:16pt; color:{colors['subtitle_color']};'>{texts['subtitle']}</span>")

fig.update_layout(
    title=dict(
        text=title_html,
        y=0.95,
        x=0.5,
        xanchor='center',
        yanchor='top'
    ),
    xaxis=dict(
        tickvals=x_values,
        ticktext=[str(x) for x in x_values],
        showline=True,
        linewidth=1,
        linecolor='lightgrey',
        showgrid=False,
        zeroline=False
    ),
    yaxis=dict(
        visible=False,
        range=[0, max(y_values) * 1.2]
    ),
    plot_bgcolor='white',
    paper_bgcolor='white',
    font_family="Arial",
    showlegend=False,
    margin=dict(t=120, b=60, l=40, r=40)
)

base_filename = os.path.splitext(os.path.basename(json_file_path))[0]
output_image_path = f"{base_filename}.png"

fig.write_image(output_image_path, scale=2)

print(f"Chart successfully generated and saved to {output_image_path}")