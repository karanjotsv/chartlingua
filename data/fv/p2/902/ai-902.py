import sys
import json
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print("Usage: python <script_name>.py <json_file_path>")
    sys.exit(1)

json_path = sys.argv[1]

try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_info = json.load(f)
except (FileNotFoundError, json.JSONDecodeError) as e:
    print(f"Error: Could not read or parse the JSON file. {e}")
    sys.exit(1)

chart_data = chart_info['chart_data']
texts = chart_info['texts']
colors = chart_info['colors']

categories = [item['category'] for item in chart_data]
values = [item['value'] for item in chart_data]

fig = go.Figure()

fig.add_trace(go.Bar(
    y=categories,
    x=values,
    orientation='h',
    marker_color=colors[0],
    hoverinfo='none'
))

title_text = texts['title']
if texts.get('subtitle'):
    title_text += f"<br><sub>{texts['subtitle']}</sub>"

fig.update_layout(
    title=dict(
        text=title_text,
        x=0.5,
        xanchor='center',
        font=dict(size=18)
    ),
    xaxis=dict(
        title=texts['x_axis_title'],
        showgrid=True,
        gridcolor='lightgray',
        zeroline=False,
        showline=True,
        linewidth=1.5,
        linecolor='black',
        mirror=True
    ),
    yaxis=dict(
        title=texts['y_axis_title'],
        showline=True,
        linewidth=1.5,
        linecolor='black',
        mirror=True,
        autorange="reversed"
    ),
    font=dict(
        family="Arial",
        size=12
    ),
    plot_bgcolor='white',
    paper_bgcolor='white',
    showlegend=False,
    margin=dict(l=250, r=30, t=80, b=80)
)

base_filename = json_path.rsplit('.', 1)[0]
output_filename = f"{base_filename}.png"

fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")