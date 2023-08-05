#!python
# -*- coding: utf-8 -*-
# @Time : 2022/10/21 11:27
# @Author : jmzhang
# @Email : zhangjm@biomarker.com.cn

from matplotlib.axes._axes import _log as matplotlib_axes_logger
import matplotlib.pyplot as plt
from matplotlib import image
from pathlib import Path
import seaborn as sns
import pandas as pd
import scanpy as sc
import numpy as np
import warnings
import argparse
import logging
import anndata
import json
import math

FORMAT = '%(asctime)s %(message)s'
logging.basicConfig(level=logging.INFO, format=FORMAT, datefmt='%Y-%m-%d %H:%M:%S')

matplotlib_axes_logger.setLevel('ERROR')
warnings.filterwarnings("ignore")

sc.set_figure_params(facecolor="white", figsize=(8, 8))
sc.settings.verbosity = 3


class SpatialApp:
    styles = {
        'pre': {
            'border': 'thin lightgrey solid',
            'overflowX': 'scroll'
        }
    }
    TOKEN = None

    @classmethod
    def run_dash(cls, spatial_tools_obj, adata, port=30000, debug=True):
        from dash import Input, Output, dcc, html
        import plotly.express as px
        # import dash_daq as daq
        import dash_bootstrap_components as dbc

        from jupyter_dash import JupyterDash

        app = JupyterDash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
        cls.TOKEN = JupyterDash._token
        color_scales = px.colors.named_colorscales() + [i + '_r' for i in px.colors.named_colorscales()]

        if isinstance(adata, pd.DataFrame):
            color_by_info = adata.columns
            feature_info = adata.columns
            meta_data = adata

        elif isinstance(adata, anndata.AnnData):
            color_by_info = adata.obs.columns
            feature_info = adata.var.index
            meta_data = adata.obs

        else:
            raise ValueError('adata should be pd.DataFrame or anndata.AnnData ...')

        # if 'leiden' in color_by_info:
        #     color_by_value = 'leiden'
        # elif 'seurat_cluster' in color_by_info:
        #     color_by_value = 'seurat_cluster'
        # elif 'cellType' in color_by_info:
        #     color_by_value = 'cellType'
        # else:
        #     color_by_value = ''

        controls = dbc.Card(
            [
                html.Div([
                    html.Label('set He figure'),
                    dcc.RadioItems(
                        ['low He', 'no He', 'hire He', 'only He'], 'low He',
                        id='pic_data',
                        labelStyle={"margin-left": "10px"}),

                    html.Br(),
                    html.Label('set point size'),
                    dcc.Slider(
                        id='point_size',
                        min=0,
                        max=3,
                        value=0.3,
                    ),

                    html.Br(),
                    html.Label('Color by'),
                    dcc.Dropdown(color_by_info,
                                 id='color_by'),

                    html.Br(),
                    html.Label('Multi-Select groups'),
                    dcc.Dropdown(id='groups',
                                 multi=True),

                    html.Br(),
                    html.Label('Feature'),
                    dcc.Dropdown(feature_info,
                                 'NULL',
                                 id='feature'),

                    html.Br(),
                    html.P("Feature color Scale"),
                    dcc.Dropdown(
                        id='cmap',
                        options=color_scales,
                        value='viridis'
                    ),

                    html.Br(),
                    html.Label('Zoom area: y1, y2, x1, x2  :'),
                    dcc.Input(value='NULL', type='text', id='crop_coord'),

                    html.Br(),
                    html.Br(),
                    html.Label('Selected point'),
                    html.Div(id='selected-data',
                             style=cls.styles['pre'],
                             children='Please using lasso or box select ...')
                ])
            ],
            body=True, style={"padding": "10px"}
        )

        app.layout = dbc.Container(
            [
                html.H1("Spatial Tools For Vision"),
                html.Hr(),
                dbc.Row(
                    [
                        dbc.Col(controls, md=3, style={'height': '50vh'}),
                        dbc.Col(dcc.Graph(id="cluster-graph", style={'width': '80vh', 'height': '80vh'}),
                                md=6),
                    ],
                    align="center",
                ),
            ],
            fluid=True,
        )

        @app.callback(
            Output('groups', 'options'),
            Input('color_by', 'value'))
        def set_groups_value(color_by):
            logging.info(color_by)
            logging.info(meta_data[color_by].unique())
            return [str(_) for _ in meta_data[color_by].unique()]

        @app.callback(
            Output('selected-data', 'children'),
            Input('cluster-graph', 'selectedData'))
        def display_selected_data(selectedData):
            if selectedData:
                return json.dumps([i['text'] for i in selectedData['points']])
            else:
                return json.dumps('Please using lasso or box select ...')

        @app.callback(
            Output("cluster-graph", "figure"),
            [
                Input("color_by", 'value'),
                Input('feature', 'value'),
                Input("pic_data", "value"),
                Input('cmap', 'value'),
                Input("point_size", "value"),
                Input('groups', 'value'),
                Input('crop_coord', 'value')
            ],
        )
        def make_graph(color_by, feature, pic_data, cmap, point_size, groups, crop_coord):

            if pic_data == 'no He':
                draw_pic = False
                low_pic = False
            else:
                draw_pic = True

                if pic_data == 'low He':
                    low_pic = True
                else:
                    low_pic = False

            if pic_data == 'only He':

                pic_only = True
                low_pic = False
            else:
                pic_only = False

            if crop_coord != 'NULL' and crop_coord != '':
                crop_coord = [i.strip() for i in crop_coord.split(',')]
            else:
                crop_coord = False

            if str(color_by) == 'None' and str(feature) == 'NULL':

                if pic_data == 'hire He':
                    return px.imshow(spatial_tools_obj.__dict__['_pic'])
                else:
                    return px.imshow(spatial_tools_obj.__dict__['_low_pic'])

            if str(feature) == 'NULL':
                feature = False

            pic = spatial_tools_obj.s1000_spatial_plot(adata=adata,
                                                       color=color_by,
                                                       feature=feature,
                                                       size=point_size,
                                                       cmap=cmap,
                                                       groups=list(groups) if groups else groups,
                                                       crop_coord=crop_coord,
                                                       draw_pic=draw_pic,
                                                       low_pic=low_pic,
                                                       pic_only=pic_only,
                                                       interactive=True)

            return pic

        logging.info('listen: http://127.0.0.1:{}/'.format(port))
        app.run_server(debug=debug, mode='external', port=port, host='127.0.0.1')

    @classmethod
    def terminate_server_for_port(cls):
        import requests

        shutdown_url = "http://{host}:{port}/_shutdown_{token}".format(
            host='127.0.0.1', port='30000', token=cls.TOKEN
        )
        try:
            response = requests.get(shutdown_url)
        except Exception as e:
            pass

    @staticmethod
    def plotly_plot_save(to_save, fig):
        import plotly
        if not Path(to_save).parent.exists():
            Path(to_save).parent.mkdir(exist_ok=True, parents=True)

        plotly.offline.plot(fig, filename=to_save + '.html')

    @classmethod
    def interact_pic_discrete(cls,
                              plot_data_grouped,
                              pic,
                              color,
                              size,
                              color_dict,
                              to_save,
                              figsize=(8, 8),
                              draw_pic=True,
                              pic_only=False):

        import plotly.graph_objects as go
        import plotly.express as px

        if pic_only:
            return px.imshow(pic)

        if draw_pic:
            fig = px.imshow(pic)
        else:
            fig = go.Figure()

        if len(color_dict) > 100:
            raise 'too much value'

        for key, group in plot_data_grouped:
            fig.add_trace(
                go.Scatter(x=group['__x'],
                           y=group['__y'],
                           mode='markers',
                           marker=dict(color=group[plot_data_grouped.keys].map(color_dict),
                                       size=size),
                           text=group['barcode'],
                           name=key
                           ))

        fig.update_layout(
            legend=dict(yanchor="top",
                        itemsizing='constant',
                        font=dict(
                            size=14,
                            color="black"
                        ),
                        y=0.8),
            title={
                'text': 'color by : {}'.format(color),
                'x': 0.45,
                'xanchor': 'center',
                'yanchor': 'top'},
            activeshape_opacity=0.9,
            width=float(figsize[0]) * 100,
            height=float(figsize[1]) * 100,
            margin=dict(l=40, r=40, t=40, b=40),
        )

        if not draw_pic:
            fig['layout']['yaxis']['autorange'] = "reversed"

        if to_save:
            cls.plotly_plot_save(to_save=to_save, fig=fig)

        return fig

    @classmethod
    def interact_pic_continuous(cls,
                                plot_data,
                                pic,
                                feature,
                                size,
                                to_save,
                                cmap,
                                figsize=(8, 8),
                                draw_pic=True,
                                pic_only=False):

        import plotly.graph_objects as go
        import plotly.express as px

        if pic_only:
            return px.imshow(pic)

        if draw_pic:
            fig = px.imshow(pic)
        else:
            fig = go.Figure()

        info_list = list(zip(plot_data['barcode'], plot_data[feature]))

        fig.add_trace(
            go.Scatter(x=plot_data['__x'],
                       y=plot_data['__y'],
                       mode='markers',
                       marker=dict(size=size,
                                   color=plot_data[feature],
                                   colorscale=cmap,
                                   showscale=True),
                       text=['barcode:{} \n value:{}'.format(str(i[0]), str(i[1])) for i in info_list]  # ,
                       )
        )

        fig.update_layout(
            title={
                'text': 'feature: {}'.format(feature),
                # 'y': 0.9,
                'x': 0.5,
                'xanchor': 'center',
                'yanchor': 'top'},

            autosize=True,
            width=float(figsize[0]) * 100,
            height=float(figsize[1]) * 100,
            margin=dict(l=40, r=40, t=40, b=40)
        )

        if not draw_pic:
            fig['layout']['yaxis']['autorange'] = "reversed"

        if to_save:
            cls.plotly_plot_save(to_save=to_save, fig=fig)

        return fig


