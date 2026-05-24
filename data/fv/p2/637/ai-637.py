import sys
import json
import pathlib
import plotly.graph_objects as go

# Check for command-line argument
if len(sys.argv) != 2:
    print("Usage: python <script_name>.py <path_to_json_file>")
    sys.exit(1)

# Get file path from command-line argument
json_path = pathlib.Path(sys.argv[1])
if not json_path.is_file():
    print(f"Error: File not found at {json_path}")
    sys.exit(1)

# Derive output filename from JSON path
output_filename = json_path.stem + ".png"

# Load data from JSON
with open(json_path, 'r', encoding='utf-8') as f:
    chart_info = json.load(f)

data = chart_info["chart_data"]
texts = chart_info["texts"]
colors = chart_info["colors"]

fig = go.Figure()

# --- Section Headers ---
header_positions = {
    "population":      (0.06, 0.28, 0.9, 0.94),
    "median_age":      (0.32, 0.54, 0.9, 0.94),
    "crime":           (0.58, 0.80, 0.9, 0.94),
    "economic_output": (0.06, 0.28, 0.61, 0.65),
    "unemployment":    (0.06, 0.28, 0.32, 0.36),
    "life_expectancy": (0.32, 0.54, 0.32, 0.36),
    "traffic":         (0.58, 0.86, 0.32, 0.36)
}

for section, (x0, x1, y0, y1) in header_positions.items():
    fig.add_shape(type="rect", xref="paper", yref="paper",
                  x0=x0, y0=y0, x1=x1, y1=y1,
                  fillcolor=colors["section_headers"][section], line_width=0)
    fig.add_shape(type="path", xref="paper", yref="paper",
                  path=f"M {(x0+x1)/2 - 0.015},{y0} L {(x0+x1)/2},{y0 - 0.02} L {(x0+x1)/2 + 0.015},{y0} Z",
                  fillcolor=colors["section_headers"][section], line_width=0)
    fig.add_annotation(xref="paper", yref="paper",
                       x=(x0 + x1) / 2, y=(y0 + y1) / 2,
                       text=f"<b>{texts['sections'][section]}</b>",
                       showarrow=False, font=dict(color="white", size=13, family="Arial"))


# --- Population Donut ---
fig.add_trace(go.Pie(
    labels=data["population"]["labels"],
    values=data["population"]["values"],
    hole=0.7,
    marker_colors=colors["population_donut"],
    domain={'x': [0.05, 0.29], 'y': [0.71, 0.89]},
    textinfo='none',
    hoverinfo='none',
    sort=False
))
fig.add_annotation(xref="paper", yref="paper", x=0.17, y=0.8,
                   text=texts["population"]["center_text"],
                   showarrow=False, font=dict(size=22, family="Arial", color=colors["text_main"]))
fig.add_annotation(xref="paper", yref="paper", x=0.17, y=0.7,
                   text=f"<b>{texts['population']['value_text']}</b>",
                   showarrow=False, font=dict(size=14, family="Arial", color=colors["text_main"]))
fig.add_annotation(xref="paper", yref="paper", x=0.17, y=0.67,
                   text=texts["population"]["date_text"],
                   showarrow=False, font=dict(size=11, family="Arial", color="grey"))

# --- Economic Output Donut ---
fig.add_trace(go.Pie(
    labels=data["economic_output"]["labels"],
    values=data["economic_output"]["values"],
    hole=0.7,
    marker_colors=colors["economic_donut"],
    domain={'x': [0.05, 0.29], 'y': [0.42, 0.60]},
    textinfo='none',
    hoverinfo='none',
    sort=False
))
fig.add_annotation(xref="paper", yref="paper", x=0.17, y=0.51,
                   text=texts["economic_output"]["center_text"],
                   showarrow=False, font=dict(size=22, family="Arial", color=colors["text_main"]))
fig.add_annotation(xref="paper", yref="paper", x=0.17, y=0.41,
                   text=f"<b>{texts['economic_output']['value_text']}</b>",
                   showarrow=False, font=dict(size=14, family="Arial", color=colors["text_main"]))
fig.add_annotation(xref="paper", yref="paper", x=0.17, y=0.38,
                   text=texts["economic_output"]["date_text"],
                   showarrow=False, font=dict(size=11, family="Arial", color="grey"))

