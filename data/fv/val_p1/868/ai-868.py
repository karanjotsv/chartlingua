import sys
import json
from pathlib import Path
import plotly.graph_objects as go

def main():
    if len(sys.argv) != 2:
        print(f"Usage: python {sys.argv[0]} <json_file_path>")
        sys.exit(1)

    json_path = Path(sys.argv[1])
    if not json_path.is_file():
        print(f"Error: File not found at {json_path}")
        sys.exit(1)

    with open(json_path, 'r', encoding='utf-8') as f:
        chart_info = json.load(f)

    chart_data = chart_info["chart_data"]
    texts = chart_info["texts"]
    colors = chart_info["colors"]

    fig = go.Figure()

    for i, series in enumerate(chart_data["series"]):
        fig.add_trace(go.Scatter(
            x=chart_data["x"],
            y=series["y"],
            name=series["name"],
            mode='lines',
            line=dict(color=colors[i])
        ))
    
    # Construct combined title string
    title_text = ""
    if texts.get("title"):
        title_text += f'<b>{texts["title"]}</b>'
    if texts.get("subtitle"):
        if title_text:
            title_text += "<br>"
        title_text += f'<i>{texts["subtitle"]}</i>'

    fig.update_layout(
        plot_bgcolor='white',
        paper_bgcolor='rgb(240,240,240)',
        font=dict(family="Arial", size=12),
        margin=dict(t=60, r=40, b=80, l=80),
        title=dict(
            text=title_text if title_text else None,
            x=0.05,
            xanchor='left'
        ),
        xaxis=dict(
            title=texts.get("x_axis_title"),
            tickvals=["2015-06-01", "2015-06-08", "2015-06-15", "2015-06-22"],
            ticktext=["Jun 01", "Jun 08", "Jun 15", "Jun 22"],
            tickformat="%b %d",
            showgrid=True,
            gridcolor='lightgrey',
            gridwidth=1,
            zeroline=False
        ),
        yaxis=dict(
            title=texts.get("y_axis_title"),
            range=[0, 70000],
            showgrid=True,
            gridcolor='lightgrey',
            gridwidth=1,
            zeroline=False
        ),
        legend=dict(
            title_text=texts.get("legend_title"),
            traceorder="normal"
        )
    )
    
    # Add source/note at the bottom
    if texts.get("source"):
        fig.add_annotation(
            text=texts["source"],
            xref="paper", yref="paper",
            x=0, y=-0.15,
            showarrow=False,
            align="left",
            xanchor="left",
            yanchor="top"
        )

    output_filename = f"{json_path.stem}.png"
    fig.write_image(output_filename, scale=2)
    print(f"Chart saved to {output_filename}")

if __name__ == "__main__":
    main()