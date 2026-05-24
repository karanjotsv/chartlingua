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
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_path}")
    sys.exit(1)

chart_data = chart_info['chart_data']
texts = chart_info['texts']
colors = chart_info['colors']

labels = [item['label'] for item in chart_data]
values = [item['value'] for item in chart_data]
text_labels = [f"{v:.2f}%".replace('.', ',') for v in values]

fig = go.Figure()

fig.add_trace(go.Pie(
    labels=labels,
    values=values,
    marker=dict(colors=colors, line=dict(color='#FFFFFF', width=1)),
    hoverinfo='label+percent',
    textinfo='text',
    text=text_labels,
    textposition='outside',
    sort=False,
    direction='clockwise',
    rotation=60
))

fig.update_layout(
    title_text=texts['title'],
    title_x=0.5,
    font=dict(
        family="Arial",
        size=14,
        color="black"
    ),
    showlegend=True,
    legend=dict(
        orientation="v",
        yanchor="top",
        y=0.85,
        xanchor="right",
        x=1.1
    ),
    margin=dict(l=40, r=180, t=80, b=40),
    paper_bgcolor='white',
    plot_bgcolor='white'
)

fig.update_traces(textfont_size=12)

# Derive the output filename from the input JSON path without using os module
filename_with_ext = json_path.replace('\\', '/').split('/')[-1]
filename_base = filename_with_ext.rsplit('.', 1)[0]
output_filename = f"{filename_base}.png"

fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")