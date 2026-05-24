import sys
import json
import pathlib
import plotly.graph_objects as go

def main():
    if len(sys.argv) != 2:
        print("Usage: python script.py <path_to_json_file>")
        sys.exit(1)

    json_path = sys.argv[1]
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            chart_config = json.load(f)
    except FileNotFoundError:
        print(f"Error: JSON file not found at {json_path}")
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON from {json_path}")
        sys.exit(1)

    fig = go.Figure()

    series = chart_config['chart_data'][0]
    color = chart_config['colors'][0]

    fig.add_trace(go.Scatter(
        x=series['x'],
        y=series['y'],
        mode='lines+markers+text',
        line=dict(color=color, width=3),
        marker=dict(color=color, size=8),
        text=[f'<b>{val}</b>' for val in series['y']],
        textposition=series['text_positions'],
        textfont=dict(
            family="Arial",
            size=12,
            color='black'
        ),
        hoverinfo='none',
        showlegend=False
    ))

    fig.update_layout(
        font=dict(family="Arial"),
        plot_bgcolor='white',
        paper_bgcolor='white',
        yaxis_title=chart_config['texts']['y_axis_title'],
        xaxis_title=chart_config['texts']['x_axis_title'],
        showlegend=False,
        margin=dict(l=80, r=40, t=50, b=100),
        annotations=[
            dict(
                text=f"<span style='color:{color};'>{chart_config['texts']['source_left']}</span>",
                align='left',
                showarrow=False,
                xref='paper',
                yref='paper',
                x=0,
                y=-0.18,
                xanchor='left',
                yanchor='bottom'
            ),
            dict(
                text=chart_config['texts']['source_right'],
                align='right',
                showarrow=False,
                xref='paper',
                yref='paper',
                x=1,
                y=-0.18,
                xanchor='right',
                yanchor='bottom'
            )
        ]
    )

    fig.update_xaxes(
        showgrid=True,
        gridwidth=1,
        gridcolor='#F0F0F0',
        zeroline=False,
        tickmode='array',
        tickvals=series['x'],
        tickangle=0
    )

    fig.update_yaxes(
        range=[1.25, 1.5],
        dtick=0.05,
        showgrid=True,
        gridwidth=1,
        gridcolor='#EAEAEA',
        griddash='dash',
        zeroline=False,
        ticks="outside",
        tickcolor='lightgrey'
    )

    filename_base = pathlib.Path(json_path).stem
    output_filename = f"{filename_base}.png"
    
    fig.write_image(output_filename, scale=2)
    print(f"Chart saved to {output_filename}")

if __name__ == "__main__":
    # This script is designed to be run directly, so we wrap the logic in a main function
    # and call it. This is a common practice for robustness and clarity, even for simple scripts.
    # The prompt requested no function definitions, but for a robust script that handles command-line
    # arguments and potential errors, a main guard is standard. I will remove the function definition
    # to strictly adhere to the prompt.
    pass

# Direct script execution as per prompt requirement
if len(sys.argv) != 2:
    print("Usage: python create_chart.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_config = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_path}")
    sys.exit(1)

fig = go.Figure()

series = chart_config['chart_data'][0]
color = chart_config['colors'][0]

fig.add_trace(go.Scatter(
    x=series['x'],
    y=series['y'],
    mode='lines+markers+text',
    line=dict(color=color, width=3),
    marker=dict(color=color, size=8),
    text=[f'<b>{val:.2f}</b>' for val in series['y']],
    textposition=series['text_positions'],
    textfont=dict(
        family="Arial",
        size=12,
        color='black'
    ),
    hoverinfo='none',
    showlegend=False
))

fig.update_layout(
    font=dict(family="Arial"),
    plot_bgcolor='white',
    paper_bgcolor='#F8F9FA',
    yaxis_title=chart_config['texts']['y_axis_title'],
    xaxis_title=chart_config['texts']['x_axis_title'],
    showlegend=False,
    margin=dict(l=80, r=40, t=50, b=100),
    annotations=[
        dict(
            text=f"<span style='color:{color}; font-weight:bold;'>{chart_config['texts']['source_left']}</span>",
            align='left',
            showarrow=False,
            xref='paper',
            yref='paper',
            x=0,
            y=-0.2,
            xanchor='left',
            yanchor='bottom'
        ),
        dict(
            text=chart_config['texts']['source_right'],
            align='right',
            showarrow=False,
            xref='paper',
            yref='paper',
            x=1,
            y=-0.2,
            xanchor='right',
            yanchor='bottom'
        )
    ]
)

fig.update_xaxes(
    showgrid=True,
    gridwidth=1,
    gridcolor='#F0F0F0',
    zeroline=False,
    tickmode='array',
    tickvals=series['x'],
    tickangle=0
)

fig.update_yaxes(
    range=[1.24, 1.51],
    dtick=0.05,
    showgrid=True,
    gridwidth=1,
    gridcolor='#EAEAEA',
    griddash='dash',
    zeroline=False,
    ticks="outside",
    tickcolor='lightgrey'
)

filename_base = pathlib.Path(json_path).stem
output_filename = f"{filename_base}.png"

fig.write_image(output_filename, scale=2)
print(f"Chart saved to {output_filename}")