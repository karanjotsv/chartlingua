import sys
import json
import pathlib
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <json_file_path>")
    sys.exit(1)

json_path = pathlib.Path(sys.argv[1])
if not json_path.is_file():
    print(f"Error: File not found at {json_path}")
    sys.exit(1)

with open(json_path, 'r', encoding='utf-8') as f:
    chart_data = json.load(f)

data = chart_data['chart_data']
texts = chart_data['texts']
colors = chart_data['colors']

labels = [item['category'] for item in data]
values = [item['value'] for item in data]

# Generate text labels for inside the pie slices
# Only show labels for slices >= 8% of the total
text_labels = []
for item in data:
    if item['value'] >= 8:
        category_text = item['category'].upper()
        if item['category'] == "South America":
            category_text = "SOUTH AMER-<br>ICA"
        text_labels.append(f"<b>{category_text} {item['value']}%</b>")
    else:
        text_labels.append('')

fig = go.Figure()

fig.add_trace(go.Pie(
    labels=labels,
    values=values,
    marker=dict(colors=colors, line=dict(color='#000000', width=1)),
    sort=False,
    direction='clockwise',
    rotation=108,
    text=text_labels,
    textposition='inside',
    insidetextorientation='horizontal',
    insidetextfont=dict(family='Arial', size=16, color='white'),
    hoverinfo='label+percent',
    showlegend=True
))

fig.update_layout(
    title=dict(
        text=f"<b>{texts['title']}</b>",
        x=0.5,
        xanchor='center',
        font=dict(family='Arial', size=24, color='#333333')
    ),
    legend=dict(
        traceorder='normal',
        font=dict(family='Arial', size=12, color='black'),
        bgcolor='rgba(255,255,255,0.5)',
        bordercolor='black',
        borderwidth=1
    ),
    font=dict(family="Arial"),
    paper_bgcolor='#D5E6EB',
    plot_bgcolor='#D5E6EB',
    margin=dict(l=60, r=60, t=120, b=100),
    annotations=[
        dict(
            text=texts['source'],
            showarrow=False,
            xref="paper", yref="paper",
            x=0, y=-0.1,
            xanchor='left', yanchor='top',
            font=dict(family='Arial', size=12, color='black')
        )
    ]
)

output_filename = json_path.stem + ".png"
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")