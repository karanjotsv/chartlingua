import sys
import json
import os
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print("Usage: python <script_name>.py <json_file_path>")
    sys.exit(1)

json_path = sys.argv[1]

with open(json_path, 'r', encoding='utf-8') as f:
    config = json.load(f)

chart_data = config['chart_data']
texts = config['texts']
colors = config['colors']

categories = [item['category'] for item in chart_data]
values = [item['value'] for item in chart_data]
label_colors = [item['label_color'] for item in chart_data]

fig = go.Figure()

fig.add_trace(go.Bar(
    y=categories,
    x=values,
    orientation='h',
    marker=dict(color=colors['bar_color']),
    text=values,
    texttemplate='%{text:,.0f}',
    textposition='outside',
    textfont=dict(
        family="Arial",
        size=11,
        color=label_colors
    ),
    cliponaxis=False
))

for i, category in enumerate(categories):
    fig.add_annotation(
        xref='paper',
        yref='y',
        x=-0.01,
        y=category,
        text=category,
        showarrow=False,
        font=dict(
            family="Arial",
            size=12,
            color=label_colors[i]
        ),
        xanchor='right',
        align='right'
    )

fig.update_layout(
    title=dict(
        text=texts['title'],
        x=0.5,
        y=0.97,
        font=dict(size=18)
    ),
    xaxis=dict(
        title=texts['x_axis_title'],
        showgrid=True,
        gridcolor='#E0E0E0',
        gridwidth=1,
        zeroline=False,
        automargin=True
    ),
    yaxis=dict(
        autorange="reversed",
        showticklabels=False,
        ticksuffix="  "
    ),
    font=dict(
        family="Arial",
        size=12
    ),
    plot_bgcolor=colors['background_color'],
    paper_bgcolor=colors['background_color'],
    showlegend=False,
    margin=dict(l=360, r=60, t=100, b=50)
)

base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_image_path = f"{base_filename}.png"

fig.write_image(output_image_path, scale=2)

print(f"Chart generated and saved to {output_image_path}")