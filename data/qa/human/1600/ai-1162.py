import sys
import json
import pathlib
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print("Usage: python <script_name>.py <json_file_path>")
    sys.exit(1)

json_file_path = pathlib.Path(sys.argv[1])
if not json_file_path.is_file():
    print(f"Error: JSON file not found at '{json_file_path}'")
    sys.exit(1)

with open(json_file_path, 'r', encoding='utf-8') as f:
    chart_data = json.load(f)

fig = go.Figure()

# --- Add Traces ---
for i, series in enumerate(chart_data['chart_data']['series']):
    fig.add_trace(go.Scatter(
        x=chart_data['chart_data']['categories'],
        y=series['y'],
        name=series['name'],
        mode='lines+markers',
        line=dict(color=chart_data['colors'][i], width=2),
        marker=dict(color=chart_data['colors'][i], size=5),
        connectgaps=False
    ))

# --- Add Series Labels as Annotations ---
for i, series in enumerate(chart_data['chart_data']['series']):
    # Find the last valid data point to place the label
    last_idx = -1
    for j in range(len(series['y']) - 1, -1, -1):
        if series['y'][j] is not None:
            last_idx = j
            break
    
    if last_idx != -1:
        fig.add_annotation(
            x=chart_data['chart_data']['categories'][last_idx],
            y=series['y'][last_idx],
            text=f"  {series['name']}",
            showarrow=False,
            xanchor='left',
            yanchor='middle',
            font=dict(
                family="Arial",
                size=14,
                color=chart_data['colors'][i]
            )
        )

# --- Define Texts ---
texts = chart_data['texts']
title_text = f"<b>{texts['title']}</b><br><span style='font-size: 15px; color:#555555;'>{texts['subtitle']}</span>"

# --- Update Layout ---
fig.update_layout(
    width=1000,
    height=650,
    plot_bgcolor='white',
    paper_bgcolor='white',
    showlegend=False,
    font=dict(
        family="Arial",
        size=12,
        color='#333333'
    ),
    title=dict(
        text=title_text,
        y=0.96,
        x=0.01,
        xanchor='left',
        yanchor='top',
        font=dict(size=22)
    ),
    xaxis=dict(
        showgrid=False,
        showline=False,
        tickmode='array',
        tickvals=[1991, 1995, 2000, 2005, 2011],
        tickfont=dict(size=14),
        range=[1990.5, 2012.5] # Add padding for labels
    ),
    yaxis=dict(
        showgrid=True,
        gridcolor='#E8E8E8',
        griddash='dash',
        zeroline=False,
        showline=False,
        tickmode='array',
        tickvals=[0, 0.5, 1, 1.5],
        ticktext=['0 kg', '0.5 kg', '1 kg', '1.5 kg'],
        tickfont=dict(size=14),
        range=[0, 1.9]
    ),
    margin=dict(l=60, r=120, t=120, b=80),
)

# --- Add Source and Note Annotations ---
fig.add_annotation(
    text=texts['source'],
    xref="paper", yref="paper",
    x=0, y=-0.12,
    xanchor='left', yanchor='top',
    showarrow=False,
    font=dict(size=12, color='#7f7f7f')
)

fig.add_annotation(
    text=texts['note'],
    xref="paper", yref="paper",
    x=1, y=-0.12,
    xanchor='right', yanchor='top',
    showarrow=False,
    font=dict(size=12, color='#7f7f7f')
)

# --- Output ---
output_filename = f"{json_file_path.stem}.png"
fig.write_image(output_filename, scale=2)
print(f"Chart saved to {output_filename}")