class SpatialTools:

    def __init__(self, pic, barcodes_pos, low_pic=None):
        self._pic = image.imread(pic)

        if low_pic:
            self._low_pic = image.imread(low_pic)
            self._low_contain = True
            self.low_scalar = self._cal_zoom_rate(self._low_pic.shape[0], self._low_pic.shape[1])
        else:
            self._low_pic = None
            self._low_contain = False

        self.obsm = pd.read_csv(barcodes_pos, '\t', names=['barcode', '__x', '__y'])

        self.point_size = self._auto_cal_radius(self.obsm)
        self.scalar = self._cal_zoom_rate(self._pic.shape[0], self._pic.shape[1])
        self.level = str(self.obsm['barcode'][0]).split('_')[0]

        self._adata_type = None
        self._facet_pos_list = None

    def __str__(self):
        info = 'low pic: {}\nlevel: {}\nscalar: {}'. \
            format('True' if self._low_contain else 'False',
                   self.level, self.scalar)
        return info

    @property
    def pic(self):
        return plt.imshow(self._pic)

    @property
    def low_pic(self):
        if not self._low_contain:
            raise ValueError('no low pic in SpatialTools')
        else:
            return plt.imshow(self._low_pic)

    @staticmethod
    def _cal_zoom_rate(width, height):
        """from litt@biomarker.com.cn SpatialCluster_split"""
        std_width = 1000
        std_height = std_width / (46 * 31) * (46 * 36 * np.sqrt(3) / 2.0)
        if std_width / std_height > width / height:
            scale = width / std_width
        else:
            scale = height / std_height
        return scale

    @staticmethod
    def _auto_cal_radius(cluster_pos_df):
        """from litt@biomarker.com.cn SpatialCluster_split"""
        radius = 999999
        pref_pos = [0, 0]
        for index, item in cluster_pos_df.iterrows():
            if index != 0:
                curr_pos = [item['__y'], item['__x']]
                center_dist = np.sqrt((curr_pos[0] - pref_pos[0]) ** 2 + (curr_pos[1] - pref_pos[1]) ** 2)
                if center_dist < radius:
                    radius = center_dist
            pref_pos = [item['__y'], item['__x']]
            if index > 1000:
                break
        radius = round(radius * 0.618 / 2)
        if radius < 1:
            radius = 1

        return radius

    @staticmethod
    def _plot_save(fig: plt, to_save):
        if not Path(to_save).parent.exists():
            Path(to_save).parent.mkdir(exist_ok=True, parents=True)

        fig.savefig('{}.png'.format(to_save), bbox_inches='tight', dpi=500)
        fig.savefig('{}.pdf'.format(to_save), bbox_inches='tight')

    @staticmethod
    def resolve_para_to_list_tuple_dict(input_str, instance_type, element_type=None):
        if instance_type == dict:
            res = {str(_[0]).strip(): str(_[1]).strip() for _ in
                   [i.split(':') for i in input_str.replace('{', '').replace('}', '').split(',')]}

        else:
            res = instance_type(
                [element_type(i.strip()) for i in input_str.replace(')', '').replace('(', '').split(',')])

        return res

    @staticmethod
    def _lighten_color(color, amount=0.5):
        """
        Lightens the given color by multiplying (1-luminosity) by the given amount.
        Input can be matplotlib color string, hex string, or RGB tuple.
        Examples:
        >> lighten_color('g', 0.3)
        >> lighten_color('#F034A3', 0.6)
        >> lighten_color((.3,.55,.1), 0.5)
        """
        import matplotlib.colors as mc
        import colorsys
        try:
            c = mc.cnames[color]
        except:
            c = color
        c = colorsys.rgb_to_hls(*mc.to_rgb(c))
        return colorsys.hls_to_rgb(c[0], 1 - amount * (1 - c[1]), c[2])

    def _facet_pos(self, length, ncol):
        nrow = math.ceil(length / ncol)
        facet_pos_list = []
        for i in range(nrow):
            for x in range(ncol):
                facet_pos_list.append((i, x))

        self._facet_pos_list = facet_pos_list

        return nrow, ncol

    @staticmethod
    def _change_para_dict(origin: dict, changed: dict):
        for k, v in changed.items():
            if k not in origin.keys():
                raise ValueError('wrong para_dict key value : {}'.format(k))

            origin[k] = v

        return origin

    def _discrete_scatter_plot(self, ax, para_dict: dict, color_dict):
        plot_para_dict = {'title': '', 'xlabel': 'S1000 spatial 1', 'ylabel': 'S1000 spatial 2',
                          'legend_scale': 1.2, 'legend_ncol': math.ceil(len(color_dict) / 17),
                          'show_ticks_and_labels': True}

        if para_dict:
            plot_para_dict = self._change_para_dict(plot_para_dict, para_dict)

        box = ax.get_position()
        ax.set_position([box.x0, box.y0, box.width * 0.99, box.height * 0.99])

        ax.legend(
            loc='center left',
            markerscale=float(plot_para_dict['legend_scale']),
            bbox_to_anchor=(1, 0.5), ncol=int(plot_para_dict['legend_ncol']),
            fontsize=16, frameon=False, handletextpad=0.3)

        plt.title(plot_para_dict['title'])
        plt.xlabel(plot_para_dict['xlabel'])
        plt.ylabel(plot_para_dict['ylabel'])

        if not plot_para_dict['show_ticks_and_labels'] or plot_para_dict['show_ticks_and_labels'] == 'False':
            plt.xticks([])
            plt.yticks([])
            ax.xaxis.set_ticklabels([])
            ax.yaxis.set_ticklabels([])

    def _continuous_scatter_plot(self):
        pass

    def _crop_coord(self, plot_data, crop_coord: list, low_pic=False):
        x1, x2, y1, y2 = [int(_) for _ in crop_coord]
        pic = self._low_pic if low_pic else self._pic
        pic = pic[x1:x2, y1:y2, :]

        plot_data = plot_data.query('{} <= __x <= {} & {} <= __y <= {}'.format(y1, y2, x1, x2))
        plot_data2 = plot_data.copy()

        plot_data2['__y'] = plot_data2['__y'] - x1
        plot_data2['__x'] = plot_data2['__x'] - y1

        return pic, plot_data2

    def s1000_spatial_plot(self, adata: anndata,
                           color='seurat_clusters',
                           groups=None,
                           size=1,
                           alpha=1,
                           alpha_map_to_value=False,
                           cmap='viridis',
                           value_limits=None,
                           figsize=(10, 10),
                           crop_coord=None,
                           to_save=None,
                           darken=None,
                           return_fig=False,
                           return_table=False,
                           feature=None,
                           split=False,
                           ncol=2,
                           color_dict: dict = None,
                           hspace=None,
                           wspace=None,
                           para_dict=None,
                           draw_pic=True,
                           low_pic=False,
                           interactive=False,
                           pic_only=False,
                           run_dash=False):
        """
        - adata:
        - color:
        - para_dict:
            - discrete_scatter_plot:
                {'title': '', 'xlabel': 'S1000 spatial 1', 'ylabel': 'S1000 spatial 2',
                 'legend_scale': 1.2, 'legend_ncol': math.ceil(len(self.color_dict) / 17),
                 'show_ticks_and_labels': True}
                - title: 标题
                - xlabel: x轴标题
                - ylabel: y轴标题
                - legend_scale: 图例图形大小
                - legend_ncol: 图例列数，默认一列17个元素
                - show_ticks_and_labels: 是否展示刻度

            - continuous_scatter_plot
                {'xlabel': 'S1000 spatial 1', 'ylabel': 'S1000 spatial 2',
                 'show_ticks_and_labels': True, 'shrink': 0.4, 'pad': 0.05}

        """
        if color == 'class':
            raise 'please change columns of class'

        if low_pic:
            if not self._low_contain:
                raise ValueError('no low pic in SpatialTools')

        if isinstance(adata, sc.AnnData):
            adata = adata.copy()
            adata.obs.index.name = None
            adata.obs['barcode'] = adata.obs.index
            self._adata_type = 'AnnData'
            plot_data = self.obsm.merge(adata.obs, on='barcode')

        elif isinstance(adata, pd.DataFrame):
            adata = adata.copy()
            adata.index.name = None

            if 'barcode' not in adata.columns:
                adata['barcode'] = adata.index

            self._adata_type = 'DataFrame'
            plot_data = self.obsm.merge(adata, on='barcode')

        else:
            raise 'wrong adata, should be AnnData and DataFrame'

        if plot_data.shape[0] == 0:
            raise ValueError('barcodes of pic and matrix are inconsistent ...')

        if not feature:

            plot_data[color] = plot_data[color].astype(str)

            # 离散型散点图
            prob = list(plot_data[color].value_counts().index)

            if not color_dict:
                number_col = len(prob)
                if number_col <= 12:
                    selected_col = list(sns.color_palette("Paired", number_col))
                else:
                    selected_col = list(sns.color_palette(None, number_col))

                color_dict = dict(zip(prob, selected_col))

            if groups:

                for i in groups:
                    if i not in plot_data[color].unique():
                        raise 'groups not in column of color'

                plot_data = plot_data.query('{} in {}'.format(color, groups))
                plot_data[color] = plot_data[color].astype("category")
                plot_data[color] = plot_data[color].cat.set_categories(groups, ordered=True)
                prob = groups

            if darken:
                color_dict = {k: self._lighten_color(v, darken) for k, v in color_dict.items()}

            if not low_pic:
                plot_data['__x'] = plot_data['__x'] * self.scalar
                plot_data['__y'] = plot_data['__y'] * self.scalar

            else:
                plot_data['__x'] = plot_data['__x'] * self.low_scalar
                plot_data['__y'] = plot_data['__y'] * self.low_scalar

            if crop_coord:
                plot_pic, plot_data = self._crop_coord(plot_data=plot_data, low_pic=low_pic, crop_coord=crop_coord)
            else:
                plot_pic = self._low_pic if low_pic else self._pic

            size = self.point_size ** 2 if size == 1 else self.point_size ** 2 * size

            grouped = plot_data.groupby(color)

            # 执行交互
            if interactive or run_dash:
                fig = SpatialApp.interact_pic_discrete(plot_data_grouped=grouped,
                                                       pic=plot_pic,
                                                       color=color,
                                                       color_dict=dict(
                                                           zip(prob, sns.color_palette(None, len(prob)).as_hex())),
                                                       size=size,
                                                       figsize=figsize,
                                                       pic_only=pic_only,
                                                       draw_pic=draw_pic,
                                                       to_save=to_save)

                return fig

            fig, ax = plt.subplots(constrained_layout=True, figsize=figsize)

            start = 0
            for key, group in grouped:

                if key in prob:
                    if split:
                        grid_dim = self._facet_pos(length=len(prob), ncol=ncol)
                        ax = plt.subplot2grid(grid_dim, self._facet_pos_list[start])
                        plt.tight_layout()
                        start += 1

                    group.plot(ax=ax, kind='scatter', x='__x', y='__y',
                               label=key,
                               c=color_dict[key],
                               s=size,
                               alpha=alpha)

                    self._discrete_scatter_plot(ax=ax,
                                                para_dict=para_dict,
                                                color_dict=color_dict)

                    if wspace:
                        plt.subplots_adjust(hspace=int(wspace))
                    if hspace:
                        plt.subplots_adjust(hspace=int(hspace))

                    if draw_pic:
                        plt.imshow(plot_pic)

            if not draw_pic:
                plt.gca().invert_yaxis()

            # plot_data = plot_data2

            # handles, labels = plt.gca().get_legend_handles_labels()
            # if self.levels:
            #     legend_order = [labels.index(i) for i in self.levels]
            # else:
            #     legend_order = [labels.index(i) for i in labels]
            #
            # ax.legend([handles[idx] for idx in legend_order], [labels[idx] for idx in legend_order])

        else:
            # 连续型散点图
            if not isinstance(feature, list):
                feature = [feature]

            if self._adata_type == 'AnnData':
                # in Anndata
                adata.var['symbol'] = adata.var.index
                prob = [i for i in feature if i in adata.obs.columns]

                if 'gene_ids' not in adata.var.columns:
                    adata.var['gene_ids'] = adata.var.index

                if 'symbol' not in adata.var.columns:
                    adata.var['symbol'] = adata.var.index

                symbol = list(adata.var.query('gene_ids in {} or symbol in {}'.format(feature, feature)).index)
                if not len(symbol) == 0:
                    gene_df = adata[:, symbol].to_df()
                    gene_df['barcode'] = gene_df.index
                    plot_data = plot_data.merge(gene_df, on='barcode')
                    prob += symbol

            else:
                prob = [i for i in feature if i in adata.columns]

            if len(prob) == 0:
                raise ValueError('wrong feature')

            size = self.point_size ** 2 if size == 1 else self.point_size ** 2 * size

            plot_para_dict = {'xlabel': 'S1000 spatial 1', 'ylabel': 'S1000 spatial 2',
                              'show_ticks_and_labels': True, 'shrink': 0.4, 'pad': 0.05}

            if para_dict:
                plot_para_dict = self._change_para_dict(plot_para_dict, para_dict)

            if not low_pic:
                plot_data['__x'] = plot_data['__x'] * self.scalar
                plot_data['__y'] = plot_data['__y'] * self.scalar

            else:
                plot_data['__x'] = plot_data['__x'] * self.low_scalar
                plot_data['__y'] = plot_data['__y'] * self.low_scalar

            if crop_coord:
                plot_pic, plot_data = self._crop_coord(plot_data=plot_data, low_pic=low_pic, crop_coord=crop_coord)
            else:
                plot_pic = self._low_pic if low_pic else self._pic

            if interactive or run_dash:
                fig = SpatialApp.interact_pic_continuous(plot_data=plot_data,
                                                         pic=plot_pic,
                                                         feature=prob[0],
                                                         size=size,
                                                         cmap=cmap,
                                                         to_save=to_save,
                                                         pic_only=pic_only,
                                                         figsize=figsize,
                                                         draw_pic=draw_pic)

                return fig

            fig, ax = plt.subplots(constrained_layout=True, figsize=figsize)

            start = 0

            for feature in prob:
                if len(prob) > 1:
                    grid_dim = self._facet_pos(length=len(prob), ncol=ncol)
                    ax = plt.subplot2grid(grid_dim, self._facet_pos_list[start])
                    plt.tight_layout()
                    start += 1

                if alpha_map_to_value:
                    from sklearn.preprocessing import MinMaxScaler
                    scalar_alpha = MinMaxScaler(feature_range=(0, 1))
                    alpha = [i[0] for i in scalar_alpha.fit_transform(pd.DataFrame(np.array(plot_data[feature])))]

                if value_limits:
                    from sklearn.preprocessing import MinMaxScaler
                    scalar_value = MinMaxScaler(feature_range=value_limits)
                    value = [i[0] for i in scalar_value.fit_transform(pd.DataFrame(np.array(plot_data[feature])))]
                else:
                    value = plot_data[feature]

                plt.scatter(x=plot_data['__x'],
                            y=plot_data['__y'],
                            alpha=alpha,
                            s=size, cmap=cmap,
                            c=value)

                plt.title(feature)
                plt.xlabel(plot_para_dict['xlabel'])
                plt.ylabel(plot_para_dict['ylabel'])
                plt.colorbar(shrink=float(plot_para_dict['shrink']), pad=float(plot_para_dict['pad']))

                if draw_pic:
                    plt.imshow(plot_pic)
                else:
                    plt.gca().invert_yaxis()

                if not plot_para_dict['show_ticks_and_labels'] or plot_para_dict['show_ticks_and_labels'] == 'False':
                    plt.xticks([])
                    plt.yticks([])
                    ax.xaxis.set_ticklabels([])
                    ax.yaxis.set_ticklabels([])

                if wspace:
                    plt.subplots_adjust(hspace=float(wspace))
                if hspace:
                    plt.subplots_adjust(hspace=float(hspace))

        if to_save:
            self._plot_save(fig, to_save=to_save)

        if return_fig and return_table:
            return fig, plot_data

        if return_fig:
            return fig

        if return_table:
            return plot_data


