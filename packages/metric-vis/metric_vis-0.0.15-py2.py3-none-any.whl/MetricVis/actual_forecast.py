from re import I
from typing import Optional, Union

import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from MetricVis.utils import *


def plot_actual_forecast(
    df: pd.DataFrame,
    actual_col: str,
    forecast_col: Union[str, list],
    lookback: int = 12,
    plot_past_year: bool = True,
    projection_col: Optional[str] = None,
    metric_name: Optional[str] = None,
    forecast_name: Optional[Union[str, list]] = None,
    projection_name: Optional[str] = None,
    percentage: bool = False,
    plot_title: Optional[bool] = None,
    forecast_color: Optional[Union[str, list]] = None,
    yaxis_title: Optional[str] = None,
    secondary_yaxis_title: Optional[str] = None,
    plotsize: Optional[list] = None,
):
    return ActualForecast(
        df=df,
        actual_col=actual_col,
        forecast_col=forecast_col,
        lookback=lookback,
        plot_past_year=plot_past_year,
        projection_col=projection_col,
        metric_name=metric_name,
        forecast_name=forecast_name,
        projection_name=projection_name,
        percentage=percentage,
        plot_title=plot_title,
        forecast_color=forecast_color,
        yaxis_title=yaxis_title,
        secondary_yaxis_title=secondary_yaxis_title,
        plotsize=plotsize,
    ).create_plot()


