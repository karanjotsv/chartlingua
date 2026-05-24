import sys
import json
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os

def main():
    """
    Main function to generate the chart from a JSON file.
    """
    if len(sys.argv) != 2:
        print("Usage: python generate_chart.py <path_to_json>")
        sys.exit(1)

    json_path = sys.argv[1]
    if not os.path.exists(json_path):
        print(f"Error: JSON file not found at {json_path}")
        sys.exit(1)

    with open(json_path, 'r', encoding='utf-8') as f:
        config = json.load(f)

    chart_data = config['chart_data']
    colors = config['colors']
    
    fig = make_subplots(rows=1, cols=2, specs=[[{'type': 'domain'}, {'type': 'domain'}]])

    # Add first pie chart
    fig.add_trace(go.Pie(
        labels=chart_data[0]['labels'],
        values=chart_data[0]['values'],
        marker=dict(colors=colors['slices']),
        pull=[0.05, 0.05, 0.05, 0.05],
        sort=False,
        textinfo='none',
        hoverinfo='none',
        name=''  # Use an empty name to avoid trace name in hover
    ), 1, 1)

    # Add second pie chart
    fig.add_trace(go.Pie(
        labels=chart_data[1]['labels'],
        values=chart_data[1]['values'],
        marker=dict(colors=colors['slices']),
        pull=[0.05, 0.05, 0.05, 0.05],
        sort=False,
        textinfo='none',
        hoverinfo='none',
        showlegend=False, # Hide legend for the second pie to avoid duplicates
        name=''
    ), 1, 2)

    annotations = [
        dict(
            text=chart_data[0]['title'],
            x=0.22,
            y=1.08,
            font_size=28,
            showarrow=False,
            font=dict(color=colors['text'])
        ),
        dict(
            text=chart_data[1]['title'],
            x=0.78,
            y=1.08,
            font_size=28,
            showarrow=False,
            font=dict(color=colors['text'])
        )
    ]
    
    fig.update_layout(
        annotations=annotations,
        paper_bgcolor=colors['background'],
        plot_bgcolor=colors['background'],
        font=dict(
            family="Arial",
            color=colors['text']
        ),
        margin=dict(t=100, b=100, l=40, r=40),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.1,
            xanchor="center",
            x=0.5,
            font=dict(color=colors['text'])
        )
    )

    filename_base = os.path.splitext(os.path.basename(json_path))[0]
    output_filename = f"{filename_base}.png"

    fig.write_image(output_filename, scale=2)
    print(f"Chart saved to {output_filename}")

if __name__ == "__main__":
    main()