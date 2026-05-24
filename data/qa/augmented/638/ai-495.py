import sys
import json
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print("Usage: python script.py <json_file_path>")
    sys.exit(1)

json_file_path = sys.argv[1]

try:
    with open(json_file_path, 'r', encoding='utf-8') as f:
        chart_details = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_file_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_file_path}")
    sys.exit(1)

data = chart_details['chart_data']
texts = chart_details['texts']
colors = chart_details['colors']

categories = [item['category'] for item in data]
values = [item['value'] for item in data]

fig = go.Figure()

fig.add_trace(go.Bar(
    x=categories,
    y=values,
    marker_color=colors[0],
    text=values,
    textposition='outside',
    texttemplate='%{text:.2f}',
    cliponaxis=False 
))

fig.update_layout(
    font=dict(family="Arial"),
    plot_bgcolor='white',
    xaxis=dict(
        title_text=texts['x_axis_title'],
        showgrid=False,
        linecolor='black',
        ticks='outside'
    ),
    yaxis=dict(
        title_text=texts['y_axis_title'],
        range=[0, 5],
        gridcolor='#e0e0e0',
        griddash='dot',
        zeroline=False,
        linecolor='black'
    ),
    margin=dict(l=80, r=40, t=50, b=100),
    showlegend=False,
    annotations=[
        dict(
            text=texts['source'],
            align='right',
            showarrow=False,
            xref='paper',
            yref='paper',
            x=1.0,
            y=-0.18,
            xanchor='right',
            yanchor='top'
        )
    ]
)

fig.update_traces(textfont_size=12, textfont_color='black')

base_filename = json_file_path.rsplit('.', 1)[0]
output_filename = f"{base_filename}.png"

fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")