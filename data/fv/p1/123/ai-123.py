import sys
import json
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print("Usage: python <script_name>.py <path_to_json>")
    sys.exit(1)

json_path = sys.argv[1]

try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_config = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at '{json_path}'")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from '{json_path}'")
    sys.exit(1)

chart_data = chart_config.get('chart_data', [])
texts = chart_config.get('texts', {})
colors = chart_config.get('colors', [])

labels = [item['category'] for item in chart_data]
values = [item['value'] for item in chart_data]
text_labels = [item['text_label'] for item in chart_data]

fig = go.Figure(data=[go.Pie(
    labels=labels,
    values=values,
    text=text_labels,
    textinfo='text',
    textposition='outside',
    marker={'colors': colors},
    hoverinfo='label+percent+value',
    sort=False,
    direction='clockwise'
)])

title_text = texts.get('title')
if texts.get('subtitle'):
    title_text = f"<b>{title_text}</b><br>{texts.get('subtitle')}"

fig.update_layout(
    title_text=title_text,
    title_x=0.5,
    font=dict(
        family="Arial",
        size=12,
        color="black"
    ),
    legend=dict(
        traceorder='normal',
        x=1,
        y=0.5,
        xanchor='left',
        yanchor='middle'
    ),
    margin=dict(l=40, r=200, t=80, b=40)
)

fig.update_traces(
    textfont=dict(
        family="Arial",
        size=12
    )
)

base_name = json_path
if '/' in base_name:
    base_name = base_name.split('/')[-1]
if '\\' in base_name:
    base_name = base_name.split('\\')[-1]
if '.' in base_name:
    base_name = base_name.rsplit('.', 1)[0]

output_filename = base_name + '.png'

fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")