class ActualForecast:
    def __init__(
        self,
        df: pd.DataFrame,
        actual_col: str,
        forecast_col: Union[str, list],
        lookback: int = 12,
        plot_past_year: bool = True,
        projection_col: Optional[str] = None,
        metric_name: Optional[str] = None,
        forecast_name: Optional[Union[str, list]] = None,
        projection_name: Optional[str] = None,
        percentage: bool = False,
        plot_title: Optional[bool] = None,
        forecast_color: Optional[Union[str, list]] = None,
        yaxis_title: Optional[str] = None,
        secondary_yaxis_title: Optional[str] = None,
        plotsize: Optional[list] = None,
    ):

        self.actual_col = actual_col
        self.forecast_col = forecast_col
        self.multi_forecast = check_list_type(self.forecast_col)
        self.df = (
            df[[actual_col, projection_col] + convert_list_if_not(forecast_col)]
            if projection_col
            else df[[actual_col] + convert_list_if_not(forecast_col)]
        )
        self.lookback = lookback
        self.plot_past_year = plot_past_year
        self.projection_col = projection_col
        self.metric_name = ifnone(metric_name, clean_text(self.actual_col))
        self.metric_name_py = self.metric_name + " PY"
        self.plot_title = ifnone(plot_title, "Actual vs Forecast - " + self.metric_name)
        self.percentage = percentage
        self.number_format = format_percentage if percentage else format_absolute
        self.forecast_name = ifnone(
            forecast_name,
            [self.metric_name + f" Forecast {i+1}" for i in range(len(forecast_col))]
            if self.multi_forecast
            else self.metric_name + " Forecast",
        )
        self.projection_name = ifnone(projection_name, self.metric_name + " Projection")
        self.plot_df = self._create_monthly_df(self.df)
        self.forecast_color = ifnone(forecast_color, CORE_COLOURS)
        self.yaxis_title = ifnone(yaxis_title, self.metric_name)
        self.secondary_yaxis_title = ifnone(secondary_yaxis_title, "YOY Growth")
        self.plotsize = plotsize

    def _create_monthly_df(self, df):
        plot_df = df.resample("1M").last()
        plot_df["month"] = plot_df.index.month
        plot_df["year"] = plot_df.index.year

        if self.multi_forecast:
            rename_dict = {i: j for i, j in zip(self.forecast_col, self.forecast_name)}
            rename_dict[self.actual_col] = self.metric_name
        else:
            rename_dict = {
                self.actual_col: self.metric_name,
                self.forecast_col: self.forecast_name,
            }

        if self.projection_col:
            rename_dict[self.projection_col] = self.projection_name

        plot_df.rename(
            rename_dict,
            axis=1,
            inplace=True,
        )

        final_index = np.where(plot_df[self.metric_name].notnull())[0][-1]
        start_index = max(0, final_index - self.lookback + 1)

        plot_df_sample = plot_df.iloc[start_index:]
        plot_df_sample = plot_df_sample.drop(self.forecast_name, axis=1)
        if self.plot_past_year:
            plot_df_sample[self.metric_name_py] = plot_df_sample.apply(
                get_month_before, axis=1, df=plot_df, col=self.metric_name
            )
            plot_df_sample["YOY Growth"] = (
                plot_df_sample[self.metric_name] / plot_df_sample[self.metric_name_py]
                - 1
            )

        plot_columns = (
            convert_list_if_not(self.forecast_name) + [self.projection_name]
            if self.projection_col
            else convert_list_if_not(self.forecast_name)
        )

        final_plot_df = (
            plot_df[plot_columns]
            .loc[plot_df_sample.index[0] :]
            .merge(plot_df_sample, how="left", left_index=True, right_index=True)
        )

        return final_plot_df

    def create_plot(self):
        fig = make_subplots(
            specs=[[{"secondary_y": True}]],
        )

        fig.add_trace(
            go.Scatter(
                x=self.plot_df.index,
                y=self.plot_df[self.metric_name],
                name=self.metric_name,
                legendgroup=self.metric_name,
                line=dict(color="#0052CC"),
                showlegend=True,
                mode="lines+markers+text",
                text=self.plot_df[self.metric_name].apply(self.number_format),
                textposition="top center",
                cliponaxis=False,
            ),
            secondary_y=True,
        )

        if self.projection_col:

            fig.add_trace(
                go.Scatter(
                    x=self.plot_df.index,
                    y=self.plot_df[self.projection_name],
                    name=self.projection_name,
                    legendgroup=self.projection_name,
                    line=dict(color="#0052CC", dash="dash"),
                    showlegend=True,
                    mode="lines",
                ),
                secondary_y=True,
            )

        for i, j in zip(convert_list_if_not(self.forecast_name), self.forecast_color):
            fig.add_trace(
                go.Scatter(
                    x=self.plot_df.index,
                    y=self.plot_df[i],
                    name=i,
                    legendgroup=i,
                    line=dict(color=j),
                    showlegend=True,
                    mode="lines",
                ),
                secondary_y=True,
            )

        if self.plot_past_year:
            fig.add_trace(
                go.Scatter(
                    x=self.plot_df.index,
                    y=self.plot_df["YOY Growth"],
                    name="YOY Growth",
                    legendgroup="YOY Growth",
                    line=dict(color="#C1C7D0", dash="dash"),
                    showlegend=True,
                    mode="lines",
                )
            )

            fig.add_trace(
                go.Scatter(
                    x=self.plot_df.index,
                    y=self.plot_df[self.metric_name_py],
                    name=self.metric_name_py,
                    legendgroup=self.metric_name_py,
                    line=dict(color="#C1C7D0"),
                    showlegend=True,
                    mode="lines",
                ),
                secondary_y=True,
            )

        fig.update_layout(
            legend=dict(
                orientation="h", xanchor="center", yanchor="bottom", x=0.5, y=-0.5
            ),
            legend_title_text="",
            plot_bgcolor="white",
            title=self.plot_title,
        )

        fig.update_layout(
            dict(
                yaxis2={"anchor": "x", "overlaying": "y", "side": "left"},
                yaxis={"anchor": "x", "side": "right"},
                yaxis_tickformat=".0%",
                yaxis2_tickformat=".0%" if self.percentage else "~s",
            )
        )

        fig.update_yaxes(title_text=self.yaxis_title, secondary_y=True)
        fig.update_yaxes(title_text=self.secondary_yaxis_title, secondary_y=False)

        if self.plotsize:
            fig.update_layout(
                width=self.plotsize[0],
                height=self.plotsize[1],
            )

        return fig
