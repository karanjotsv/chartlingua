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
    print(f"Error: File not found at {json_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_path}")
    sys.exit(1)

chart_data = chart_info['chart_data']
texts = chart_info['texts']
colors = chart_info['colors']

fig = go.Figure()

for i, series in enumerate(chart_data['series']):
    fig.add_trace(go.Bar(
        name=series['name'],
        y=chart_data['categories'],
        x=series['values'],
        orientation='h',
        marker_color=colors[i],
        text=series['values'],
        textposition='inside',
        insidetextanchor='middle',
        texttemplate='<b>%{text}</b>',
        textfont=dict(color='white', size=14, family='Arial')
    ))

title_text = f"<b>{texts['title']}</b><br><span style='font-size:16px; color:#555555'>{texts['subtitle']}</span>"
footer_text = f"<span style='color:#555555'>{texts['source']}</span><br><b>{texts['footer']}</b>"

fig.update_layout(
    barmode='stack',
    title=dict(
        text=title_text,
        y=0.96,
        x=0.01,
        xanchor='left',
        yanchor='top',
        font=dict(size=24)
    ),
    xaxis=dict(
        visible=False,
        range=[0, 101]
    ),
    yaxis=dict(
        showgrid=False,
        ticks='',
        tickfont=dict(size=14)
    ),
    legend=dict(
        orientation='h',
        yanchor='bottom',
        y=1.01,
        xanchor='left',
        x=0.32,
        traceorder='normal',
        font=dict(size=14),
        bgcolor='rgba(0,0,0,0)'
    ),
    plot_bgcolor='white',
    paper_bgcolor='white',
    font=dict(family='Arial'),
    width=850,
    height=700,
    margin=dict(l=280, r=20, t=150, b=150),
    annotations=[
        dict(
            text=footer_text,
            showarrow=False,
            xref='paper',
            yref='paper',
            x=0,
            y=-0.22,
            xanchor='left',
            yanchor='top',
            align='left',
            font=dict(size=12)
        )
    ]
)

base_filename = json_path.split('/')[-1].replace('.json', '')
output_filename = f"{base_filename}.png"

fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")