import sys
import json
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

chart_data = chart_info['chart_data']
texts = chart_info['texts']
colors = chart_info['colors']
categories = chart_data['categories']

fig = go.Figure()

for i, series in enumerate(chart_data['series']):
    color = colors[i]
    fig.add_trace(go.Scatter(
        x=categories,
        y=series['y'],
        name=series['name'],
        mode='lines+markers+text',
        line=dict(color=color, width=2.5),
        marker=dict(color=color, size=7),
        text=series['y'],
        textposition='top center',
        textfont=dict(
            family="Arial",
            size=12,
            color=color
        ),
        hoverinfo='skip'
    ))

# Add alternating background vertical rectangles
for year in range(categories[0] + 1, categories[-1] + 1, 2):
     fig.add_vrect(x0=year - 0.5, x1=year + 0.5, fillcolor="#F8F9FA", layer="below", line_width=0)


fig.update_layout(
    font=dict(family="Arial", size=12),
    plot_bgcolor='white',
    paper_bgcolor='white',
    margin=dict(l=80, r=40, t=40, b=120),
    xaxis=dict(
        tickmode='array',
        tickvals=categories,
        ticktext=[str(c) for c in categories],
        showgrid=False,
        showline=True,
        linewidth=1,
        linecolor='lightgrey'
    ),
    yaxis=dict(
        title=texts['y_axis_title'],
        range=[77.5, 88.5],
        showgrid=True,
        gridcolor='#EAEAEA',
        gridwidth=1,
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
            x=1,
            y=-0.35,
            text=texts['source'],
            showarrow=False,
            xanchor='right',
            yanchor='bottom',
            font=dict(size=12)
        )
    ]
)

# Derive output filename from input JSON path
base_name = json_path.split('/')[-1].split('.')[0]
output_filename = f"{base_name}.png"

fig.write_image(output_filename, scale=2)
print(f"Chart saved to {output_filename}")