# --- Median Age ---
y_pos = 0.85
for item in data["median_age"]:
    color = colors["text_highlights"]["median_age"] if item["region"] == "West Midlands" else colors["text_main"]
    fig.add_annotation(xref="paper", yref="paper", x=0.32, y=y_pos,
                       text=item["region"], align='left',
                       showarrow=False, font=dict(size=13, family="Arial", color=color))
    fig.add_annotation(xref="paper", yref="paper", x=0.44, y=y_pos,
                       text=f"<b>{item['age']:.1f}</b>", align='right',
                       showarrow=False, font=dict(size=26, family="Arial", color=color))
    fig.add_annotation(xref="paper", yref="paper", x=0.52, y=y_pos-0.005,
                       text=texts["median_age"]["unit"], align='right',
                       showarrow=False, font=dict(size=12, family="Arial", color=color))
    y_pos -= 0.06
fig.add_annotation(xref="paper", yref="paper", x=0.43, y=y_pos-0.01,
                   text=texts["median_age"]["date_text"],
                   showarrow=False, font=dict(size=11, family="Arial", color="grey"))


# --- Crime Bars ---
fig.add_trace(go.Bar(
    y=[d["region"] for d in data["crime"]],
    x=[d["rate"] for d in data["crime"]],
    orientation='h',
    marker_color=colors["crime_bars"],
    text=[f"<b>{d['rate']}</b>" for d in data["crime"]],
    textposition="inside",
    textfont=dict(color="white", size=24, family="Arial"),
    width=0.5,
    insidetextanchor='middle',
    hoverinfo='none'
))
fig.add_annotation(xref="paper", yref="paper", x=0.69, y=0.68,
                   text=texts["crime"]["subtitle"], align="center",
                   showarrow=False, font=dict(size=10, family="Arial", color="grey"))
fig.add_annotation(xref="paper", yref="paper", x=0.69, y=0.64,
                   text=texts["crime"]["note"], align="center",
                   showarrow=False, font=dict(size=10, family="Arial", color="grey"))


# --- Unemployment Bars ---
unemployment_colors = [colors["unemployment_bars"]["highlight"] if d["region"] == "East" else colors["unemployment_bars"]["default"] for d in data["unemployment"]]
fig.add_trace(go.Bar(
    x=[d["region"] for d in data["unemployment"]],
    y=[d["rate"] for d in data["unemployment"]],
    marker_color=unemployment_colors,
    text=[f"{d['rate']}%" for d in data["unemployment"]],
    textposition="outside",
    textfont=dict(family="Arial", size=12, color=colors["text_main"]),
    hoverinfo='none',
    xaxis='x2',
    yaxis='y2'
))
fig.add_annotation(xref="paper", yref="paper", x=0.17, y=0.1,
                   text=texts["unemployment"]["date_text"],
                   showarrow=False, font=dict(size=11, family="Arial", color="grey"))

# --- Life Expectancy ---
le_data = data["life_expectancy"]
y_pos = 0.27
fig.add_annotation(xref="paper", yref="paper", x=0.43, y=y_pos,
                   text=f"<b><span style='color:{colors['text_highlights']['life_expectancy']}'>{texts['life_expectancy']['east_of_england']}</span></b>",
                   showarrow=False, font=dict(size=14, family="Arial"))
fig.add_annotation(xref="paper", yref="paper", x=0.36, y=y_pos - 0.04,
                   text=f"<b>{le_data['east_of_england']['male']:.1f}</b><br>{texts['life_expectancy']['unit']}",
                   showarrow=False, font=dict(size=16, family="Arial", color=colors['text_main']))
fig.add_annotation(xref="paper", yref="paper", x=0.50, y=y_pos - 0.04,
                   text=f"<b>{le_data['east_of_england']['female']:.1f}</b><br>{texts['life_expectancy']['unit']}",
                   showarrow=False, font=dict(size=16, family="Arial", color=colors['text_main']))
fig.add_annotation(xref="paper", yref="paper", x=0.37, y=y_pos - 0.035, text="🧍", showarrow=False, font=dict(size=30, color=colors['text_highlights']['life_expectancy']))
fig.add_annotation(xref="paper", yref="paper", x=0.51, y=y_pos - 0.035, text="🧍‍♀️", showarrow=False, font=dict(size=30, color=colors['text_highlights']['life_expectancy']))

y_pos = 0.18
fig.add_annotation(xref="paper", yref="paper", x=0.43, y=y_pos,
                   text=f"<b>{texts['life_expectancy']['south_east']}</b>",
                   showarrow=False, font=dict(size=14, family="Arial", color=colors['text_main']))
fig.add_annotation(xref="paper", yref="paper", x=0.36, y=y_pos - 0.04,
                   text=f"<b>{le_data['south_east']['male']:.1f}</b><br>{texts['life_expectancy']['unit']}",
                   showarrow=False, font=dict(size=16, family="Arial", color=colors['text_main']))
