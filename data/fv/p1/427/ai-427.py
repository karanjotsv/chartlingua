import sys
import json
import plotly.graph_objects as go

def main():
    if len(sys.argv) != 2:
        print("Usage: python script.py <path_to_json_file>")
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

    fig = go.Figure()

    for i, series in enumerate(chart_info["chart_data"]):
        color = chart_info["colors"][i]
        
        if series["type"] == "line":
            fig.add_trace(go.Scatter(
                x=series["x"],
                y=series["y"],
                name=series["name"],
                mode='lines',
                line=dict(color=color, width=series.get("line_width", 2))
            ))
        elif series["type"] == "scatter_marker":
            fig.add_trace(go.Scatter(
                x=series["x"],
                y=series["y"],
                name=series["name"],
                mode='markers',
                marker=dict(
                    color='rgba(0,0,0,0)',
                    symbol=series.get("marker_symbol", "circle"),
                    size=series.get("marker_size", 8),
                    line=dict(color=color, width=2) if "open" in series.get("marker_symbol", "") else None
                ),
                marker_color=color
            ))

    texts = chart_info["texts"]
    
    fig.update_layout(
        title=dict(
            text=texts["title"],
            x=0.5,
            y=0.95,
            xanchor='center',
            yanchor='top'
        ),
        yaxis_title=texts["y_axis_title"],
        yaxis=dict(
            type='log',
            tickvals=[30, 100, 1000, 10000, 100000, 200000],
            gridcolor='lightgray',
            showline=True, 
            linewidth=2, 
            linecolor='black',
            mirror=True
        ),
        xaxis=dict(
            tickformat='%b<br>%d<br>%Y',
            gridcolor='lightgray',
            showline=True, 
            linewidth=2, 
            linecolor='black',
            mirror=True
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.5,
            xanchor="center",
            x=0.5
        ),
        font=dict(
            family="Arial",
            size=12
        ),
        plot_bgcolor='white',
        paper_bgcolor='white',
        margin=dict(l=80, r=40, t=80, b=200),
        autosize=False,
        width=600,
        height=500
    )

    if chart_info["chart_data"][0]["name"] == "Median daily statistic (80 years)":
        fig.update_traces(
            marker=dict(line=dict(width=1.5)), 
            selector={"name": "Median daily statistic (80 years)"}
        )
    
    output_filename = json_path.rsplit('.', 1)[0] + '.png'
    fig.write_image(output_filename, scale=2)
    print(f"Chart saved to {output_filename}")

if __name__ == "__main__":
    main()