import sys
import json
import os
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print("Usage: python <script_name>.py <json_file_path>")
    sys.exit(1)

json_path = sys.argv[1]
if not os.path.exists(json_path):
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)

with open(json_path, 'r', encoding='utf-8') as f:
    chart_data = json.load(f)

# Define constants for layout
WIDTH = 800
HEIGHT = 1200
TEXT_MAIN = chart_data["colors"]["text_main"]
TEXT_LIGHT = chart_data["colors"]["text_light"]
TEXT_WHITE = chart_data["colors"]["text_white"]

fig = go.Figure()

# --- Main Title ---
fig.add_annotation(
    text=chart_data["texts"]["main_title"],
    xref="paper", yref="paper",
    x=0.5, y=0.96,
    showarrow=False,
    font=dict(family="Arial", size=28, color=TEXT_MAIN),
    align="center"
)

# --- Define Section Header Function ---
def add_section_header(fig, x_center, y_pos, width, height, text, color):
    # Rectangle for the header background
    fig.add_shape(type="rect",
        xref="paper", yref="paper",
        x0=x_center - width/2, y0=y_pos,
        x1=x_center + width/2, y1=y_pos + height,
        fillcolor=color, line_color=color
    )
    # Text on the rectangle
    fig.add_annotation(
        text=text,
        xref="paper", yref="paper",
        x=x_center, y=y_pos + height/2,
        showarrow=False,
        font=dict(family="Arial", size=12, color=TEXT_WHITE),
        align="center"
    )
    # Pointer triangle
    fig.add_shape(type="path",
        path=f'M {x_center-0.015},{y_pos} L {x_center+0.015},{y_pos} L {x_center},{y_pos-0.02} Z',
        xref="paper", yref="paper",
        fillcolor=color, line_color=color
    )

# --- TOP ROW ---
# 1. Population
pop_x, pop_y = 0.17, 0.76
add_section_header(fig, pop_x, 0.88, 0.28, 0.03, chart_data["texts"]["section_titles"]["population"], chart_data["colors"]["section_headers"]["population"])
fig.add_trace(go.Pie(
    values=chart_data["chart_data"]["population_donut"]["values"],
    labels=["NI", "Rest"], hole=0.7,
    marker_colors=chart_data["colors"]["charts"]["population_donut"],
    domain={'x': [pop_x - 0.12, pop_x + 0.12], 'y': [pop_y - 0.1, pop_y + 0.1]},
    hoverinfo='none', textinfo='none', sort=False
))
fig.add_annotation(text=chart_data["texts"]["annotations"]["population"]["donut_center"],
    xref="paper", yref="paper", x=pop_x, y=pop_y, showarrow=False,
    font=dict(family="Arial", size=24, color=TEXT_MAIN), align="center")
fig.add_annotation(text=chart_data["texts"]["annotations"]["population"]["value"],
    xref="paper", yref="paper", x=pop_x, y=pop_y - 0.12, showarrow=False,
    font=dict(family="Arial", size=14, color=TEXT_MAIN))
fig.add_annotation(text=chart_data["texts"]["annotations"]["population"]["date"],
    xref="paper", yref="paper", x=pop_x, y=pop_y - 0.15, showarrow=False,
    font=dict(family="Arial", size=11, color=TEXT_LIGHT))

# 2. Population under 16
pu16_x, pu16_y_start = 0.49, 0.84
add_section_header(fig, pu16_x, 0.88, 0.28, 0.03, chart_data["texts"]["section_titles"]["population_under_16"], chart_data["colors"]["section_headers"]["population_under_16"])
for i, item in enumerate(chart_data["chart_data"]["population_under_16_list"]):
    fig.add_annotation(text=item["label"],
        xref="paper", yref="paper", x=pu16_x - 0.05, y=pu16_y_start - i * 0.05,
        showarrow=False, align="right", font=dict(family="Arial", size=12, color=TEXT_MAIN))
    fig.add_annotation(text=item["value"],
        xref="paper", yref="paper", x=pu16_x + 0.05, y=pu16_y_start - i * 0.05,
        showarrow=False, align="left",
        font=dict(family="Arial", size=22 if item["is_highlight"] else 18,
                  color=chart_data["colors"]["section_headers"]["population_under_16"] if item["is_highlight"] else TEXT_MAIN))
fig.add_annotation(text=chart_data["texts"]["annotations"]["population_under_16"]["date"],
    xref="paper", yref="paper", x=pu16_x, y=0.67, showarrow=False,
    font=dict(family="Arial", size=11, color=TEXT_LIGHT))

