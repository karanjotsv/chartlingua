import sys
import json
import plotly.graph_objects as go

# Ensure a JSON file path is provided as a command-line argument
if len(sys.argv) != 2:
    print(f"Usage: python {sys.argv[0].split('/')[-1]} <json_file_path>")
    sys.exit(1)

json_file_path = sys.argv[1]

# Load chart data and configuration from the specified JSON file
with open(json_file_path, 'r', encoding='utf-8') as f:
    config = json.load(f)

chart_data = config['chart_data']
texts = config['texts']
colors = config['colors']

# Initialize a new figure
fig = go.Figure()

# Add a bar trace for each data series defined in the JSON
for i, series in enumerate(chart_data):
    fig.add_trace(go.Bar(
        name=series['name'],
        x=series['x'],
        y=series['y'],
        marker_color=colors[i],
        text=[f"{val}%" for val in series['y']],
        textposition='outside',
        cliponaxis=False,
        textfont=dict(family="Arial", size=12, color='black')
    ))

# Combine title and subtitle using HTML for rich text formatting
title_text = ""
if texts.get("title"):
    title_text += f'<b>{texts["title"]}</b>'
if texts.get("subtitle"):
    title_text += f'<br><sub>{texts["subtitle"]}</sub>'

# Combine source and note
source_text_parts = []
if texts.get("source"):
    source_text_parts.append(texts.get("source"))
if texts.get("note"):
    source_text_parts.append(texts.get("note"))
source_text = "<br>".join(source_text_parts)

# Update the layout of the chart for a professional and clean appearance
fig.update_layout(
    barmode='group',
    plot_bgcolor='#FFFFFF',
    paper_bgcolor='#FFFFFF',
    font=dict(family="Arial", size=12, color='black'),
    title={
        'text': title_text,
        'y': 0.95, 'x': 0.5,
        'xanchor': 'center', 'yanchor': 'top'
    },
    xaxis=dict(
        title_text=texts.get('x_axis_title'),
        showgrid=False,
        showline=True,
        linecolor='black',
        zeroline=False,
        tickfont=dict(size=12)
    ),
    yaxis=dict(
        title_text=texts.get('y_axis_title'),
        range=[0, 50],
        tickvals=[0, 10, 20, 30, 40, 50],
        ticktext=["0%", "10%", "20%", "30%", "40%", "50%"],
        showgrid=True,
        gridcolor='#E0E0E0',
        showline=False,
        zeroline=False
    ),
    legend=dict(
        orientation="h",
        yanchor="bottom", y=-0.25,
        xanchor="center", x=0.5
    ),
    margin=dict(l=80, r=40, b=120, t=60),
    annotations=[
        dict(
            text=source_text,
            showarrow=False,
            xref="paper", yref="paper",
            x=1.0, y=-0.32,
            xanchor='right', yanchor='bottom',
            align="right",
            font=dict(size=10, color='#666666')
        )
    ]
)

# Add faint vertical lines to separate the category groups, mimicking the original style
shapes = []
if len(chart_data) > 0 and 'x' in chart_data[0] and len(chart_data[0]['x']) > 1:
    x_categories = chart_data[0]['x']
    for i in range(len(x_categories) - 1):
        shapes.append(
            go.layout.Shape(
                type="line",
                xref="x", yref="paper",
                x0=i + 0.5, y0=0, x1=i + 0.5, y1=1,
                line=dict(color="#F0F0F0", width=2)
            )
        )
fig.update_layout(shapes=shapes)


# Determine the output filename from the input JSON path
base_filename = json_file_path.split('/')[-1].replace('.json', '')
output_filename = f"{base_filename}.png"

# Save the figure to a high-resolution PNG file
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")