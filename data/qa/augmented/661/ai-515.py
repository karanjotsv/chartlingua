import sys
import json
import pathlib
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print("Usage: python script.py <json_file_path>")
    sys.exit(1)

json_file_path = sys.argv[1]

try:
    with open(json_file_path, 'r', encoding='utf-8') as f:
        chart_config = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_file_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_file_path}")
    sys.exit(1)

chart_data = chart_config.get('chart_data', [])
texts = chart_config.get('texts', {})
colors = chart_config.get('colors', [])

categories = [item['category'] for item in chart_data]
values = [item['value'] for item in chart_data]
display_texts = [item['display_text'] for item in chart_data]

fig = go.Figure()

fig.add_trace(go.Bar(
    x=categories,
    y=values,
    text=display_texts,
    textposition='auto',
    insidetextanchor='end',
    marker_color=colors[0] if colors else None,
    textfont=dict(family="Arial", size=12, color='black'),
    hoverinfo='none'
))

fig.update_layout(
    font=dict(family="Arial"),
    title_text=texts.get('title'),
    yaxis_title_text=texts.get('y_axis_title'),
    xaxis_title_text=texts.get('x_axis_title'),
    plot_bgcolor='white',
    showlegend=False,
    bargap=0.35,
    margin=dict(l=80, r=40, t=40, b=120),
    yaxis=dict(
        range=[0, 80000],
        gridcolor='#E5E5E5',
        showline=False,
        zeroline=False,
        tickprefix=' ',
        ticksuffix=' '
    ),
    xaxis=dict(
        showline=True,
        linewidth=1,
        linecolor='black',
        tickfont=dict(size=12)
    ),
    annotations=[
        dict(
            text=texts.get('source'),
            showarrow=False,
            xref='paper',
            yref='paper',
            x=1.0,
            y=-0.2,
            xanchor='right',
            yanchor='top',
            align='right'
        )
    ]
)

# Set text position to be inside but right at the top of the bar
fig.update_traces(textposition='inside', insidetextanchor='end', textangle=0)


input_path = pathlib.Path(json_file_path)
output_filename = input_path.with_suffix('.png')

fig.write_image(str(output_filename), scale=2)

print(f"Chart saved to {output_filename}")