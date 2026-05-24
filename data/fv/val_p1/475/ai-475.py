import sys
import json
import os
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print(f"Usage: python {os.path.basename(sys.argv[0])} <json_file_path>", file=sys.stderr)
    sys.exit(1)

json_path = sys.argv[1]

try:
    with open(json_path, 'r', encoding='utf-8') as f:
        config = json.load(f)
except FileNotFoundError:
    print(f"Error: File not found at {json_path}", file=sys.stderr)
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Invalid JSON format in {json_path}", file=sys.stderr)
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
    marker=dict(colors=colors, line=dict(color='#000000', width=1)),
    sort=False,
    direction='clockwise',
    hoverinfo='label+percent',
    textinfo='none',
    domain=dict(y=[0.2, 0.85]) 
))

title_text = f"<b>{texts.get('title', '')}</b>"
if texts.get('subtitle'):
    title_text += f"<br>{texts.get('subtitle')}"

annotations = []
if texts.get('source'):
    annotations.append(
        dict(
            text=texts.get('source'),
            align='left',
            showarrow=False,
            xref='paper',
            yref='paper',
            x=0.0,
            y=0.0,
            xanchor='left',
            yanchor='bottom',
            font=dict(size=10)
        )
    )

fig.update_layout(
    title={
        'text': title_text,
        'y': 0.95,
        'x': 0.5,
        'xanchor': 'center',
        'yanchor': 'top'
    },
    legend={
        'orientation': 'v',
        'yanchor': 'top',
        'y': 0.18,
        'xanchor': 'center',
        'x': 0.5,
        'borderwidth': 1,
        'bordercolor': 'black'
    },
    font=dict(
        family="Arial",
        size=12
    ),
    margin=dict(l=20, r=20, b=80, t=100),
    paper_bgcolor='white',
    annotations=annotations,
    width=600,
    height=750
)

base_name = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_name}.png"

fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")