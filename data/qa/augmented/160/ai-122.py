import sys
import json
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print("Usage: python <script_name>.py <json_file_path>")
    sys.exit(1)

json_path = sys.argv[1]

try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_info = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_path}")
    sys.exit(1)

chart_data = chart_info['chart_data']
texts = chart_info['texts']
colors = chart_info['colors']

categories = [d['category'] for d in chart_data]
legend_labels = texts['legend_labels']

fig = go.Figure()

for i in range(len(legend_labels)):
    values = [d['values'][i] for d in chart_data]
    fig.add_trace(go.Bar(
        name=legend_labels[i],
        x=categories,
        y=values,
        marker_color=colors[i],
        text=values,
        textposition='outside',
        texttemplate='%{text}',
        textfont=dict(family='Arial', size=12, color='black'),
        cliponaxis=False
    ))

fig.update_layout(
    barmode='group',
    plot_bgcolor='white',
    font=dict(family="Arial", size=12, color="black"),
    margin=dict(l=80, r=40, t=50, b=120),
    yaxis=dict(
        title_text=texts.get('y_axis_title'),
        range=[0, 175000],
        gridcolor='#EAEAEA',
        zeroline=False,
        showline=False,
        ticks='outside',
        ticklen=5,
        tickcolor='lightgrey'
    ),
    xaxis=dict(
        title_text=texts.get('x_axis_title'),
        showline=True,
        linewidth=1,
        linecolor='black',
        ticks='outside',
        ticklen=5
    ),
    legend=dict(
        orientation='h',
        yanchor='bottom',
        y=-0.3,
        xanchor='center',
        x=0.5,
        traceorder='normal'
    )
)

if texts.get('source'):
    fig.add_annotation(
        text=texts['source'],
        align='right',
        showarrow=False,
        xref='paper',
        yref='paper',
        x=1.0,
        y=-0.4,
        xanchor='right',
        yanchor='bottom',
        font=dict(size=10, color='grey')
    )

base_filename = json_path.rsplit('.', 1)[0]
output_filename = f"{base_filename}.png"

fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")