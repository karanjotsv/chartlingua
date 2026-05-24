import sys
import json
import os
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
    sys.exit(f"Error: Could not decode JSON from {json_path}")

chart_data = config['chart_data']
texts = config['texts']
colors = config['colors']

x_vals = [d['x'] for d in chart_data]
y_vals = [d['y'] for d in chart_data]

fig = go.Figure()

fig.add_trace(go.Bar(
    x=x_vals,
    y=y_vals,
    text=y_vals,
    textposition='outside',
    cliponaxis=False,
    marker_color=colors[0],
    textfont=dict(color='black', size=12, family="Arial")
))

fig.update_layout(
    title=dict(
        text=texts['title'],
        x=0.5,
        xanchor='center',
        yanchor='top',
        y=0.95
    ),
    xaxis=dict(
        title_text=texts['x_axis_title'],
        tickvals=x_vals,
        ticktext=[str(x) for x in x_vals],
        showline=True,
        linecolor='black',
        gridcolor='black',
        mirror=True,
        ticks='inside'
    ),
    yaxis=dict(
        title_text=texts['y_axis_title'],
        range=[0, 950],
        dtick=100,
        showline=True,
        linecolor='black',
        gridcolor='black',
        mirror=True,
        ticks='inside',
        zeroline=True,
        zerolinecolor='black',
        zerolinewidth=1
    ),
    annotations=[
        dict(
            xref="paper",
            yref="paper",
            x=0.5,
            y=-0.22,
            showarrow=False,
            text=texts['source_note'],
            xanchor='center',
            yanchor='top'
        )
    ],
    plot_bgcolor='white',
    paper_bgcolor='white',
    font=dict(family="Arial", color='black'),
    margin=dict(t=80, b=120, l=80, r=40)
)

base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_image_path = f"{base_filename}.png"

fig.write_image(output_image_path, scale=2)

print(f"Generated chart and saved to {output_image_path}")