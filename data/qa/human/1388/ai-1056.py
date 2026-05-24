import sys
import json
import pathlib
import plotly.graph_objects as go

# --- 1. Load data from JSON file provided as a command-line argument ---
if len(sys.argv) != 2:
    print("Usage: python create_chart.py <path_to_json_file>")
    sys.exit(1)

json_path = pathlib.Path(sys.argv[1])
if not json_path.is_file():
    print(f"Error: File not found at {json_path}")
    sys.exit(1)

with open(json_path, 'r', encoding='utf-8') as f:
    chart_info = json.load(f)

chart_data = chart_info["chart_data"]
texts = chart_info["texts"]
colors = chart_info["colors"]

# --- 2. Prepare data and text positions ---
y_satisfied = chart_data[0]['y']
y_dissatisfied = chart_data[1]['y']

textpos_satisfied = []
textpos_dissatisfied = []

for ys, yd in zip(y_satisfied, y_dissatisfied):
    if ys > yd:
        textpos_satisfied.append('top center')
        textpos_dissatisfied.append('bottom center')
    else:
        textpos_satisfied.append('bottom center')
        textpos_dissatisfied.append('top center')

# --- 3. Create the figure and add traces ---
fig = go.Figure()

for i, series in enumerate(chart_data):
    textpositions = textpos_satisfied if series['name'] == 'Satisfied' else textpos_dissatisfied
    fig.add_trace(go.Scatter(
        x=series['x'],
        y=series['y'],
        name=series['name'],
        mode='lines+markers+text',
        line=dict(color=colors[i], width=3),
        marker=dict(
            color=colors[i],
            size=9,
            line=dict(color='white', width=1.5)
        ),
        text=[f'{val}' for val in series['y']],
        textposition=textpositions,
        textfont=dict(
            family="Arial",
            size=12,
            color=colors[i]
        ),
        hoverinfo='none',
        showlegend=False
    ))

# --- 4. Configure layout, title, axes, and annotations ---
fig.update_layout(
    plot_bgcolor='white',
    paper_bgcolor='white',
    font=dict(family="Arial", size=12, color='#333333'),
    margin=dict(l=40, r=40, t=140, b=100),
    title=dict(
        text=f"<span style='font-size: 22px;'>{texts['title']}</span>"
             f"<br><sup style='font-size:1em'></sup>"
             f"<br><span style='font-size: 15px; color: #555555;'>{texts['subtitle']}</span>",
        y=0.95,
        x=0.01,
        xanchor='left',
        yanchor='top'
    ),
    xaxis=dict(
        showline=False,
        showgrid=False,
        showticklabels=True,
        tickmode='array',
        tickvals=[2002, 2004, 2006, 2008, 2010, 2012, 2014, 2016, 2018],
        tickfont=dict(size=14),
        zeroline=False,
        range=[2001.5, 2018.5]
    ),
    yaxis=dict(
        showline=False,
        showgrid=False,
        showticklabels=True,
        range=[-5, 105],
        tickmode='array',
        tickvals=[0],
        ticktext=['0'],
        tickfont=dict(size=14),
        zeroline=False
    ),
    annotations=[
        # Source text
        dict(
            text=texts['source'],
            showarrow=False,
            xref='paper', yref='paper',
            x=0, y=-0.20,
            xanchor='left', yanchor='bottom',
            align='left',
            font=dict(size=12)
        ),
        # Y-axis top label
        dict(
            text="100 %",
            showarrow=False,
            xref='paper', yref='y',
            x=-0.04, y=100,
            xanchor='left', yanchor='middle',
            font=dict(size=14)
        ),
        # Legend-like labels
        dict(
            text="<b>Satisfied</b>",
            showarrow=False,
            xref='x', yref='y',
            x=2015, y=75,
            font=dict(size=14, color=colors[0])
        ),
        dict(
            text="<b>Dissatisfied</b>",
            showarrow=False,
            xref='x', yref='y',
            x=2015, y=20,
            font=dict(size=14, color=colors[1])
        ),
    ],
    shapes=[
        # Main title separator line
        dict(
            type='line',
            xref='paper', yref='paper',
            x0=0, x1=1,
            y0=0.84, y1=0.84,
            line=dict(color='black', width=2)
        ),
        # X-axis line
        dict(
            type='line',
            xref='paper', yref='y',
            x0=0, x1=1,
            y0=0, y1=0,
            line=dict(color='grey', width=1)
        )
    ]
)

# --- 5. Output the chart to a PNG file ---
output_filename = f"{json_path.stem}.png"
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")