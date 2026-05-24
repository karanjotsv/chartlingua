import sys
import json
import plotly.graph_objects as go

if len(sys.argv) != 2:
    sys.exit("Usage: python <script_name>.py <json_file_path>")

json_path = sys.argv[1]

try:
    with open(json_path, 'r', encoding='utf-8') as f:
        config = json.load(f)
except FileNotFoundError:
    sys.exit(f"Error: JSON file not found at {json_path}")
except json.JSONDecodeError:
    sys.exit("Error: Could not decode JSON.")

chart_data = config.get('chart_data', [])
texts = config.get('texts', {})
colors = config.get('colors', [])

labels = [d['label'] for d in chart_data]
values = [d['value'] for d in chart_data]
custom_texts = [d.get('text') for d in chart_data]
text_positions = [d.get('position', 'auto') for d in chart_data]

fig = go.Figure()

fig.add_trace(go.Pie(
    labels=labels,
    values=values,
    marker=dict(colors=colors, line=dict(color='black', width=2)),
    hoverinfo='label+percent',
    text=custom_texts,
    textinfo='text',
    textposition=text_positions,
    sort=False,
    direction='clockwise',
    rotation=86.4
))

fig.update_layout(
    title=dict(
        text=texts.get('title'),
        y=0.95,
        x=0.5,
        xanchor='center',
        yanchor='top'
    ),
    font=dict(
        family="Arial",
        size=16
    ),
    showlegend=True,
    legend=dict(
        font=dict(size=14),
        x=0.9,
        y=0.95,
        xanchor='left',
        yanchor='top',
        bgcolor='rgba(255,255,255,0)'
    ),
    margin=dict(l=20, r=150, t=120, b=20),
    paper_bgcolor='white',
    plot_bgcolor='white'
)

fig.update_traces(
    textfont=dict(
        family="Arial",
        size=14,
        color='black'
    ),
    insidetextorientation='horizontal'
)

output_filename_base = json_path.rsplit('.', 1)[0]
output_filename_png = f"{output_filename_base}.png"

fig.write_image(output_filename_png, scale=2)

print(f"Chart saved to {output_filename_png}")