# 3. Economic Inactivity
ei_x_domain, ei_y_domain = [0.72, 0.98], [0.68, 0.86]
add_section_header(fig, 0.85, 0.88, 0.28, 0.03, chart_data["texts"]["section_titles"]["economic_inactivity"], chart_data["colors"]["section_headers"]["economic_inactivity"])
fig.add_trace(go.Bar(
    x=chart_data["chart_data"]["economic_inactivity_bar"]["categories"],
    y=chart_data["chart_data"]["economic_inactivity_bar"]["values"],
    text=[f"{v}%" for v in chart_data["chart_data"]["economic_inactivity_bar"]["values"]],
    textposition="outside", textfont=dict(family="Arial", size=11, color=TEXT_MAIN),
    marker_color=chart_data["colors"]["charts"]["economic_inactivity_bar"],
    xaxis="x1", yaxis="y1", hoverinfo='none'
))
fig.add_annotation(text=chart_data["texts"]["annotations"]["economic_inactivity"]["note"],
    xref="paper", yref="paper", x=sum(ei_x_domain)/2, y=ei_y_domain[0]-0.02,
    showarrow=False, font=dict(family="Arial", size=11, color=TEXT_MAIN), align="center")

# --- MIDDLE ROW ---
# 4. Economic Output
eo_x, eo_y = 0.17, 0.5
add_section_header(fig, eo_x, 0.62, 0.28, 0.03, chart_data["texts"]["section_titles"]["economic_output"], chart_data["colors"]["section_headers"]["economic_output"])
fig.add_trace(go.Pie(
    values=chart_data["chart_data"]["economic_output_donut"]["values"],
    labels=["NI", "Rest"], hole=0.7,
    marker_colors=chart_data["colors"]["charts"]["economic_output_donut"],
    domain={'x': [eo_x - 0.12, eo_x + 0.12], 'y': [eo_y - 0.1, eo_y + 0.1]},
    hoverinfo='none', textinfo='none', sort=False
))
fig.add_annotation(text=chart_data["texts"]["annotations"]["economic_output"]["donut_center"],
    xref="paper", yref="paper", x=eo_x, y=eo_y, showarrow=False,
    font=dict(family="Arial", size=24, color=TEXT_MAIN), align="center")
fig.add_annotation(text=chart_data["texts"]["annotations"]["economic_output"]["note"],
    xref="paper", yref="paper", x=eo_x, y=eo_y - 0.13, showarrow=False,
    font=dict(family="Arial", size=11, color=TEXT_MAIN), align="center")

# --- BOTTOM ROW ---
# 5. Weekly Earnings
we_x, we_y = 0.17, 0.2
add_section_header(fig, we_x, 0.35, 0.28, 0.03, chart_data["texts"]["section_titles"]["weekly_earnings"], chart_data["colors"]["section_headers"]["weekly_earnings"])
earnings_data = chart_data["chart_data"]["weekly_earnings_list"]
positions = [(we_x-0.07, we_y+0.05), (we_x+0.07, we_y+0.05), (we_x-0.07, we_y-0.05), (we_x+0.07, we_y-0.05)]
radius = 0.06
for i, item in enumerate(earnings_data):
    px, py = positions[i]
    fig.add_shape(type="circle", xref="paper", yref="paper",
        x0=px-radius, y0=py-radius, x1=px+radius, y1=py+radius,
        fillcolor=chart_data["colors"]["charts"]["weekly_earnings_circles"], line_color=chart_data["colors"]["charts"]["weekly_earnings_circles"])
    fig.add_annotation(text=f"{item['label']}<br><b>{item['value']}</b>",
        xref="paper", yref="paper", x=px, y=py, showarrow=False,
        font=dict(family="Arial", size=12, color=TEXT_WHITE), align="center")
fig.add_annotation(text=chart_data["texts"]["annotations"]["weekly_earnings"]["note"],
    xref="paper", yref="paper", x=we_x, y=we_y - 0.15, showarrow=False,
    font=dict(family="Arial", size=11, color=TEXT_MAIN), align="center")

