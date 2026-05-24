import sys
import json
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print("Usage: python script.py <path_to_json>")
    sys.exit(1)

json_path = sys.argv[1]

try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_info = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_path}")
    sys.exit(1)

chart_data = chart_info.get('chart_data', [])
texts = chart_info.get('texts', {})
colors = chart_info.get('colors', [])

# Reverse data for correct plotting order in Plotly horizontal bar charts
chart_data.reverse()

categories = [item['category'] for item in chart_data]
values = [item['value'] for item in chart_data]

fig = go.Figure()

fig.add_trace(go.Bar(
    y=categories,
    x=values,
    orientation='h',
    marker=dict(color=colors[0]),
    text=[f"{v}%" for v in values],
    textposition='outside',
    cliponaxis=False 
))

fig.update_layout(
    title_text=texts.get('title'),
    font=dict(family="Arial", size=12, color="black"),
    xaxis=dict(
        title=texts.get('x_axis_title'),
        range=[0, 110],
        dtick=10,
        ticksuffix='%',
        showgrid=True,
        gridcolor='#dddddd',
        zeroline=False
    ),
    yaxis=dict(
        title=texts.get('y_axis_title'),
        showgrid=False,
        zeroline=False,
        showline=False,
        autorange="reversed" # This is another way to handle order, but we already reversed the data
    ),
    plot_bgcolor='white',
    paper_bgcolor='white',
    margin=dict(l=150, r=60, t=40, b=60),
    showlegend=False,
    annotations=[
        dict(
            xref='paper', yref='paper',
            x=1.0, y=-0.1,
            xanchor='right', yanchor='top',
            text=texts.get('source'),
            showarrow=False,
            font=dict(size=10, color='grey')
        )
    ]
)

# Reverse autorange again to ensure correct visual order if data wasn't reversed
fig.update_yaxes(autorange=True)

output_filename_base = json_path.rsplit('.', 1)[0]
output_filename_png = f"{output_filename_base}.png"

fig.write_image(output_filename_png, scale=2)

print(f"Chart saved to {output_filename_png}")