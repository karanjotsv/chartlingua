import sys
import json
import pathlib
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print("Usage: python script.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_data = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at '{json_path}'")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from '{json_path}'")
    sys.exit(1)

data_config = chart_data.get('chart_data', [])
texts = chart_data.get('texts', {})
colors = chart_data.get('colors', [])

labels = [item['label'] for item in data_config]
values = [item['value'] for item in data_config]

fig = go.Figure()

fig.add_trace(go.Pie(
    labels=labels,
    values=values,
    hole=0.6,
    marker=dict(colors=colors),
    sort=False,
    direction='clockwise',
    hoverinfo='label+percent',
    textinfo='none'
))

title_text = f"<b>{texts.get('title', '')}</b>"
if texts.get('subtitle'):
    title_text += f"<br>{texts.get('subtitle')}"

fig.update_layout(
    title={
        'text': title_text,
        'y': 0.95,
        'x': 0.05,
        'xanchor': 'left',
        'yanchor': 'top'
    },
    font=dict(
        family="Arial",
        size=16
    ),
    showlegend=True,
    legend=dict(
        orientation="v",
        yanchor="top",
        y=0.9,
        xanchor="left",
        x=0.8,
        traceorder='normal',
        font=dict(size=14),
        bgcolor='rgba(255,255,255,0)'
    ),
    paper_bgcolor='white',
    plot_bgcolor='white',
    margin=dict(l=20, r=20, t=80, b=20)
)

base_name = pathlib.Path(json_path).stem
output_filename = f"{base_name}.png"

fig.write_image(output_filename, scale=2)

print(f"Chart saved as {output_filename}")