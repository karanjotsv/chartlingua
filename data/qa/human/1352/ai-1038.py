import sys
import json
import plotly.graph_objects as go
import os

if len(sys.argv) != 2:
    print("Usage: python script.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]

try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_details = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_path}")
    sys.exit(1)

data = chart_details['chart_data']
categories = chart_details['categories']
texts = chart_details['texts']
colors = chart_details['colors']

fig = go.Figure()

y_axis_categories = categories[::-1]

for i, series in enumerate(data):
    x_values = series['values'][::-1]
    
    if i == 0:
        text_labels = [f"<b>{v}%</b>" for v in x_values]
    else:
        text_labels = [f"<b>{v}</b>" for v in x_values]

    fig.add_trace(go.Bar(
        name=series['name'],
        x=x_values,
        y=y_axis_categories,
        orientation='h',
        marker=dict(color=colors[i], line=dict(width=0)),
        text=text_labels,
        textposition='inside',
        insidetextanchor='middle',
        textfont=dict(color='white', family='Arial')
    ))

full_source_text = f"{texts['source']}<br><br><b>{texts['logo']}</b>"

fig.update_layout(
    barmode='stack',
    title=dict(
        text=f"<b>{texts['title']}</b>",
        font=dict(family="Arial", size=18),
        x=0.01,
        xanchor='left'
    ),
    xaxis=dict(
        showgrid=False,
        zeroline=False,
        showticklabels=False,
        range=[0, 100],
        visible=False
    ),
    yaxis=dict(
        showline=False,
        showgrid=False,
        ticks='',
        tickfont=dict(family="Arial", size=12)
    ),
    legend=dict(
        orientation='h',
        yanchor='bottom',
        y=1.01,
        xanchor='left',
        x=0.22,
        traceorder='normal',
        font=dict(family="Arial", size=12),
        bgcolor='rgba(0,0,0,0)'
    ),
    plot_bgcolor='white',
    paper_bgcolor='white',
    margin=dict(l=160, r=20, t=100, b=140),
    annotations=[
        dict(
            text=full_source_text,
            showarrow=False,
            xref='paper',
            yref='paper',
            x=0,
            y=-0.15,
            xanchor='left',
            yanchor='top',
            align='left',
            font=dict(family="Arial", size=11)
        )
    ]
)

base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_filename}.png"
fig.write_image(output_filename, scale=2)

print(f"Chart saved as {output_filename}")