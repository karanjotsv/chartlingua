import sys
import json
import plotly.graph_objects as go
import pathlib

if len(sys.argv) != 2:
    print(f"Usage: {pathlib.Path(__file__).name} <json_file_path>")
    sys.exit(1)

json_file_path = pathlib.Path(sys.argv[1])
if not json_file_path.is_file():
    print(f"Error: File not found at {json_file_path}")
    sys.exit(1)

with open(json_file_path, 'r', encoding='utf-8') as f:
    chart_spec = json.load(f)

data = chart_spec['chart_data']
texts = chart_spec['texts']
colors = chart_spec['colors']

# Plotly plots y-axis from bottom to top, so we reverse the data lists
# to match the visual order of the original image (top to bottom).
categories = [item['category'] for item in data][::-1]
values = [item['value'] for item in data][::-1]
text_labels = [str(item['value']) for item in data][::-1]

fig = go.Figure()

fig.add_trace(go.Bar(
    y=categories,
    x=values,
    orientation='h',
    marker=dict(
        color=colors[0],
        line=dict(width=0)
    ),
    text=text_labels,
    textposition='inside',
    insidetextanchor='end',
    textfont=dict(
        family="Arial",
        size=18,
        color='white',
        weight='bold'
    ),
    hoverinfo='none'
))

fig.update_layout(
    title=dict(
        text=texts['title'],
        font=dict(
            family="Arial",
            size=26,
            color='#000000',
            weight='bold'
        ),
        x=0.05,
        y=0.95,
        xanchor='left',
        yanchor='top'
    ),
    xaxis=dict(
        visible=False,
        range=[0, max(values) * 1.1]  # Ensure space for text inside bars
    ),
    yaxis=dict(
        showline=False,
        showgrid=False,
        tickfont=dict(
            family="Arial",
            size=20,
            color='#000000'
        )
    ),
    plot_bgcolor='white',
    paper_bgcolor='white',
    showlegend=False,
    margin=dict(l=220, r=40, t=100, b=20),
    height=450,
    autosize=False
)

output_filename = f"{json_file_path.stem}.png"
fig.write_image(output_filename, scale=2)
print(f"Chart saved to {output_filename}")