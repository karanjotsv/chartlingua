import sys
import json
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print("Usage: python <script_name>.py <json_file_path>")
    sys.exit(1)

json_file_path = sys.argv[1]

with open(json_file_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

chart_data = data['chart_data']
texts = data['texts']
colors = data['colors']
background_color = data['background_color']

labels = [item['label'] for item in chart_data]
values = [item['value'] for item in chart_data]

fig = go.Figure(data=[go.Pie(
    labels=labels,
    values=values,
    marker_colors=colors,
    sort=False,
    direction='clockwise',
    textinfo='percent',
    textposition='outside',
    textfont=dict(size=14)
)])

fig.update_layout(
    title_text=texts['title'],
    title_x=0.5,
    title_font_size=24,
    font_family="Arial",
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=-0.2,
        xanchor="center",
        x=0.5,
        traceorder='normal'
    ),
    paper_bgcolor=background_color,
    plot_bgcolor=background_color,
    margin=dict(l=60, r=60, t=120, b=120)
)

output_filename_base = json_file_path.rsplit('.', 1)[0]
output_filename = f"{output_filename_base}.png"

fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")