import sys
import json
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print("Usage: python create_chart.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]

try:
    with open(json_path, 'r', encoding='utf-8') as f:
        config = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)

chart_data = config['chart_data']
texts = config['texts']
colors = config['colors']

# Data is read top-to-bottom, but Plotly plots y-axis bottom-to-top. Reverse it.
chart_data.reverse()

categories = [item['category'] for item in chart_data]
num_series = len(texts['series_names'])

series_values = []
series_labels = []
for i in range(num_series):
    series_values.append([item['values'][i] for item in chart_data])
    series_labels.append([item['labels'][i] for item in chart_data])

fig = go.Figure()

for i in range(num_series):
    fig.add_trace(go.Bar(
        y=categories,
        x=series_values[i],
        name=texts['series_names'][i],
        orientation='h',
        marker_color=colors[i],
        text=series_labels[i],
        textposition='outside',
        textfont=dict(family="Arial", size=14, color='black'),
        cliponaxis=False
    ))

combined_title = f"<b>{texts['title']}</b><br>{texts['subtitle']}"

fig.update_layout(
    barmode='group',
    plot_bgcolor='white',
    paper_bgcolor='white',
    font=dict(family="Arial", size=14),
    margin=dict(l=180, r=50, t=140, b=120),
    title=dict(
        text=combined_title,
        x=0.01,
        y=0.98,
        xanchor='left',
        yanchor='top',
        font=dict(family="Arial", size=20, color='black')
    ),
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="left",
        x=0.25,
        bgcolor='rgba(0,0,0,0)',
        bordercolor='rgba(0,0,0,0)',
        font=dict(size=14)
    ),
    xaxis=dict(
        visible=False,
        range=[0, max(max(v) for v in series_values) * 1.18]
    ),
    yaxis=dict(
        showline=False,
        showgrid=False,
        ticks=''
    ),
    annotations=[
        dict(
            text=texts['source'],
            showarrow=False,
            xref="paper",
            yref="paper",
            x=0,
            y=0,
            xanchor='left',
            yanchor='top',
            align='left',
            font=dict(family="Arial", size=12, color='#666666')
        )
    ],
    bargap=0.2,
    bargroupgap=0.1
)

base_filename = json_path.split('/')[-1].rsplit('.', 1)[0]
output_filename = f"{base_filename}.png"

fig.write_image(output_filename, scale=2)

print(f"Chart saved as {output_filename}")