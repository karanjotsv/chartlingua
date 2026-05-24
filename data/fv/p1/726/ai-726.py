import sys
import json
import os
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print(f"Usage: python {os.path.basename(__file__)} <json_file_path>")
    sys.exit(1)

json_path = sys.argv[1]

if not os.path.exists(json_path):
    print(f"Error: File not found at {json_path}")
    sys.exit(1)

try:
    with open(json_path, 'r', encoding='utf-8') as f:
        config = json.load(f)
except json.JSONDecodeError:
    print(f"Error: Invalid JSON format in {json_path}")
    sys.exit(1)

chart_data = config.get('chart_data', [])
texts = config.get('texts', {})
colors = config.get('colors', [])

labels = [item.get('label') for item in chart_data]
values = [item.get('value') for item in chart_data]

fig = go.Figure()

fig.add_trace(go.Pie(
    labels=labels,
    values=values,
    marker=dict(colors=colors, line=dict(color='#ffffff', width=1)),
    texttemplate="%{label}<br>%{value}%",
    textposition='outside',
    sort=False,
    direction='clockwise',
    hoverinfo='label+percent'
))

fig.update_layout(
    showlegend=False,
    plot_bgcolor='white',
    paper_bgcolor='white',
    margin=dict(l=80, r=80, t=80, b=80),
    font=dict(family="Arial", size=12, color="black"),
    annotations=[
        dict(
            text=texts.get('title'),
            align='left',
            showarrow=False,
            xref='paper',
            yref='paper',
            x=0.95,
            y=0.8,
            xanchor='left',
            yanchor='top',
            font=dict(family="Arial", size=16, color="black")
        )
    ]
)

fig.update_traces(textfont_size=12)

base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_image_path = f"{base_filename}.png"

try:
    fig.write_image(output_image_path, scale=2, width=1000, height=700)
    print(f"Chart successfully saved to {output_image_path}")
except Exception as e:
    print(f"Error writing image file: {e}")
    print("Please ensure you have 'kaleido' installed: pip install kaleido")
    sys.exit(1)