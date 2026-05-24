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

labels = [item['label'] for item in data]
values = [item['value'] for item in data]

fig = go.Figure()

fig.add_trace(go.Pie(
    labels=labels,
    values=values,
    marker=dict(colors=colors, line=dict(color='#FFFFFF', width=1)),
    hoverinfo='label+percent',
    textinfo='none',  # The original uses outside labels, not text on slices
    sort=False,
    direction='clockwise'
))

annotations = []
if texts.get('source'):
    annotations.append(
        dict(
            text=texts['source'],
            align='right',
            showarrow=False,
            xref='paper',
            yref='paper',
            x=1,
            y=0,
            xanchor='right',
            yanchor='bottom',
            font=dict(family="Arial", size=10, color="#666666")
        )
    )

fig.update_layout(
    showlegend=True,
    legend=dict(
        orientation="v",
        yanchor="middle",
        y=0.5,
        xanchor="left",
        x=1.05,
        font=dict(family="Arial", size=12),
        bgcolor='rgba(0,0,0,0)'
    ),
    font=dict(family="Arial", size=14),
    margin=dict(l=40, r=200, t=40, b=50),
    paper_bgcolor='white',
    plot_bgcolor='white',
    annotations=annotations
)

# Recreate the label format from the image in the legend
# The original image format is "Label Value%"
for i, trace in enumerate(fig.data):
    if trace.type == 'pie':
        # Custom legend labels
        trace.legendgroup = 'group' # To make them appear as one legend
        new_labels = [f"{label} {value}%" for label, value in zip(labels, values)]
        fig.data[i].name = "" # Hack to not show trace name in legend
        fig.data[i].showlegend = True
        fig.data[i].customdata = new_labels
        fig.data[i].legendgrouptitle = dict(text='')
        trace.hovertemplate = '%{label}<br>%{percent}<extra></extra>' # Cleaner hover
        
# A bit of a workaround to assign custom text to legend items
# We create dummy invisible traces for the legend
for i in range(len(labels)):
    fig.add_trace(go.Scatter(
        x=[None], y=[None],
        mode='markers',
        marker=dict(color=colors[i], size=10),
        name=f"{labels[i]} {values[i]}%",
        showlegend=True
    ))

# Hide the original pie chart legend
fig.data[0].showlegend = False


base_filename = os.path.splitext(json_path)[0]
output_filename = f"{base_filename}.png"

fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")