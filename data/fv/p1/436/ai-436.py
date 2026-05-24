import sys
import json
import os
import plotly.graph_objects as go

# --- 1. Load Data ---
# The script must be called with the JSON file path as an argument
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <json_file_path>")
    sys.exit(1)

json_path = sys.argv[1]
if not os.path.exists(json_path):
    print(f"Error: JSON file not found at '{json_path}'")
    sys.exit(1)

with open(json_path, 'r', encoding='utf-8') as f:
    chart_info = json.load(f)

# Extract data from JSON
texts = chart_info.get("texts", {})
colors = chart_info.get("colors", {})
data = chart_info.get("chart_data", {})

# --- 2. Create Figure ---
fig = go.Figure()
fig.update_layout(
    font_family="Arial",
    width=850,
    height=1500,
    paper_bgcolor=colors.get("white"),
    plot_bgcolor=colors.get("background"),
    title=dict(
        text=texts.get("title"),
        y=0.97,
        x=0.5,
        xanchor='center',
        yanchor='top',
        font=dict(size=28, color=colors.get("text_primary"))
    ),
    showlegend=False,
    margin=dict(l=20, r=20, t=80, b=80),
    annotations=[],
    shapes=[]
)

# --- Helper function for section headers ---
def add_section_header(fig, x, y, width, text, color):
    # Rectangle
    fig.add_shape(type="rect",
        x0=x - width/2, y0=y, x1=x + width/2, y1=y + 35,
        fillcolor=color, line_width=0
    )
    # Triangle
    fig.add_shape(type="path",
        path=f" M {x-10},{y} L {x+10},{y} L {x},{y-10} Z",
        fillcolor=color, line_width=0
    )
    # Text
    fig.add_annotation(
        x=x, y=y + 17.5, text=text, showarrow=False,
        font=dict(color=colors.get("white"), size=14)
    )

# Use a coordinate system for easier placement
fig_width = 850
fig_height = 1500
fig.update_layout(
    xaxis=dict(visible=False, range=[0, fig_width]),
    yaxis=dict(visible=False, range=[0, fig_height], autorange=False) # Use fixed range
)

# --- 3. Construct each infographic element ---

# == ROW 1 ==
# Population
pop_data = data.get("population")
add_section_header(fig, 175, 1350, 160, pop_data['title'], colors.get("population"))
fig.add_trace(go.Pie(
    values=[pop_data['value_pct'], 100 - pop_data['value_pct']],
    marker_colors=[colors.get("population"), colors.get("donut_track")],
    hole=0.7,
    domain={'x': [0.05, 0.35], 'y': [0.75, 0.88]},
    hoverinfo='none', direction='clockwise', sort=False
))
fig.add_annotation(x=175, y=1210, text=f"<b>{pop_data['value_pct']}%</b>", font_size=48, showarrow=False, font_color=colors.get("text_primary"))
fig.add_annotation(x=175, y=1170, text=pop_data['label'], font_size=14, showarrow=False, font_color=colors.get("text_secondary"))
fig.add_annotation(x=175, y=1070, text=f"<b>{pop_data['value_abs']}</b>", font_size=20, showarrow=False, font_color=colors.get("text_primary"))
fig.add_annotation(x=175, y=1040, text=pop_data['subtitle'], font_size=12, showarrow=False, font_color=colors.get("text_secondary"))

# Population under 16
pop16_data = data.get("population_under_16")
add_section_header(fig, 450, 1350, 220, pop16_data['title'], colors.get("population_under_16"))
y_pos = 1270
for item in pop16_data['data']:
    fig.add_annotation(x=380, y=y_pos, text=item['category'], align='left', xanchor='left', showarrow=False, font_size=14, font_color=colors.get("text_secondary"))
    fig.add_annotation(x=520, y=y_pos, text=f"<b>{item['value']:.1f}%</b>", align='right', xanchor='right', showarrow=False, font_size=30, font_color=colors.get("population_under_16"))
    y_pos -= 60
fig.add_annotation(x=450, y=1040, text=pop16_data['subtitle'], font_size=12, showarrow=False, font_color=colors.get("text_secondary"))

# Economic Inactivity
econ_in_data = data.get("economic_inactivity")
add_section_header(fig, 690, 1350, 220, econ_in_data['title'], colors.get("economic_inactivity"))
fig.add_trace(go.Bar(
    x=[d['category'] for d in econ_in_data['data']],
    y=[d['value'] for d in econ_in_data['data']],
    marker_color=colors.get("economic_inactivity"),
    text=[f"{d['value']:.1f}%" for d in econ_in_data['data']],
    textposition='auto',
    insidetextanchor='end',
    textfont=dict(color=colors.get("white"), size=12),
    xaxis='x2', yaxis='y2'
))
fig.update_layout(
    xaxis2=dict(domain=[0.63, 0.97], anchor='y2', showticklabels=True, tickfont=dict(size=10)),
    yaxis2=dict(domain=[0.70, 0.85], anchor='x2', range=[0, 32], showgrid=False, zeroline=False, showticklabels=False)
)
fig.add_annotation(x=690, y=1040, text=econ_in_data['subtitle'], font_size=12, showarrow=False, font_color=colors.get("text_secondary"), align='center')


