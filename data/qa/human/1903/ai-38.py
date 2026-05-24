import sys
import json
import os
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print("Usage: python script.py <path_to_json_file>")
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

categories = [item['category'] for item in chart_data]
values = [item['value'] for item in chart_data]

fig = go.Figure()

fig.add_trace(go.Bar(
    x=categories,
    y=values,
    marker_color=colors[0] if colors else '#2979FF',
    text=[str(v) for v in values],
    textposition='outside',
    cliponaxis=False 
))

fig.update_layout(
    font=dict(
        family="Arial",
        size=12,
        color="black"
    ),
    plot_bgcolor='white',
    paper_bgcolor='white',
    showlegend=False,
    margin=dict(l=80, r=40, t=50, b=100),
    yaxis=dict(
        title=texts.get('yaxis_title'),
        range=[0, 8.5],
        showgrid=True,
        gridcolor='#EAEAEA',
        gridwidth=1,
        griddash='dot',
        zeroline=False,
        ticks='outside',
        ticklen=5,
        tickcolor='lightgrey'
    ),
    xaxis=dict(
        showgrid=False,
        zeroline=False,
        showline=True,
        linecolor='lightgrey'
    ),
    annotations=[
        dict(
            showarrow=False,
            text=texts.get('source', ''),
            xref='paper',
            yref='paper',
            x=0.98,
            y=-0.18,
            xanchor='right',
            yanchor='top',
            font=dict(size=12, color='grey')
        )
    ]
)

fig.update_traces(textfont_size=12, textfont_color='black')


base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_filename}.png"

fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")