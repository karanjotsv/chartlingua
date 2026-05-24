import sys
import json
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print("Usage: python script.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]

try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_data = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_path}")
    sys.exit(1)

data = chart_data.get('chart_data', [])
texts = chart_data.get('texts', {})
colors = chart_data.get('colors', [])

labels = [item['label'] for item in data]
values = [item['value'] for item in data]

fig = go.Figure()

fig.add_trace(go.Pie(
    labels=labels,
    values=values,
    marker=dict(colors=colors, line=dict(color='#FFFFFF', width=1)),
    hoverinfo='label+percent',
    textinfo='none',
    sort=False,
    direction='clockwise'
))

fig.update_layout(
    title_text=texts.get('title'),
    font=dict(
        family="Arial",
        size=12,
        color="black"
    ),
    showlegend=True,
    legend=dict(
        x=0.98,
        y=0.5,
        xanchor='left',
        yanchor='middle',
        bgcolor='rgba(0,0,0,0)',
        traceorder='normal'
    ),
    margin=dict(l=40, r=220, t=60, b=40),
    paper_bgcolor='white',
    plot_bgcolor='white'
)

output_filename_base = json_path.rsplit('.', 1)[0]
output_filename_png = f"{output_filename_base}.png"

fig.write_image(output_filename_png, scale=2)

print(f"Chart saved to {output_filename_png}")