# 6. House Prices
hp_x_domain, hp_y_domain = [0.38, 0.62], [0.12, 0.31]
add_section_header(fig, 0.5, 0.35, 0.28, 0.03, chart_data["texts"]["section_titles"]["house_prices"], chart_data["colors"]["section_headers"]["house_prices"])
fig.add_trace(go.Bar(
    y=chart_data["chart_data"]["house_prices_bar"]["categories"],
    x=chart_data["chart_data"]["house_prices_bar"]["values"],
    text=chart_data["chart_data"]["house_prices_bar"]["text_labels"],
    textposition="inside", insidetextanchor="middle",
    textfont=dict(family="Arial", size=11, color=TEXT_WHITE),
    marker_color=chart_data["colors"]["charts"]["house_prices_bar"],
    orientation='h', xaxis="x2", yaxis="y2", hoverinfo='none'
))
fig.add_annotation(text=chart_data["texts"]["annotations"]["house_prices"]["date"],
    xref="paper", yref="paper", x=sum(hp_x_domain)/2, y=hp_y_domain[0]-0.02,
    showarrow=False, font=dict(family="Arial", size=11, color=TEXT_LIGHT), align="center")


# 7. Reduction in Greenhouse Gases
gg_x_domain, gg_y_domain = [0.72, 0.98], [0.12, 0.31]
add_section_header(fig, 0.85, 0.35, 0.28, 0.03, chart_data["texts"]["section_titles"]["reduction_in_greenhouse_gases"], chart_data["colors"]["section_headers"]["reduction_in_greenhouse_gases"])
fig.add_trace(go.Bar(
    x=chart_data["chart_data"]["reduction_in_greenhouse_gases_bar"]["categories"],
    y=chart_data["chart_data"]["reduction_in_greenhouse_gases_bar"]["values"],
    text=[f"{abs(v)}%" for v in chart_data["chart_data"]["reduction_in_greenhouse_gases_bar"]["values"]],
    textposition="outside", textfont=dict(family="Arial", size=11, color=TEXT_MAIN),
    marker_color=chart_data["colors"]["charts"]["reduction_in_greenhouse_gases_bar"],
    xaxis="x3", yaxis="y3", hoverinfo='none'
))
fig.add_annotation(text=chart_data["texts"]["annotations"]["reduction_in_greenhouse_gases"]["note"],
    xref="paper", yref="paper", x=sum(gg_x_domain)/2, y=gg_y_domain[0]-0.02,
    showarrow=False, font=dict(family="Arial", size=11, color=TEXT_MAIN), align="center")


# --- FOOTER ---
fig.add_annotation(
    text=chart_data["texts"]["footer_source"],
    xref="paper", yref="paper", x=0.01, y=0.04,
    showarrow=False, font=dict(family="Arial", size=12, color=TEXT_MAIN),
    align="left"
)
fig.add_annotation(
    text=chart_data["texts"]["footer_note"],
    xref="paper", yref="paper", x=0.01, y=0.015,
    showarrow=False, font=dict(family="Arial", size=9, color=TEXT_LIGHT),
    align="left"
)
fig.add_annotation(
    text=f"<b>{chart_data['texts']['footer_logo_text']}</b>",
    xref="paper", yref="paper", x=0.99, y=0.025,
    showarrow=False, font=dict(family="Arial", size=12, color=TEXT_MAIN),
    align="right"
)

# --- Layout and Axis Configuration ---
fig.update_layout(
    width=WIDTH, height=HEIGHT,
    paper_bgcolor=chart_data["colors"]["background"],
    plot_bgcolor=chart_data["colors"]["background"],
    showlegend=False,
    margin=dict(l=10, r=10, t=10, b=10),
    xaxis1=dict(domain=ei_x_domain, anchor='y1', range=[None, 35], visible=False),
    yaxis1=dict(domain=ei_y_domain, anchor='x1', visible=False),
    xaxis2=dict(domain=hp_x_domain, anchor='y2', visible=False),
    yaxis2=dict(domain=hp_y_domain, anchor='x2', autorange="reversed", visible=False, tickfont=dict(size=11)),
    xaxis3=dict(domain=gg_x_domain, anchor='y3', visible=False),
    yaxis3=dict(domain=gg_y_domain, anchor='x3', range=[-35, 0], visible=False)
)
# Add category labels for horizontal bar chart
for i, cat in enumerate(chart_data["chart_data"]["house_prices_bar"]["categories"]):
    fig.add_annotation(text=cat, align='left', showarrow=False,
                       xref='paper', yref='y2',
                       x=hp_x_domain[0] + 0.01, y=cat,
                       font=dict(size=11, color=TEXT_MAIN))


# --- Output ---
filename_base = os.path.splitext(os.path.basename(json_path))[0]
fig.write_image(f"{filename_base}.png", scale=2)

print(f"Chart saved to {filename_base}.png")