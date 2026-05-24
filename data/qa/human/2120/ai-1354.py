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
        chart_data = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_path}")
    sys.exit(1)

data = chart_data['chart_data']
texts = chart_data['texts']
colors = chart_data['colors']
x_labels = chart_data['x_axis_labels']

fig = go.Figure()

for i, series in enumerate(data):
    fig.add_trace(go.Bar(
        x=x_labels,
        y=series['values'],
        name=series['name'],
        marker_color=colors[i],
        text=[f'{v}%' for v in series['values']],
        textposition='outside',
        cliponaxis=False,
        textfont=dict(family="Arial", size=12)
    ))

title_text = ""
if texts.get("title"):
    title_text += f'<span style="font-size: 24px;"><b>{texts["title"]}</b></span>'
if texts.get("subtitle"):
    title_text += f'<br><span style="font-size: 16px;">{texts["subtitle"]}</span>'

fig.update_layout(
    barmode='group',
    title=dict(text=title_text, x=0.05, xanchor='left'),
    xaxis=dict(
        title=texts['x_axis_title'],
        tickvals=x_labels,
        ticktext=[str(label) for label in x_labels],
        showgrid=False,
        domain=[0.01, 0.99] # Add a small padding
    ),
    yaxis=dict(
        title=texts['y_axis_title'],
        range=[0, 31],
        ticksuffix='%',
        gridcolor='lightgray'
    ),
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=-0.3,
        xanchor="center",
        x=0.5
    ),
    font=dict(family="Arial"),
    plot_bgcolor='white',
    margin=dict(l=80, r=40, t=60, b=180),
    bargap=0.15,
    bargroupgap=0.1
)

for year_val in [x - 0.5 for x in x_labels[1:]]:
     fig.add_vline(x=year_val, line_width=1, line_dash="solid", line_color="lightgray")

if texts.get("source"):
    fig.add_annotation(
        text=texts['source'],
        xref="paper", yref="paper",
        x=0.99, y=-0.35,
        showarrow=False,
        xanchor="right", yanchor="bottom",
        font=dict(family="Arial", size=12, color="grey")
    )


base_filename = os.path.basename(json_path).rsplit('.', 1)[0]
output_filename = f"{base_filename}.png"

fig.write_image(output_filename, scale=2)
print(f"Chart saved to {output_filename}")