import sys
import json
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print("Usage: python <script_name>.py <json_file_path>")
    sys.exit(1)

json_path = sys.argv[1]

try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_details = json.load(f)
except FileNotFoundError:
    print(f"Error: The file {json_path} was not found.")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: The file {json_path} is not a valid JSON.")
    sys.exit(1)

fig = go.Figure()

data = chart_details['chart_data']
texts = chart_details['texts']
colors = chart_details['colors']
categories = data['categories']

for i, series in enumerate(data['series']):
    fig.add_trace(go.Bar(
        name=series['name'],
        x=categories,
        y=series['values'],
        marker_color=colors[i],
        text=series['values'],
        texttemplate='%{y}%',
        textposition='outside',
        textfont=dict(family="Arial", size=12, color='black'),
        cliponaxis=False
    ))

fig.update_layout(
    barmode='group',
    plot_bgcolor='white',
    font=dict(family="Arial", size=12),
    margin=dict(l=60, r=40, t=40, b=150),
    xaxis=dict(
        title_text=texts['x_axis_title'],
        showgrid=False,
        showline=True,
        linecolor='black',
        categoryorder='array',
        categoryarray=categories
    ),
    yaxis=dict(
        title_text=texts['y_axis_title'],
        range=[0, 72],
        tickvals=[i for i in range(0, 71, 10)],
        showgrid=True,
        gridcolor='#E5E5E5',
        ticksuffix='%',
        zeroline=False
    ),
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=-0.3,
        xanchor="center",
        x=0.5
    ),
    annotations=[
        dict(
            xref='paper',
            yref='paper',
            x=0.99,
            y=-0.45,
            text=texts['source'],
            showarrow=False,
            align='right',
            xanchor='right',
            yanchor='bottom',
            font=dict(size=12, color='grey')
        )
    ]
)

output_filename_base = json_path.rsplit('.', 1)[0]
output_path = f"{output_filename_base}.png"
fig.write_image(output_path, scale=2)

print(f"Chart generated and saved to {output_path}")