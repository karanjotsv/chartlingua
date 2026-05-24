import sys
import json
import os
import plotly.graph_objects as go

def main():
    if len(sys.argv) != 2:
        print("Usage: python <script_name>.py <json_file_path>")
        sys.exit(1)

    json_path = sys.argv[1]
    if not os.path.exists(json_path):
        print(f"Error: JSON file not found at '{json_path}'")
        sys.exit(1)

    with open(json_path, 'r', encoding='utf-8') as f:
        chart_data = json.load(f)

    fig = go.Figure()

    # Add traces from JSON data
    for series in chart_data["chart_data"]:
        if series["type"] == "line":
            fig.add_trace(go.Scatter(
                x=series["x"],
                y=series["y"],
                name=series["name"],
                mode='lines',
                line=dict(
                    color=series["style"]["color"],
                    width=series["style"]["width"]
                ),
                showlegend=series["showlegend"]
            ))
        elif series["type"] == "markers":
            fig.add_trace(go.Scatter(
                x=series["x"],
                y=series["y"],
                name=series["name"],
                mode='markers',
                marker=dict(
                    color=series["style"]["color"],
                    size=series["style"]["size"],
                    line=dict(
                        color=series["style"]["line"]["color"],
                        width=series["style"]["line"]["width"]
                    )
                ),
                showlegend=series["showlegend"]
            ))

    # Add annotations
    for ann in chart_data["texts"]["annotations"]:
        fig.add_annotation(
            x=ann["x"],
            y=ann["y"],
            text=ann["text"],
            showarrow=False,
            align=ann.get("align", "left"),
            xanchor='left' if ann.get("align", "left") == 'left' else 'center',
            font=dict(family="Arial", size=10, color="black")
        )

    # Update layout
    fig.update_layout(
        plot_bgcolor='white',
        paper_bgcolor='white',
        font=dict(family="Arial", size=12, color="black"),
        xaxis=dict(
            title_text=chart_data["texts"]["x_axis_title"],
            range=[1790, 2110],
            tickmode='linear',
            dtick=20,
            showgrid=True,
            gridwidth=1,
            gridcolor='lightgrey',
            linecolor='black'
        ),
        yaxis=dict(
            title_text=chart_data["texts"]["y_axis_title"],
            range=[0, 16000],
            tickmode='linear',
            dtick=1000,
            showgrid=True,
            gridwidth=1,
            gridcolor='lightgrey',
            linecolor='black'
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.2,
            xanchor="center",
            x=0.5
        ),
        margin=dict(l=80, r=40, t=40, b=120)
    )

    # Generate output filename and save image
    base_filename = os.path.splitext(os.path.basename(json_path))[0]
    output_filename = f"{base_filename}.png"

    fig.write_image(output_filename, scale=2)
    print(f"Chart saved to {output_filename}")

if __name__ == "__main__":
    main()