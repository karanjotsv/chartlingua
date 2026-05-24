import sys
import json
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print(f"Usage: python {sys.argv[0]} <json_file_path>")
    sys.exit(1)

json_path = sys.argv[1]

try:
    with open(json_path, 'r', encoding='utf-8') as f:
        config = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_path}")
    sys.exit(1)

chart_data = config.get('chart_data', [])
texts = config.get('texts', {})
colors = config.get('colors', [])

labels = [item.get('label', '') for item in chart_data]
values = [item.get('value', 0) for item in chart_data]

fig = go.Figure()

fig.add_trace(go.Pie(
    labels=labels,
    values=values,
    marker=dict(colors=colors, line=dict(color='black', width=2)),
    hoverinfo='label+percent',
    textinfo='none',
    sort=False,
    direction='clockwise',
    rotation=90
))

title_text = texts.get('title', '')
if texts.get('subtitle'):
    title_text += f"<br><sub>{texts['subtitle']}</sub>"

fig.update_layout(
    title_text=title_text,
    title_x=0.5,
    title_y=0.95,
    title_font=dict(
        family="Arial",
        size=28,
        color='white'
    ),
    font=dict(
        family="Arial",
        size=14,
        color='white'
    ),
    showlegend=True,
    legend=dict(
        x=0.8,
        y=0.55,
        bgcolor='rgba(0,0,0,0)',
        bordercolor='rgba(0,0,0,0)',
        font=dict(family="Arial")
    ),
    paper_bgcolor='black',
    plot_bgcolor='black',
    margin=dict(l=20, r=20, t=100, b=20)
)

# Derive output filename from input JSON path, handling different path separators
base_filename = json_path.split('/')[-1].split('\\')[-1]
if base_filename.lower().endswith('.json'):
    base_filename = base_filename[:-5]

output_filename = f"{base_filename}.png"

fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")