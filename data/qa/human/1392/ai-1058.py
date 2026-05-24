import sys
import json
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print("Usage: python script.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]

try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_data_json = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_path}")
    sys.exit(1)

chart_data = chart_data_json['chart_data']
texts = chart_data_json['texts']
colors = chart_data_json['colors']

fig = go.Figure()

for i, series in enumerate(chart_data):
    fig.add_trace(go.Scatter(
        x=series['x'],
        y=series['y'],
        name=series['name'],
        mode='lines+markers+text',
        line=dict(color=colors[i], width=2),
        marker=dict(color=colors[i], size=8, symbol='circle'),
        text=series['y'],
        textposition=series['textposition'],
        textfont=dict(family="Arial", size=11, color='black'),
        hoverinfo='none'
    ))

# Create custom legend using annotations
legend_y_start = 0.8
for i, label in enumerate(texts['legend_labels']):
    fig.add_annotation(
        xref="paper", yref="paper",
        x=0.8, y=legend_y_start - (i * 0.1),
        text=f"<span style='color: {colors[i]}; font-size: 20px;'>●</span> {label}",
        showarrow=False,
        align='left',
        xanchor='left',
        yanchor='middle',
        font=dict(family="Arial", size=12)
    )

# Add source annotation
fig.add_annotation(
    xref="paper", yref="paper",
    x=0, y=-0.15,
    text=texts['source'],
    showarrow=False,
    align='left',
    xanchor='left',
    yanchor='top',
    font=dict(family="Arial", size=11)
)

title_text = f"<b>{texts['title']}</b><br><span style='color:#505050; font-size:0.9em;'>{texts['subtitle']}</span>"

fig.update_layout(
    title=dict(
        text=title_text,
        y=0.95,
        x=0.01,
        xanchor='left',
        yanchor='top'
    ),
    xaxis=dict(
        title_text=texts['x_axis_title'],
        tickvals=[2002, 2004, 2006, 2008, 2010, 2012, 2014, 2017],
        showgrid=False,
        zeroline=False,
        linecolor='black',
        ticks='outside',
    ),
    yaxis=dict(
        title_text=texts['y_axis_title'],
        range=[0, 105],
        tickvals=[0, 100],
        ticktext=['0', '100%'],
        showgrid=True,
        gridcolor='#e0e0e0',
        zeroline=False,
        linecolor='black',
        ticks='outside',
    ),
    font=dict(family="Arial", size=12, color="black"),
    plot_bgcolor='white',
    paper_bgcolor='white',
    showlegend=False,
    margin=dict(l=40, r=40, t=120, b=100)
)

output_filename = json_path.rsplit('.', 1)[0] + '.png'
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")