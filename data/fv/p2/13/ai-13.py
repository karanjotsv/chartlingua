import sys
import json
import os
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print("Usage: python <script_name>.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]

try:
    with open(json_path, 'r', encoding='utf-8') as f:
        config = json.load(f)
except (FileNotFoundError, json.JSONDecodeError) as e:
    print(f"Error reading or parsing JSON file: {e}")
    sys.exit(1)

chart_data = config.get('chart_data', [])
texts = config.get('texts', {})
colors = config.get('colors', {})

labels = [item['category'] for item in chart_data]
values = [item['value'] for item in chart_data]
slice_colors = colors.get('slices')
text_colors = colors.get('text_on_slice')

fig = go.Figure()

fig.add_trace(go.Pie(
    labels=labels,
    values=values,
    marker=dict(
        colors=slice_colors,
        line=dict(color='white', width=2)
    ),
    textinfo='percent',
    texttemplate='%{value}%',
    textfont=dict(
        family="Arial",
        size=18,
        color='white'  # Default color
    ),
    textfont_colors=text_colors,
    hoverinfo='label+percent',
    sort=False,
    direction='clockwise'
))

fig.update_layout(
    title=dict(
        text=f"<b>{texts.get('title', '')}</b>",
        font=dict(size=30, color='black'),
        x=0.5,
        xanchor='center'
    ),
    font=dict(
        family="Arial",
        size=16
    ),
    showlegend=True,
    legend=dict(
        x=0.8,
        y=0.5,
        xanchor='left',
        yanchor='middle',
        font=dict(size=16)
    ),
    paper_bgcolor='white',
    plot_bgcolor='white',
    margin=dict(t=100, b=40, l=40, r=250)
)

base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_filename}.png"

fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")