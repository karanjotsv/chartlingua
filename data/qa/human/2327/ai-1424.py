import sys
import json
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print("Usage: python create_chart.py <json_file_path>")
    sys.exit(1)

json_file_path = sys.argv[1]

try:
    with open(json_file_path, 'r', encoding='utf-8') as f:
        config = json.load(f)
except FileNotFoundError:
    print(f"Error: File not found at {json_file_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Invalid JSON format in {json_file_path}")
    sys.exit(1)

chart_data = config['chart_data']
texts = config['texts']
colors = config['colors']

chart_data.reverse()

categories = [d['category'] for d in chart_data]
num_series = len(texts['legend_labels'])

fig = go.Figure()

for i in range(num_series):
    values = [d['values'][i] for d in chart_data]
    fig.add_trace(go.Bar(
        y=categories,
        x=values,
        name=texts['legend_labels'][i],
        orientation='h',
        marker=dict(
            color=colors[i],
            line=dict(color='white', width=1)
        ),
        text=[f"{v}%" for v in values if v > 0],
        textposition='inside',
        insidetextanchor='middle',
        textfont=dict(
            family='Arial',
            size=12,
            color='white'
        ),
        hoverinfo='skip'
    ))

title_text = ""
if texts.get('title'):
    title_text += f"<b>{texts['title']}</b>"
if texts.get('subtitle'):
    title_text += f"<br><sub>{texts['subtitle']}</sub>"

fig.update_layout(
    barmode='stack',
    title=dict(
        text=title_text,
        x=0.01,
        xanchor='left'
    ),
    xaxis=dict(
        title=texts.get('x_axis_title'),
        showgrid=True,
        gridcolor='#e0e0e0',
        zeroline=False,
        ticks='outside',
        tickvals=[0, 20, 40, 60, 80, 100, 120],
        ticktext=['0%', '20%', '40%', '60%', '80%', '100%', '120%'],
        range=[0, 120]
    ),
    yaxis=dict(
        showgrid=False,
        zeroline=False,
        ticks='',
        showticklabels=True
    ),
    legend=dict(
        orientation='h',
        yanchor='bottom',
        y=-0.2,
        xanchor='center',
        x=0.5,
        traceorder='normal',
        font=dict(size=12)
    ),
    font=dict(
        family="Arial",
        size=12
    ),
    plot_bgcolor='white',
    paper_bgcolor='white',
    margin=dict(l=250, r=40, t=50, b=120),
    height=800
)

fig.add_annotation(
    text=texts.get('source', ''),
    align='right',
    showarrow=False,
    xref='paper',
    yref='paper',
    x=1.0,
    y=-0.25,
    xanchor='right',
    yanchor='top',
    font=dict(
        family="Arial",
        size=10,
        color="grey"
    )
)

base_name_with_ext = json_file_path.split('/')[-1].split('\\')[-1]
base_filename = base_name_with_ext.rsplit('.', 1)[0]
output_filename = f"{base_filename}.png"

fig.write_image(output_filename, scale=2)
print(f"Chart successfully generated and saved as {output_filename}")