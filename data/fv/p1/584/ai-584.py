import sys
import json
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print("Usage: python create_chart.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]

try:
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
except FileNotFoundError:
    print(f"Error: File not found at {json_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Invalid JSON format in {json_path}")
    sys.exit(1)

chart_data = data.get('chart_data', [])
texts = data.get('texts', {})
colors = data.get('colors', [])

labels = [item.get('category') for item in chart_data]
values = [item.get('value') for item in chart_data]

fig = go.Figure()

fig.add_trace(go.Pie(
    labels=labels,
    values=values,
    marker=dict(
        colors=colors,
        line=dict(color='#000000', width=1)
    ),
    textinfo='label+percent',
    textposition='outside',
    sort=False,
    insidetextorientation='radial'
))

title_text = texts.get('title', '')
if texts.get('subtitle'):
    title_text += f"<br><sub>{texts.get('subtitle')}</sub>"

fig.update_layout(
    title_text=title_text,
    title_x=0.5,
    font=dict(
        family="Arial",
        size=14
    ),
    showlegend=False,
    paper_bgcolor='white',
    plot_bgcolor='white',
    margin=dict(l=100, r=100, t=80, b=40)
)

fig.update_traces(
    textfont=dict(
        family="Arial",
        size=12,
        color='black'
    )
)

base_name = json_path
if '/' in base_name:
    base_name = base_name.rsplit('/', 1)[1]
if '\\' in base_name:
    base_name = base_name.rsplit('\\', 1)[1]

if '.' in base_name:
    base_name = base_name.rsplit('.', 1)[0]

output_filename = base_name + '.png'

fig.write_image(output_filename, scale=2)

print(f"Chart saved as {output_filename}")