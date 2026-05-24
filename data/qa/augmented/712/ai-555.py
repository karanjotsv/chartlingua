import sys
import json
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print("Usage: python <script_name>.py <json_file_path>")
    sys.exit(1)

json_file_path = sys.argv[1]

try:
    with open(json_file_path, 'r', encoding='utf-8') as f:
        chart_info = json.load(f)
except FileNotFoundError:
    print(f"Error: File not found at {json_file_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print("Error: Invalid JSON format.")
    sys.exit(1)

data = chart_info['chart_data']
texts = chart_info['texts']
colors = chart_info['colors']

fig = go.Figure()

for i, series in enumerate(data):
    fig.add_trace(go.Bar(
        x=series['x'],
        y=series['y'],
        name=series['name'],
        marker_color=colors[i],
        text=series['y'],
        textposition='inside',
        insidetextanchor='middle',
        textfont=dict(
            family="Arial",
            size=12,
            color='white'
        ),
        hoverinfo='skip'
    ))

source_text_parts = []
if texts.get("source"):
    source_text_parts.append(texts["source"])
if texts.get("note"):
    source_text_parts.append(texts["note"])
source_text = "<br>".join(source_text_parts)

fig.update_layout(
    barmode='stack',
    plot_bgcolor='white',
    font=dict(family="Arial", size=12),
    margin=dict(l=80, r=40, t=40, b=150),
    yaxis=dict(
        title=texts.get('y_axis_title'),
        range=[0, 2],
        tickvals=[0, 0.5, 1, 1.5, 2],
        gridcolor='#e0e0e0',
        zeroline=False
    ),
    xaxis=dict(
        title=texts.get('x_axis_title'),
        tickangle=-45,
        type='category'
    ),
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=-0.45,
        xanchor="center",
        x=0.5
    ),
    showlegend=True
)

if source_text:
    fig.add_annotation(
        text=source_text,
        xref="paper", yref="paper",
        x=1, y=-0.45,
        showarrow=False,
        align="right",
        xanchor="right",
        yanchor="bottom",
        font=dict(size=10, color="#808080")
    )

base_filename = json_file_path.split('/')[-1].rsplit('.', 1)[0]
output_filename = f"{base_filename}.png"

fig.write_image(output_filename, scale=2)
print(f"Chart saved as {output_filename}")