# == ROW 2 ==
# Economic Output
econ_out_data = data.get("economic_output")
add_section_header(fig, 175, 950, 200, econ_out_data['title'], colors.get("economic_output"))
fig.add_trace(go.Pie(
    values=[econ_out_data['value_pct'], 100 - econ_out_data['value_pct']],
    marker_colors=[colors.get("economic_output"), colors.get("donut_track")],
    hole=0.7,
    domain={'x': [0.05, 0.35], 'y': [0.5, 0.63]},
    hoverinfo='none', direction='clockwise', sort=False
))
fig.add_annotation(x=175, y=820, text=f"<b>{econ_out_data['value_pct']}%</b>", font_size=48, showarrow=False, font_color=colors.get("text_primary"))
fig.add_annotation(x=175, y=780, text=econ_out_data['label'], font_size=14, showarrow=False, font_color=colors.get("text_secondary"))
fig.add_annotation(x=175, y=690, text=econ_out_data['subtitle'], font_size=12, showarrow=False, font_color=colors.get("text_secondary"), align='center')

# Map
map_d = data.get("map_data")
fig.add_shape(type="rect", x0=350, y0=600, x1=800, y1=950, fillcolor=colors.get("map_fill"), line_width=0, layer="below")
fig.add_trace(go.Scatter(
    x=[c['x'] for c in map_d['cities']],
    y=[c['y'] for c in map_d['cities']],
    mode='markers',
    marker=dict(color=colors.get("map_points"), size=8),
    xaxis='x3', yaxis='y3'
))
for city in map_d['cities']:
    fig.add_annotation(
        x=city['x'], y=city['y'], text=city['name'], showarrow=False,
        font=dict(size=12, color=colors.get("text_primary")),
        xshift=10, yshift=10, xref='x3', yref='y3'
    )
fig.update_layout(
    xaxis3=dict(domain=[0.42, 0.93], anchor='y3', range=[0, 1], zeroline=False, showgrid=False, showticklabels=False),
    yaxis3=dict(domain=[0.40, 0.63], anchor='x3', range=[0, 1], zeroline=False, showgrid=False, showticklabels=False)
)

# == ROW 3 ==
# Weekly Earnings
earn_data = data.get("weekly_earnings")
add_section_header(fig, 175, 550, 200, earn_data['title'], colors.get("weekly_earnings"))
positions = [(115, 450), (235, 450), (115, 350), (235, 350)]
for i, item in enumerate(earn_data['data']):
    x_pos, y_pos = positions[i]
    fig.add_shape(type="circle", x0=x_pos-50, y0=y_pos-50, x1=x_pos+50, y1=y_pos+50,
                  fillcolor=colors.get("weekly_earnings"), line_color=colors.get("white"), line_width=5)
    fig.add_annotation(x=x_pos, y=y_pos + 10, text=item['category'], showarrow=False, font=dict(color=colors.get("white"), size=12))
    fig.add_annotation(x=x_pos, y=y_pos - 15, text=f"<b>{item['value']}</b>", showarrow=False, font=dict(color=colors.get("white"), size=20))
fig.add_annotation(x=175, y=250, text=earn_data['subtitle'], font_size=12, showarrow=False, font_color=colors.get("text_secondary"), align='center')

# House Prices
house_data = data.get("house_prices")
add_section_header(fig, 450, 550, 180, house_data['title'], colors.get("house_prices"))
fig.add_trace(go.Bar(
    y=[d['category'] for d in house_data['data']],
    x=[d['value'] for d in house_data['data']],
    orientation='h',
    marker_color=colors.get("house_prices"),
    text=[d['label'] for d in house_data['data']],
    textposition='auto',
    insidetextanchor='end',
    textfont=dict(color=colors.get("white"), size=12),
    xaxis='x4', yaxis='y4'
))
fig.update_layout(
    xaxis4=dict(domain=[0.44, 0.68], anchor='y4', range=[0, 280], showgrid=False, zeroline=False, showticklabels=False),
    yaxis4=dict(domain=[0.20, 0.35], anchor='x4', autorange="reversed", tickfont=dict(size=12))
)
fig.add_annotation(x=450, y=280, text=house_data['subtitle'], font_size=12, showarrow=False, font_color=colors.get("text_secondary"), align='center')

# Reduction in Greenhouse Gases
gas_data = data.get("reduction_greenhouse")
add_section_header(fig, 690, 550, 240, gas_data['title'], colors.get("greenhouse_gases"))
fig.add_trace(go.Bar(
    x=[d['category'] for d in gas_data['data']],
    y=[d['value'] for d in gas_data['data']],
    marker_color=colors.get("greenhouse_gases"),
    text=[f"{d['value']}%" for d in gas_data['data']],
    textposition='auto',
    textfont=dict(color=colors.get("white"), size=12),
    xaxis='x5', yaxis='y5'
))
fig.update_layout(
    xaxis5=dict(domain=[0.63, 0.97], anchor='y5', tickfont=dict(size=10)),
    yaxis5=dict(domain=[0.20, 0.35], anchor='x5', range=[-35, 0], showgrid=False, zeroline=False, showticklabels=False)
)
fig.add_annotation(x=690, y=280, text=gas_data['subtitle'], font_size=12, showarrow=False, font_color=colors.get("text_secondary"), align='center')


# --- 4. Add Footers and Finalize ---
fig.add_annotation(
    x=0, y=-0.01, xref="paper", yref="paper",
    text=texts.get("footer_left"),
    showarrow=False, align="left", xanchor="left",
    font=dict(size=12, color=colors.get("text_secondary"))
)
fig.add_annotation(
    x=1, y=-0.01, xref="paper", yref="paper",
    text=texts.get("footer_right"),
    showarrow=False, align="right", xanchor="right",
    font=dict(size=10, color=colors.get("text_secondary"))
)


# --- 5. Output Image ---
filename_base = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{filename_base}.png"
fig.write_image(output_filename, scale=2)
print(f"Chart saved to {output_filename}")