if __name__ == '__main__':
    desc = """
    Version: Version beta v0.8
    Contact: zhangjm <zhangjm@biomarker.com.cn>
    Program Date: 2022.10.25
    Description: spatial tools
    """

    parser = argparse.ArgumentParser(description=desc, formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('--pic', type=str, help='seurat_obj')
    parser.add_argument('--barcodes_pos', type=str, help='barcodes pos')
    parser.add_argument('--adata', type=str, help='pd.DataFrame or AnnData')
    parser.add_argument('--color', type=str, help='seurat_clusters')
    parser.add_argument('--feature', type=str, help='feature', default=None)
    parser.add_argument('--groups', type=str, help='groups', default=None)
    parser.add_argument('--size', type=float, help='dot size', default=1)
    parser.add_argument('--alpha', type=float, help='alpha', default=1)
    parser.add_argument('--figsize', type=str, help='figsize', default='(10, 10)')
    parser.add_argument('--to_save', type=str, help='to_save', default=None)
    parser.add_argument('--darken', type=float, help='darken the color', default=None)
    parser.add_argument('--return_fig', type=bool, help='return_fig', default=False)
    parser.add_argument('--return_table', type=bool, help='return_table', default=False)
    parser.add_argument('--split', type=bool, help='colnames of groups', default=False)
    parser.add_argument('--ncol', type=int, help='ncol', default=2)
    parser.add_argument('--color_dict', type=str, help='color_dict', default=None)
    parser.add_argument('--hspace', type=float, help='hspace', default=None)
    parser.add_argument('--wspace', type=float, help='wspace', default=None)
    parser.add_argument('--para_dict', type=str, help='para_dict', default=None)
    input_args = parser.parse_args()

    st_data = SpatialTools(pic=input_args.pic, barcodes_pos=input_args.barcodes_pos)

    if input_args.groups:
        input_args.groups = st_data.resolve_para_to_list_tuple_dict(input_args.groups, list, str)

    if input_args.figsize:
        input_args.figsize = st_data.resolve_para_to_list_tuple_dict(input_args.figsize, tuple, float)

    if input_args.feature:
        input_args.feature = st_data.resolve_para_to_list_tuple_dict(input_args.feature, list, str)

    if input_args.color_dict:
        input_args.color_dict = st_data.resolve_para_to_list_tuple_dict(input_args.color_dict, dict)

    if input_args.para_dict:
        input_args.para_dict = st_data.resolve_para_to_list_tuple_dict(input_args.para_dict, dict)

    logging.info('input args: {}'.format(input_args))

    if str(input_args.adata).endswith('.xls'):
        logging.info('reading xls')
        adata = pd.read_csv(input_args.adata, sep='\t')
        if 'barcode' not in adata.columns:
            raise ValueError('xls file must contains barcode column')
        else:
            adata.index = adata['barcode']
            adata.index.name = None

    elif str(input_args.adata).endswith('.loom'):
        logging.info('reading loom file ...')
        adata = sc.read_loom(input_args.adata)

    else:
        raise ValueError('wrong adata args!')

    logging.info('plotting ...')
    st_data.s1000_spatial_plot(
        adata=adata,
        color=input_args.color,
        groups=input_args.groups,
        size=input_args.size,
        alpha=input_args.alpha,
        figsize=input_args.figsize,
        to_save=input_args.to_save,
        darken=input_args.darken,
        return_fig=input_args.return_fig,
        return_table=input_args.return_table,
        feature=input_args.feature,
        split=input_args.split,
        ncol=input_args.ncol,
        color_dict=input_args.color_dict,
        hspace=input_args.hspace,
        wspace=input_args.wspace,
        para_dict=input_args.para_dict)

    logging.info('done!')