fig.add_annotation(xref="paper", yref="paper", x=0.50, y=y_pos - 0.04,
                   text=f"<b>{le_data['south_east']['female']:.1f}</b><br>{texts['life_expectancy']['unit']}",
                   showarrow=False, font=dict(size=16, family="Arial", color=colors['text_main']))
fig.add_annotation(xref="paper", yref="paper", x=0.37, y=y_pos - 0.035, text="🧍", showarrow=False, font=dict(size=30, color=colors['text_highlights']['life_expectancy']))
fig.add_annotation(xref="paper", yref="paper", x=0.51, y=y_pos - 0.035, text="🧍‍♀️", showarrow=False, font=dict(size=30, color=colors['text_highlights']['life_expectancy']))

fig.add_annotation(xref="paper", yref="paper", x=0.43, y=0.09,
                   text=texts["life_expectancy"]["date_text"],
                   showarrow=False, font=dict(size=11, family="Arial", color="grey"))

# --- Traffic Bars ---
fig.add_trace(go.Bar(
    y=[d["region"] for d in data["traffic"]],
    x=[d["change"] for d in data["traffic"]],
    orientation='h',
    marker_color=colors["traffic_bars"],
    text=[f"{d['change']}%" for d in data["traffic"]],
    textposition="outside",
    textfont=dict(family="Arial", size=12, color=colors["text_main"]),
    hoverinfo='none',
    xaxis='x3',
    yaxis='y3'
))
fig.add_annotation(xref="paper", yref="paper", x=0.72, y=0.1,
                   text=texts["traffic"]["date_text"],
                   showarrow=False, font=dict(size=11, family="Arial", color="grey"))

# --- Map ---
fig.add_shape(type="rect", xref="paper", yref="paper",
              x0=0.32, y0=0.38, x1=0.86, y1=0.6,
              fillcolor=colors["map_background"], line_width=0, layer="below")
fig.add_trace(go.Scatter(
    x=[c['x'] for c in data['map_cities']],
    y=[c['y'] for c in data['map_cities']],
    mode='markers+text',
    marker=dict(color=colors['map_cities'], size=8),
    text=[c['name'] for c in data['map_cities']],
    textposition='top right',
    textfont=dict(family="Arial", size=10, color=colors['map_cities']),
    hoverinfo='none',
    xaxis='x4',
    yaxis='y4'
))

# --- Layout ---
fig.update_layout(
    title=dict(
        text=f"<b>{texts['title']}</b>",
        y=0.98, x=0.02,
        xanchor='left', yanchor='top',
        font=dict(size=24, family="Arial", color=colors["text_main"])
    ),
    plot_bgcolor=colors["background"],
    paper_bgcolor=colors["background"],
    width=800,
    height=1100,
    showlegend=False,
    margin=dict(l=20, r=20, t=40, b=100),

    # Crime bar chart axes
    yaxis=dict(domain=[0.73, 0.87], showticklabels=True, autorange="reversed", tickfont=dict(family="Arial", size=12)),
    xaxis=dict(domain=[0.58, 0.85], showgrid=False, zeroline=False, showticklabels=False),

    # Unemployment bar chart axes
    xaxis2=dict(domain=[0.06, 0.28], anchor='y2', showticklabels=True, tickfont=dict(family="Arial", size=10)),
    yaxis2=dict(domain=[0.14, 0.30], anchor='x2', range=[0, 11], showgrid=False, zeroline=False, showticklabels=False),
    
    # Traffic bar chart axes
    xaxis3=dict(domain=[0.58, 0.86], anchor='y3', range=[-10, 10], zeroline=True, zerolinecolor='grey', zerolinewidth=1, showgrid=False, showticklabels=False),
    yaxis3=dict(domain=[0.14, 0.30], anchor='x3', autorange="reversed", showticklabels=True, tickfont=dict(family="Arial", size=12)),

    # Map axes
    xaxis4=dict(domain=[0.32, 0.86], anchor='y4', range=[0.3, 0.9], visible=False),
    yaxis4=dict(domain=[0.38, 0.67], anchor='x4', range=[0.3, 0.7], visible=False),

    annotations=[
        dict(
            xref="paper", yref="paper",
            x=0.02, y=0.01,
            xanchor='left', yanchor='bottom',
            text=texts["source"],
            showarrow=False,
            align='left',
            font=dict(size=11, family="Arial", color=colors["text_main"])
        )
    ]
)

# --- Final Output ---
fig.write_image(output_filename, scale=2)
print(f"Chart saved to {output_filename}")