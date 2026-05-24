import sys
import json
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print(f"Usage: python {sys.argv[0]} <json_file_path>")
    sys.exit(1)

json_file_path = sys.argv[1]

try:
    with open(json_file_path, 'r', encoding='utf-8') as f:
        config = json.load(f)
except FileNotFoundError:
    print(f"Error: File not found at {json_file_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_file_path}")
    sys.exit(1)

chart_data = config['chart_data']
texts = config['texts']
colors = config['colors']

categories = [item['category'] for item in chart_data]
values = [item['value'] for item in chart_data]
display_texts = [item['display_text'] for item in chart_data]

fig = go.Figure()

fig.add_trace(go.Bar(
    x=categories,
    y=values,
    text=display_texts,
    textposition='outside',
    marker_color=colors[0],
    cliponaxis=False
))

fig.update_layout(
    font=dict(family="Arial", size=12),
    plot_bgcolor='white',
    paper_bgcolor='white',
    margin=dict(l=90, r=20, t=50, b=150),
    showlegend=False,
    xaxis=dict(
        title_text=texts['x_axis_title'],
        showgrid=False,
        zeroline=False,
        linecolor='black',
        automargin=True
    ),
    yaxis=dict(
        title_text=texts['y_axis_title'],
        showgrid=True,
        gridcolor='#e0e0e0',
        griddash='dot',
        zeroline=False,
        range=[0, 40],
        dtick=10,
        ticksuffix='%'
    ),
    annotations=[
        dict(
            showarrow=False,
            text=texts.get('source', ''),
            xref="paper",
            yref="paper",
            x=1.0,
            y=-0.32,
            xanchor='right',
            yanchor='bottom',
            align='right',
            font=dict(size=12)
        )
    ]
)

fig.update_traces(textfont_size=12, textfont_color='black')

base_filename = json_file_path.split('/')[-1].rsplit('.', 1)[0]
output_image_filename = f"{base_filename}.png"

fig.write_image(output_image_filename, scale=2)

print(f"Chart saved to {output_image_filename}")