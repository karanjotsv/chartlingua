import sys
import json
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print("Usage: python recreate_chart.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]

try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_info = json.load(f)
except FileNotFoundError:
    print(f"Error: The file '{json_path}' was not found.")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: The file '{json_path}' is not a valid JSON file.")
    sys.exit(1)


data = chart_info['chart_data']
texts = chart_info['texts']
colors = chart_info['colors']

labels = [item['label'] for item in data]
values = [item['value'] for item in data]

fig = go.Figure()

fig.add_trace(go.Pie(
    labels=labels,
    values=values,
    marker=dict(colors=colors, line=dict(color='#FFFFFF', width=2)),
    textinfo='percent',
    hoverinfo='label+percent',
    sort=False,
    direction='clockwise',
    textfont=dict(family="Arial", size=16, color='black', weight='bold')
))

title_text = ""
if texts.get("title"):
    title_text += f'<b>{texts["title"]}</b>'
if texts.get("subtitle"):
    title_text += f'<br><sub>{texts["subtitle"]}</sub>'

fig.update_layout(
    title_text=title_text,
    title_x=0.5,
    font=dict(family="Arial", size=12, color="black"),
    showlegend=True,
    legend=dict(
        orientation="v",
        yanchor="top",
        y=0.9,
        xanchor="left",
        x=1.02,
        font=dict(size=14)
    ),
    margin=dict(l=20, r=450, t=80, b=20),
    paper_bgcolor='white',
    plot_bgcolor='white'
)

output_filename_base = json_path.rsplit('.', 1)[0]
output_filename_png = f"{output_filename_base}.png"

fig.write_image(output_filename_png, scale=2, width=1000, height=600)

print(f"Chart saved to {output_filename_png}")