import sys
import json
from pathlib import Path
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def main():
    if len(sys.argv) != 2:
        print(f"Usage: python {sys.argv[0]} <json_file_path>")
        sys.exit(1)

    json_path = Path(sys.argv[1])
    if not json_path.is_file():
        print(f"Error: JSON file not found at '{json_path}'")
        sys.exit(1)

    with open(json_path, 'r', encoding='utf-8') as f:
        chart_data = json.load(f)

    output_path = json_path.with_suffix(".png")
    
    texts = chart_data["texts"]
    colors = chart_data["colors"]
    facets = chart_data["chart_data"]

    # The order of reasons must be consistent across all subplots
    y_categories = [item["reason"] for item in facets[0]["data"]]

    subplot_titles = [f"<b>{facet['facet']}</b>" for facet in facets]
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=subplot_titles,
        shared_xaxes=True,
        shared_yaxes=True,
        vertical_spacing=0.08,
        horizontal_spacing=0.03
    )

    # To ensure each reason appears in the legend only once
    legend_added = set()

    for i, facet in enumerate(facets):
        row = i // 2 + 1
        col = i % 2 + 1

        # Create a dictionary for quick lookup of data points for the current facet
        facet_data_map = {item['reason']: item for item in facet['data']}

        for reason in y_categories:
            point = facet_data_map.get(reason, {"value": 0, "text": ""})
            
            # Skip drawing a bar if the value is 0
            if point["value"] == 0:
                continue

            show_legend = reason not in legend_added
            fig.add_trace(
                go.Bar(
                    x=[point["value"]],
                    y=[reason],
                    orientation='h',
                    name=reason,
                    marker_color=colors.get(reason, '#cccccc'),
                    text=point["text"],
                    textposition='auto',
                    textfont=dict(size=9, color='black'),
                    hovertemplate='%{y}: %{x:.2f}%<extra></extra>',
                    legendgroup=reason,
                    showlegend=show_legend
                ),
                row=row,
                col=col
            )
            if show_legend:
                legend_added.add(reason)

    full_title = f'<b>{texts["title"]}</b><br>{texts["subtitle"]}'
    
    fig.update_layout(
        title=dict(text=full_title, x=0.5, y=0.95, xanchor='center'),
        font=dict(family="Arial", size=12),
        width=1400,
        height=950,
        margin=dict(l=350, r=40, t=100, b=250),
        plot_bgcolor='white',
        paper_bgcolor='white',
        showlegend=True,
        legend=dict(
            title_text=f'<b>{texts["legend_title"]}</b>',
            orientation="h",
            yanchor="bottom",
            y=-0.35,
            xanchor="center",
            x=0.5,
            traceorder='normal'
        ),
        barmode='stack' # Use stack to draw bars on top of each other (for one value it just draws the bar)
    )

    fig.update_xaxes(
        showgrid=True, gridwidth=1, gridcolor='LightGray',
        range=[0, 100],
        tickformat='%g%%',
        showline=True, linewidth=1, linecolor='black'
    )
    
    # Set y-axis categories to maintain order
    fig.update_yaxes(
        categoryorder='array',
        categoryarray=y_categories,
        showline=True, linewidth=1, linecolor='black'
    )
    
    # Add shared axis titles using annotations
    fig.add_annotation(
        text=f'<b>{texts["y_axis_title"]}</b>',
        x=-0.28, y=0.5,
        xref='paper', yref='paper',
        textangle=-90,
        showarrow=False,
        font=dict(size=14)
    )
    fig.add_annotation(
        text=f'<b>{texts["x_axis_title"]}</b>',
        x=0.5, y=-0.1,
        xref='paper', yref='paper',
        showarrow=False,
        font=dict(size=14)
    )

    # Add source note
    fig.add_annotation(
        text=texts["source"],
        x=0.5, y=-0.4,
        xref='paper', yref='paper',
        showarrow=False,
        xanchor='center',
        yanchor='bottom',
        align='center',
        font=dict(size=11)
    )

    fig.write_image(output_path, scale=2)
    print(f"Chart saved to {output_path}")

if __name__ == "__main__":
    main()