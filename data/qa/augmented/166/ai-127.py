import sys
import json
import pathlib
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print("Usage: python <script_name>.py <json_file_path>", file=sys.stderr)
    sys.exit(1)

json_file_path = pathlib.Path(sys.argv[1])
output_image_path = json_file_path.with_suffix(".png")

with open(json_file_path, 'r', encoding='utf-8') as f:
    config = json.load(f)

chart_data = config['chart_data']
texts = config['texts']
colors = config['colors']

categories = [item['category'] for item in chart_data]
values = [item['value'] for item in chart_data]

# Reverse the data to display from top to bottom in Plotly
categories.reverse()
values.reverse()

# Format numeric labels with spaces as thousand separators
text_labels = [f'{v:,}'.replace(',', ' ') for v in values]

fig = go.Figure()

fig.add_trace(go.Bar(
    y=categories,
    x=values,
    text=text_labels,
    textposition='outside',
    orientation='h',
    marker_color=colors[0],
    cliponaxis=False  # Allow text to be drawn outside the plot area
))

title_text = ""
if texts.get('title'):
    title_text += f"<b>{texts['title']}</b>"
if texts.get('subtitle'):
    title_text += f"<br>{texts['subtitle']}"

annotations = []
if texts.get('source'):
    annotations.append(
        dict(
            text=texts['source'],
            showarrow=False,
            xref='paper',
            yref='paper',
            x=1,
            y=-0.1,  # Position below the x-axis title
            xanchor='right',
            yanchor='top',
            align='right'
        )
    )

fig.update_layout(
    title=dict(
        text=title_text,
        x=0.05,
        xanchor='left'
    ),
    xaxis=dict(
        title=texts.get('x_axis_title', ''),
        showgrid=True,
        gridcolor='#EAEAEA',
        griddash='dot',
        zeroline=False,
        showline=False,
        showticklabels=True
    ),
    yaxis=dict(
        title=texts.get('y_axis_title', ''),
        showline=False,
        showticklabels=True
    ),
    font=dict(
        family="Arial",
        size=12
    ),
    plot_bgcolor='white',
    paper_bgcolor='white',
    margin=dict(l=120, r=60, t=40, b=80),
    annotations=annotations,
    showlegend=False
)

# Dynamically adjust the x-axis range to prevent text label clipping
max_value = max(values)
fig.update_xaxes(range=[0, max_value * 1.18])

fig.write_image(str(output_image_path), scale=2)