#!/usr/bin/env python
####################################################################################################
# NAME
#    <NAME> - contain graphical utility functions for charts
#
# SYNOPSIS
#    <NAME>
#
# AUTHOR
#    Written by Florian Barras (florian@barras.io).
#
# COPYRIGHT
#    Copyright © 2013-2022 Florian Barras <https://barras.io>.
#    The MIT License (MIT) <https://opensource.org/licenses/MIT>.
####################################################################################################

import io

import matplotlib.figure as mfigure
import matplotlib.pyplot as mplot
import matplotlib.ticker as mticker
import plotly.express as px
import plotly.graph_objs as go
import plotly.io as pio
import plotly.subplots as sp
import plotly.tools as tls

import ngui.web as web
from ngui.image import *
from nutil.math import *

####################################################################################################
# CHART SETTINGS
####################################################################################################

pio.renderers.default = 'browser'

####################################################################################################
# CHART CONSTANTS
####################################################################################################

__CHART_CONSTANTS___________________________________ = ''

# The default tick length
DEFAULT_TICK_LENGTH = 4

# The default tick direction
DEFAULT_TICK_DIRECTION = 'outside'

##################################################

MAP_PROJECTIONS = [
	'equirectangular', 'mercator', 'orthographic', 'natural earth', 'kavrayskiy7', 'miller',
	'robinson', 'eckert4', 'azimuthal equal area', 'azimuthal equidistant', 'conic equal area',
	'conic conformal', 'conic equidistant', 'gnomonic', 'stereographic', 'mollweide', 'hammer',
	'transverse mercator', 'albers usa', 'winkel tripel', 'aitoff', 'sinusoidal'
]

####################################################################################################
# CHART FUNCTIONS
####################################################################################################

__CHART___________________________________________ = ''


def is_matplot(fig):
	return isinstance(fig, mfigure.Figure)


def is_plotly(fig):
	return isinstance(fig, go._figure.Figure)


#########################

def is_multi_plot(fig):
	return not is_null(fig._grid_ref)


##################################################

def get_grid_size(n, row_count=None, col_count=None):
	if is_collection(n):
		n = max(1, count_cols(n))
	if is_null(col_count):
		col_count = round_to_int(sqrt(n))
	if is_null(row_count):
		row_count = ceil(n / col_count)
	return row_count, col_count


def get_hover_template(index):
	if not is_empty(index):
		return collapse('<b>%{customdata}</b><br />',
		                '<b>x:</b> %{x}<br />',
		                '<b>y:</b> %{y}')
	return collapse('<b>x:</b> %{x}<br />',
	                '<b>y:</b> %{y}')


def get_label(data, transformation=None, yaxis=0,
              show_date=False, show_name=True):
	if is_null(data):
		return ''
	yaxis = '(' + str(yaxis) + ')' if yaxis != 0 else ''
	if show_date and is_time_series(data):
		date_from = get_first(data.index)
		date_to = get_last(data.index)
		year_from = date_from.year if not is_null(date_from) else None
		year_to = date_to.year if not is_null(date_to) else None
		if is_any_null(year_from, year_to):
			date_range = ''
		elif year_from != year_to:
			date_range = collapse(year_from, '-', year_to)
		else:
			date_range = year_from
	else:
		date_range = ''
	if show_name and not is_empty(data):
		name = get_names(data)[0] if is_collection(data) else data
		name = str(name).title() if not is_null(name) else ''
	else:
		name = ''
	transformation = transformation.value.title() if not is_null(transformation) else ''
	return paste(yaxis, date_range, name, transformation)


def get_margin(x, fig=None, has_title=False, has_title_x=False, has_title_y=False):
	'''Returns the margin with the specified ratio to the width or height.'''
	if not is_null(fig) and not is_empty(fig._layout_obj.annotations):
		has_title |= (not is_empty(fig._layout_obj.title.text) or
		              any(a.yanchor in ('bottom', 'top') for a in fig._layout_obj.annotations))
		has_title_x |= (not is_empty(fig._layout_obj.xaxis.title.text) or
		                any(a.yanchor in ('bottom', 'top') for a in fig._layout_obj.annotations))
		has_title_y |= (not is_empty(fig._layout_obj.yaxis.title.text) or
		                any(a.xanchor in ('left', 'right') for a in fig._layout_obj.annotations))
	if is_null(x):
		x = {}
	if is_dict(x):
		for k in ('l', 'r', 'b', 't'):
			if k not in x:
				x[k] = (DEFAULT_MARGIN_WITH_TITLE[k] if (has_title and k == 't' or
				                                         has_title_x and k == 'b' or
				                                         has_title_y and k in ('l', 'r')) else
				        DEFAULT_MARGIN[k])
		return x
	return dict(l=x, r=x, b=x, t=x)


##################################################

def matplot_to_plotly(fig, resize=False, strip_style=False, verbose=VERBOSE):
	for ax in fig.axes:
		ax.xaxis._gridOnMajor = ax.xaxis._major_tick_kw['gridOn']
		ax.yaxis._gridOnMajor = ax.yaxis._major_tick_kw['gridOn']
		for collection in ax.collections:
			collection.get_offset_position = lambda: 'screen'
		for _, spine in ax.spines.items():
			spine.is_frame_like = lambda: False
	return tls.mpl_to_plotly(fig, resize=resize, strip_style=strip_style, verbose=verbose)


#########################

def fig_to_image(fig, format,
                 scale=DEFAULT_SCALE,
                 width=DEFAULT_WIDTH, height=DEFAULT_HEIGHT, margin=None):
	'''Converts the specified figure to an image buffer with the specified format.'''
	update_layout_size(fig, width=width, height=height, margin=margin)
	if is_matplot(fig):
		buffer = io.BytesIO()
		fig.savefig(buffer, format=format, dpi=scale * 100)
		buffer.seek(0)
		return buffer.read()
	elif is_plotly(fig):
		return pio.to_image(fig, format=format, scale=scale, width=width, height=height)


def fig_to_jpg(fig,
               scale=DEFAULT_SCALE,
               width=DEFAULT_WIDTH, height=DEFAULT_HEIGHT, margin=None):
	'''Converts the specified figure to a JPEG image.'''
	return fig_to_image(fig, JPEG_FORMAT, scale=scale, width=width, height=height, margin=margin)


def fig_to_png(fig,
               scale=DEFAULT_SCALE,
               width=DEFAULT_WIDTH, height=DEFAULT_HEIGHT, margin=None):
	'''Converts the specified figure to a PNG image.'''
	return fig_to_image(fig, PNG_FORMAT, scale=scale, width=width, height=height, margin=margin)


def fig_to_svg(fig,
               scale=DEFAULT_SCALE,
               width=DEFAULT_WIDTH, height=DEFAULT_HEIGHT, margin=None):
	'''Converts the specified figure to an SVG image.'''
	return fig_to_image(fig, SVG_FORMAT, scale=scale, width=width, height=height, margin=margin)


def fig_to_webp(fig,
                scale=DEFAULT_SCALE,
                width=DEFAULT_WIDTH, height=DEFAULT_HEIGHT, margin=None):
	'''Converts the specified figure to a WebP image.'''
	return fig_to_image(fig, WEBP_FORMAT, scale=scale, width=width, height=height, margin=margin)


#########################

def fig_to_html(fig, full=True,
                width=DEFAULT_WIDTH, height=DEFAULT_HEIGHT, margin=None):
	'''Converts the specified figure to HTML.'''
	if is_null(fig):
		return ''
	update_layout_size(fig, width=width, height=height, margin=margin)
	return pio.to_html(fig, full_html=full, default_width=width, default_height=height)


def fig_to_image_html(fig, format, encoding=DEFAULT_ENCODING, mode=DEFAULT_IMAGE_MODE, style=None,
                      rotate=False, scale=DEFAULT_SCALE,
                      width=DEFAULT_WIDTH, height=DEFAULT_HEIGHT, margin=None):
	'''Converts the specified figure to the specified format, encodes it to Base64 and returns its
	HTML code.'''
	if is_null(fig):
		return ''
	image = fig_to_image(fig, format, scale=scale, width=width, height=height, margin=margin)
	return image_to_html(image, format, encoding=encoding, mode=mode, style=style,
	                     rotate=rotate,
	                     width=width, height=height)


def fig_to_jpg_html(fig, encoding=DEFAULT_ENCODING, style=None,
                    rotate=False, scale=DEFAULT_SCALE,
                    width=DEFAULT_WIDTH, height=DEFAULT_HEIGHT, margin=None):
	'''Converts the specified figure to a JPEG image, encodes it to Base64 and returns its HTML
	code.'''
	return fig_to_image_html(fig, JPEG_FORMAT, encoding=encoding, style=style,
	                         rotate=rotate, scale=scale,
	                         width=width, height=height, margin=margin)


def fig_to_png_html(fig, encoding=DEFAULT_ENCODING, style=None,
                    rotate=False, scale=DEFAULT_SCALE,
                    width=DEFAULT_WIDTH, height=DEFAULT_HEIGHT, margin=None):
	'''Converts the specified figure to a PNG image, encodes it to Base64 and returns its HTML
	code.'''
	return fig_to_image_html(fig, PNG_FORMAT, encoding=encoding, style=style,
	                         rotate=rotate, scale=scale,
	                         width=width, height=height, margin=margin)


def fig_to_svg_html(fig, encoding=DEFAULT_ENCODING, style=None,
                    rotate=False, scale=DEFAULT_SCALE,
                    width=DEFAULT_WIDTH, height=DEFAULT_HEIGHT, margin=None):
	'''Converts the specified figure to an SVG image, encodes it to Base64 and returns its HTML
	code.'''
	return fig_to_image_html(fig, SVG_FORMAT, encoding=encoding, style=style,
	                         rotate=rotate, scale=scale,
	                         width=width, height=height, margin=margin)


def fig_to_webp_html(fig, encoding=DEFAULT_ENCODING, style=None,
                     rotate=False, scale=DEFAULT_SCALE,
                     width=DEFAULT_WIDTH, height=DEFAULT_HEIGHT, margin=None):
	'''Converts the specified figure to a WEBP image, encodes it to Base64 and returns its HTML
	code.'''
	return fig_to_image_html(fig, WEBP_FORMAT, encoding=encoding, style=style,
	                         rotate=rotate, scale=scale,
	                         width=width, height=height, margin=margin)


##################################################

def create_figure(auto_size=True,
                  axis_color='black', axis_width=DEFAULT_LINE_WIDTH,
                  bar_mode=None,
                  bg_color=DEFAULT_BG_COLOR,
                  font_size=DEFAULT_FONT_SIZE,
                  grid_color='lightgray', grid_width=1,
                  label_color='black', label_size=None,
                  legend_bg_color=DEFAULT_BG_COLOR, legend_x=0.01, legend_y=0.99,
                  range_to_zero_x=False, range_to_zero_y=False, range_to_zero_y2=False,
                  show_grid_x=True, show_grid_y=True, show_grid_y2=True, show_spine=True,
                  show_title=True, show_zero_line=True,
                  tick_color='black', tick_direction=DEFAULT_TICK_DIRECTION,
                  tick_length=DEFAULT_TICK_LENGTH,
                  tick_number_x=None, tick_number_y=None, tick_number_y2=None,
                  tick_start_x=None, tick_start_y=None, tick_start_y2=None,
                  tick_step_x=None, tick_step_y=None, tick_step_y2=None,
                  tick_values_x=None, tick_values_y=None, tick_values_y2=None,
                  title=None, title_x=None, title_y=None, title_y2=None,
                  width=DEFAULT_WIDTH, height=DEFAULT_HEIGHT, margin=None,
                  zero_line_color='darkgray', zero_line_width=DEFAULT_LINE_WIDTH):
	fig = go.Figure()
	update_layout(fig,
	              auto_size=auto_size,
	              axis_color=axis_color, axis_width=axis_width,
	              bar_mode=bar_mode,
	              bg_color=bg_color,
	              font_size=font_size,
	              grid_color=grid_color, grid_width=grid_width,
	              label_color=label_color, label_size=label_size,
	              legend_bg_color=legend_bg_color, legend_x=legend_x, legend_y=legend_y,
	              range_to_zero_x=range_to_zero_x, range_to_zero_y=range_to_zero_y,
	              range_to_zero_y2=range_to_zero_y2,
	              show_grid_x=show_grid_x, show_grid_y=show_grid_y, show_grid_y2=show_grid_y2,
	              show_spine=show_spine, show_title=show_title, show_zero_line=show_zero_line,
	              tick_color=tick_color, tick_direction=tick_direction, tick_length=tick_length,
	              tick_number_x=tick_number_x, tick_number_y=tick_number_y,
	              tick_number_y2=tick_number_y2,
	              tick_start_x=tick_start_x, tick_start_y=tick_start_y, tick_start_y2=tick_start_y2,
	              tick_step_x=tick_step_x, tick_step_y=tick_step_y, tick_step_y2=tick_step_y2,
	              tick_values_x=tick_values_x, tick_values_y=tick_values_y,
	              tick_values_y2=tick_values_y2,
	              title=title, title_x=title_x, title_y=title_y, title_y2=title_y2,
	              width=width, height=height, margin=margin,
	              zero_line_color=zero_line_color, zero_line_width=zero_line_width)
	return fig


def create_figures(row_count, col_count,
                   share_x=False, share_y=False,
                   auto_size=True,
                   axis_color='black', axis_width=DEFAULT_LINE_WIDTH,
                   bar_mode=None,
                   bg_color=DEFAULT_BG_COLOR,
                   font_size=DEFAULT_FONT_SIZE,
                   grid_color='lightgray', grid_width=1,
                   label_color='black', label_size=None,
                   legend_bg_color=DEFAULT_BG_COLOR, legend_x=0.01, legend_y=0.99,
                   range_to_zero_x=False, range_to_zero_y=False,
                   show_grid_x=True, show_grid_y=True, show_spine=True,
                   show_title=True, show_zero_line=True,
                   tick_color='black', tick_direction=DEFAULT_TICK_DIRECTION,
                   tick_length=DEFAULT_TICK_LENGTH,
                   tick_number_x=None, tick_number_y=None,
                   tick_start_x=None, tick_start_y=None,
                   tick_step_x=None, tick_step_y=None,
                   tick_values_x=None, tick_values_y=None,
                   title=None, subtitles=None, title_x=None, title_y=None,
                   width=DEFAULT_WIDTH, height=DEFAULT_HEIGHT, margin=None,
                   zero_line_color='darkgray', zero_line_width=DEFAULT_LINE_WIDTH):
	margin = get_margin(margin, has_title=not is_empty(title) or not is_empty(subtitles),
	                    has_title_x=not is_empty(title_x), has_title_y=not is_empty(title_y))
	fig = sp.make_subplots(rows=row_count, cols=col_count,
	                       shared_xaxes=share_x, shared_yaxes=share_y,
	                       subplot_titles=apply(subtitles, to_string),
	                       x_title=title_x, y_title=title_y)
	update_layout(fig,
	              auto_size=auto_size,
	              axis_color=axis_color, axis_width=axis_width,
	              bar_mode=bar_mode,
	              bg_color=bg_color,
	              font_size=font_size,
	              grid_color=grid_color, grid_width=grid_width,
	              label_color=label_color, label_size=label_size,
	              legend_bg_color=legend_bg_color, legend_x=legend_x, legend_y=legend_y,
	              range_to_zero_x=range_to_zero_x, range_to_zero_y=range_to_zero_y,
	              show_grid_x=show_grid_x, show_grid_y=show_grid_y,
	              show_spine=show_spine, show_title=show_title, show_zero_line=show_zero_line,
	              tick_color=tick_color, tick_direction=tick_direction, tick_length=tick_length,
	              tick_number_x=tick_number_x, tick_number_y=tick_number_y,
	              tick_start_x=tick_start_x, tick_start_y=tick_start_y,
	              tick_step_x=tick_step_x, tick_step_y=tick_step_y,
	              tick_values_x=tick_values_x, tick_values_y=tick_values_y,
	              title=title, title_x=None, title_y=None,
	              width=width, height=height, margin=margin,
	              zero_line_color=zero_line_color, zero_line_width=zero_line_width)
	return fig


#########################

def create_choropleth_map(df, loc_col, label_col, loc_mode='ISO-3', label_name=None,
                          # Layout
                          title=None, dragmode=False, showframe=False,
                          colors=get_RYG(), range_color=None,
                          width=DEFAULT_WIDTH, height=DEFAULT_HEIGHT, margin=None,
                          # Geos
                          lat=None, lon=None,
                          projection='miller',
                          range_mode='auto', lataxis_range=None, lonaxis_range=None,
                          resolution=50,
                          showcoastlines=True, coastlinecolor='Black',
                          showland=False, landcolor='LightGreen',
                          showocean=True, oceancolor='AliceBlue',
                          showlakes=False, lakecolor='Blue',
                          showrivers=False, rivercolor='Blue'):
	'''Creates a choropleth map with the specified parameters.'''
	fig = px.choropleth(data_frame=df,
	                    lat=lat, lon=lon,
	                    locations=loc_col, locationmode=loc_mode, projection=projection,
	                    labels={label_col: label_name if not is_null(label_name) else label_col},
	                    color=label_col, range_color=range_color,
	                    color_continuous_scale=colors, color_discrete_sequence=colors)
	update_layout(fig, title=title, width=width, height=height, margin=margin)
	fig.update_layout(clickmode='event+select', dragmode=dragmode, hovermode='closest')
	if range_mode == 'auto':
		if is_null(projection) or projection in ('equirectangular', 'kavrayskiy7', 'sinusoidal'):
			lataxis_range = [-48, 63]
		elif projection == 'aitoff':
			lataxis_range = [-39, 63]
		elif projection == 'eckert4':
			lataxis_range = [-50, 59]
		elif projection == 'hammer':
			lataxis_range = [-42, 61]
		elif projection == 'mercator':
			lataxis_range = [-35, 71]
		elif projection == 'miller':
			lataxis_range = [-43, 68]
		elif projection == 'mollweide':
			lataxis_range = [-50, 61]
		elif projection == 'natural earth' or projection == 'robinson':
			lataxis_range = [-49, 62]
		elif projection == 'winkel tripel':
			lataxis_range = [-44, 64]
	fig.update_geos(
		lataxis_range=lataxis_range,
		lonaxis_range=lonaxis_range,
		resolution=resolution,
		showframe=showframe,
		showcoastlines=showcoastlines, coastlinecolor=coastlinecolor,
		showland=showland, landcolor=landcolor,
		showocean=showocean, oceancolor=oceancolor,
		showlakes=showlakes, lakecolor=lakecolor,
		showrivers=showrivers, rivercolor=rivercolor)
	return fig


##################################################

def draw(x, y=None,
         # Chart
         color=None, dash=None, fill='none', index=None, line_width=DEFAULT_LINE_WIDTH,
         marker_size=DEFAULT_MARKER_SIZE, mode='lines', name=None, opacity=1, stackgroup=None,
         yaxis=0,
         # Flags
         show_date=False, show_legend=True, show_name=True):
	data = x
	if is_null(y):
		x = to_array(get_index(data))
		y = get_values(data)
	elif is_null(index) and is_frame(data):
		index = to_array(get_index(data))
	if is_null(name):
		name = get_name(data)
	name = get_label(name, yaxis=yaxis, show_date=show_date, show_name=show_name)
	hover_template = get_hover_template(index)
	line = dict(color=color, dash=dash, width=line_width)
	marker = dict(color=color, size=marker_size)
	if mode == 'lines':
		marker = None
	elif mode == 'markers':
		line = None
	return go.Scatter(x=x, y=y,
	                  # Chart
	                  customdata=index, hovertemplate=hover_template, fill=fill, line=line,
	                  marker=marker, mode=mode, name=name, opacity=opacity, stackgroup=stackgroup,
	                  yaxis='y' + str(1 if yaxis == 0 else yaxis),
	                  # Flags
	                  showlegend=show_legend)


def draw_ellipse(center, a, b, angle=0, precision=100,
                 # Chart
                 color=None, dash=None, fill='none', index=None, line_width=DEFAULT_LINE_WIDTH,
                 marker_size=DEFAULT_MARKER_SIZE, mode='lines', name=None, opacity=1, yaxis=0,
                 # Flags
                 show_date=False, show_legend=True, show_name=True):
	X, Y = create_ellipse(center, a, b, angle=angle, precision=precision)
	return draw(x=X, y=Y,
	            # Chart
	            color=color, dash=dash, fill=fill, index=index, line_width=line_width,
	            marker_size=marker_size, mode=mode, name=name, opacity=opacity, yaxis=yaxis,
	            # Flags
	            show_date=show_date, show_legend=show_legend, show_name=show_name)


def draw_series(series, *args, f=None,
                # Chart
                color=None, dash=None, fill='none', index=None, line_width=DEFAULT_LINE_WIDTH,
                marker_size=DEFAULT_MARKER_SIZE, mode='lines', name=None, opacity=1,
                stackgroup=None, yaxis=0,
                # Flags
                show_date=False, show_legend=True, show_name=True, **kwargs):
	if not is_null(f):
		series = f(series, *args, **kwargs)
	return draw(series,
	            # Chart
	            color=color, dash=dash, fill=fill, index=index, line_width=line_width,
	            marker_size=marker_size, mode=mode, name=name, opacity=opacity,
	            stackgroup=stackgroup, yaxis=yaxis,
	            # Flags
	            show_date=show_date, show_legend=show_legend, show_name=show_name)


#########################

def plot_multi(df, draw, *args,
               # Figure
               fig=None, row_count=None, col_count=None,
               share_x=True, share_y=True,
               title=None, subtitles=None, title_x=None, title_y=None,
               width=DEFAULT_WIDTH, height=DEFAULT_HEIGHT, margin=None,
               # Chart
               colors=DEFAULT_COLORS, **kwargs):
	row_count, col_count = get_grid_size(df, row_count=row_count, col_count=col_count)
	if is_null(fig):
		if is_null(subtitles):
			subtitles = get_names(df)
		fig = create_figures(row_count, col_count,
		                     share_x=share_x, share_y=share_y,
		                     title=title, subtitles=subtitles, title_x=title_x, title_y=title_y,
		                     width=width, height=height, margin=margin)
	colors = get_iterator(to_list(colors), cycle=True)

	# Get the number of series
	series_count = count_cols(df)

	for i in range(row_count):
		for j in range(col_count):
			series_index = i * col_count + j
			if series_index < series_count:
				fig.add_trace(draw(get_col(df, series_index), *args, color=next(colors), **kwargs),
				              row=i + 1, col=j + 1)
	return fig


def plot_series(series, *args, f=None,
                # Figure
                fig=None, title=None, title_x=None, title_y=None, title_y2=None,
                width=DEFAULT_WIDTH, height=DEFAULT_HEIGHT, margin=None,
                # Chart
                colors=DEFAULT_COLORS, dash=None, fill='none', index=None,
                line_width=DEFAULT_LINE_WIDTH, marker_size=DEFAULT_MARKER_SIZE, mode='lines',
                name=None, opacity=1, stackgroup=None, yaxis=0,
                # Flags
                show_date=False, show_legend=True, show_name=True, **kwargs):
	if is_null(fig):
		fig = create_figure(title=title, title_x=title_x, title_y=title_y, title_y2=title_y2,
		                    width=width, height=height, margin=margin)
	colors = get_iterator(to_list(colors), cycle=True)

	for s in to_series(series) if is_frame(series) else [series]:
		fig.add_trace(draw_series(s,
		                          *args, f=f,
		                          # Chart
		                          color=next(colors), dash=dash, fill=fill, index=index,
		                          line_width=line_width, marker_size=marker_size, mode=mode,
		                          name=name, opacity=opacity, stackgroup=stackgroup, yaxis=yaxis,
		                          # Flags
		                          show_date=show_date, show_legend=show_legend, show_name=show_name,
		                          **kwargs))
	return fig


def plot_multi_series(df, *args, f=None,
                      # Figure
                      fig=None, row_count=None, col_count=None, share_x=True, share_y=True,
                      title=None, subtitles=None, title_x=None, title_y=None,
                      width=DEFAULT_WIDTH, height=DEFAULT_HEIGHT, margin=None,
                      # Chart
                      colors=DEFAULT_COLORS, dash=None, fill='none', index=None,
                      line_width=DEFAULT_LINE_WIDTH, marker_size=DEFAULT_MARKER_SIZE, mode='lines',
                      opacity=1, stackgroup=None,
                      # Flags
                      show_date=False, show_legend=False, show_name=True, **kwargs):
	return plot_multi(df, draw_series,
	                  *args, f=f,
	                  # Figure
	                  fig=fig, row_count=row_count, col_count=col_count,
	                  share_x=share_x, share_y=share_y,
	                  title=title, subtitles=subtitles, title_x=title_x, title_y=title_y,
	                  width=width, height=height, margin=margin,
	                  # Chart
	                  colors=colors, dash=dash, fill=fill, index=index, line_width=line_width,
	                  marker_size=marker_size, mode=mode, opacity=opacity, stackgroup=stackgroup,
	                  # Flags
	                  show_date=show_date, show_legend=show_legend, show_name=show_name, **kwargs)


def plot_ellipse(center, a, b, angle=0, precision=100,
                 # Figure
                 fig=None, title=None, title_x=None, title_y=None, title_y2=None,
                 width=DEFAULT_WIDTH, height=DEFAULT_HEIGHT, margin=None,
                 # Chart
                 color=None, dash=None, fill='none', index=None, line_width=DEFAULT_LINE_WIDTH,
                 marker_size=DEFAULT_MARKER_SIZE, mode='lines', name=None, opacity=1, yaxis=0,
                 # Flags
                 show_axes=True, show_date=False, show_legend=True, show_name=True):
	if is_null(fig):
		fig = create_figure(title=title, title_x=title_x, title_y=title_y, title_y2=title_y2,
		                    width=width, height=height, margin=margin)
	fig.add_trace(draw_ellipse(center, a, b, angle=angle, precision=precision,
	                           # Chart
	                           color=color, dash=dash, fill=fill, index=index,
	                           line_width=line_width, marker_size=marker_size, mode=mode, name=name,
	                           opacity=opacity, yaxis=yaxis,
	                           # Flags
	                           show_date=show_date, show_legend=show_legend, show_name=show_name))
	if show_axes:
		fig.add_trace(draw([center[0] - a * cos(angle), center[0] + a * cos(angle)],
		                   [center[1] - a * sin(angle), center[1] + a * sin(angle)],
		                   # Chart
		                   color=color, dash=dash, line_width=line_width, marker_size=marker_size,
		                   name=name, opacity=opacity,
		                   # Flags
		                   show_legend=False))
		fig.add_trace(draw([center[0] - b * sin(angle), center[0] + b * sin(angle)],
		                   [center[1] + b * cos(angle), center[1] - b * cos(angle)],
		                   # Chart
		                   color=color, dash=dash, line_width=line_width, marker_size=marker_size,
		                   name=name, opacity=opacity,
		                   # Flags
		                   show_legend=False))
	return fig


#########################

def update_layout(fig,
                  auto_size=True,
                  axis_color='black', axis_width=DEFAULT_LINE_WIDTH,
                  bar_mode=None,
                  bg_color=DEFAULT_BG_COLOR,
                  font_size=DEFAULT_FONT_SIZE,
                  grid_color='lightgray', grid_width=1,
                  label_color='black', label_size=None,
                  legend_bg_color=DEFAULT_BG_COLOR, legend_x=0.01, legend_y=0.99,
                  range_to_zero_x=False, range_to_zero_y=False, range_to_zero_y2=False,
                  show_grid_x=True, show_grid_y=True, show_grid_y2=True, show_spine=True,
                  show_title=True, show_zero_line=True,
                  tick_color='black', tick_direction=DEFAULT_TICK_DIRECTION,
                  tick_length=DEFAULT_TICK_LENGTH,
                  tick_number_x=None, tick_number_y=None, tick_number_y2=None,
                  tick_start_x=None, tick_start_y=None, tick_start_y2=None,
                  tick_step_x=None, tick_step_y=None, tick_step_y2=None,
                  tick_values_x=None, tick_values_y=None, tick_values_y2=None,
                  title=None, title_x=None, title_y=None, title_y2=None,
                  width=DEFAULT_WIDTH, height=DEFAULT_HEIGHT, margin=None,
                  zero_line_color='darkgray', zero_line_width=DEFAULT_LINE_WIDTH):
	margin = get_margin(margin, fig=fig, has_title=not is_empty(title),
	                    has_title_x=not is_empty(title_x), has_title_y=not is_empty(title_y))
	update_layout_plot(fig, auto_size=auto_size, bar_mode=bar_mode, bg_color=bg_color,
	                   font_size=font_size, show_title=show_title, title=title)
	update_layout_axes(fig,
	                   axis_color=axis_color, axis_width=axis_width,
	                   grid_color=grid_color, grid_width=grid_width,
	                   label_color=label_color, label_size=label_size,
	                   range_to_zero_x=range_to_zero_x, range_to_zero_y=range_to_zero_y,
	                   range_to_zero_y2=range_to_zero_y2,
	                   show_grid_x=show_grid_x, show_grid_y=show_grid_y, show_grid_y2=show_grid_y2,
	                   show_spine=show_spine, show_zero_line=show_zero_line,
	                   tick_color=tick_color, tick_direction=tick_direction,
	                   tick_length=tick_length,
	                   tick_number_x=tick_number_x, tick_number_y=tick_number_y,
	                   tick_number_y2=tick_number_y2,
	                   tick_start_x=tick_start_x, tick_start_y=tick_start_y,
	                   tick_start_y2=tick_start_y2,
	                   tick_step_x=tick_step_x, tick_step_y=tick_step_y,
	                   tick_step_y2=tick_step_y2,
	                   tick_values_x=tick_values_x, tick_values_y=tick_values_y,
	                   tick_values_y2=tick_values_y2,
	                   title_x=title_x, title_y=title_y, title_y2=title_y2,
	                   zero_line_color=zero_line_color, zero_line_width=zero_line_width)
	update_layout_legend(fig, bg_color=legend_bg_color, x=legend_x, y=legend_y)
	update_layout_size(fig, width=width, height=height, margin=margin)


def update_layout_plot(fig, auto_size=True, bar_mode=None, bg_color=DEFAULT_BG_COLOR,
                       font_size=DEFAULT_FONT_SIZE, show_title=True, title=None):
	if is_matplot(fig):
		for ax in fig.axes:
			if not is_null(bg_color):
				ax.set_facecolor(bg_color)
			if not is_null(title) or not show_title:
				ax.set_title(title if show_title else None)
	elif is_plotly(fig):
		fig.update_annotations(font_size=font_size)
		bg_color = format_rgb_color(bg_color)
		if not is_null(title) or not show_title:
			fig.update_layout(title=web.b(title) if show_title else None)
		if not is_null(bar_mode):
			fig.update_layout(barmode=bar_mode)
		fig.update_layout(autosize=auto_size, paper_bgcolor=bg_color, plot_bgcolor=bg_color)


def update_layout_axes(fig,
                       axis_color='black', axis_width=DEFAULT_LINE_WIDTH,
                       grid_color='lightgray', grid_width=1,
                       label_color='black', label_size=None,
                       range_to_zero_x=False, range_to_zero_y=False, range_to_zero_y2=False,
                       scale_ratio_y=None, scale_ratio_y2=None,
                       show_grid_x=True, show_grid_y=True, show_grid_y2=True, show_spine=True,
                       show_zero_line=True,
                       tick_color='black', tick_direction=DEFAULT_TICK_DIRECTION,
                       tick_length=DEFAULT_TICK_LENGTH,
                       tick_number_x=None, tick_number_y=None, tick_number_y2=None,
                       tick_start_x=None, tick_start_y=None, tick_start_y2=None,
                       tick_step_x=None, tick_step_y=None, tick_step_y2=None,
                       tick_values_x=None, tick_values_y=None, tick_values_y2=None,
                       title_x=None, title_y=None, title_y2=None,
                       zero_line_color='darkgray', zero_line_width=DEFAULT_LINE_WIDTH):
	if is_matplot(fig):
		for ax in fig.axes:
			# Set the titles
			# - Horizontal axis
			if not is_null(title_x):
				ax.set_xlabel(to_string(title_x))
			# - Vertical axis
			if not is_null(title_y):
				ax.set_ylabel(to_string(title_y))
			# Set the spines
			for _, spine in ax.spines.items():
				spine.set_color(axis_color)
				spine.set_linewidth(axis_width)
				spine.set_visible(show_spine)
			# Set the grids
			# - Horizontal axis
			if show_grid_x:
				ax.grid(axis='x', b=True, color=grid_color, linestyle='-', linewidth=grid_width)
			else:
				ax.grid(axis='x', b=False)
			# - Vertical axis
			if show_grid_y:
				ax.grid(axis='y', b=True, color=grid_color, linestyle='-', linewidth=grid_width)
			else:
				ax.grid(axis='y', b=False)
			# Set the scale
			if not is_null(scale_ratio_y):
				ax.axes.set_aspect('equal')
			# Set the ticks
			ax.tick_params(color=tick_color,
			               direction='out' if tick_direction == 'outside' else 'in',
			               labelcolor=label_color, labelsize=label_size,
			               length=tick_length, width=grid_width)
			# - Horizontal axis
			if range_to_zero_x:
				ax.set_xlim(left=0)
			if not is_null(tick_number_x):
				ax.xaxis.set_major_locator(mticker.MaxNLocator(tick_number_x))
			elif not is_null(tick_start_x):
				ax.xaxis.set_major_locator(mticker.IndexLocator(base=tick_step_x,
				                                                offset=tick_start_x))
			elif not is_null(tick_step_x):
				ax.xaxis.set_major_locator(mticker.MultipleLocator(base=tick_step_x))
			elif not is_null(tick_values_x):
				ax.set_xticks(tick_values_x)
			# - Vertical axis
			if range_to_zero_y:
				ax.set_ylim(bottom=0)
			if not is_null(tick_number_y):
				ax.yaxis.set_major_locator(mticker.MaxNLocator(tick_number_y))
			elif not is_null(tick_start_y):
				ax.yaxis.set_major_locator(mticker.IndexLocator(base=tick_step_y,
				                                                offset=tick_start_y))
			elif not is_null(tick_step_y):
				ax.yaxis.set_major_locator(mticker.MultipleLocator(base=tick_step_y))
			elif not is_null(tick_values_y):
				ax.set_yticks(tick_values_y)
	elif is_plotly(fig):
		axis_color = format_rgb_color(axis_color)
		grid_color = format_rgb_color(grid_color)
		label_color = format_rgb_color(label_color)
		tick_color = format_rgb_color(tick_color)
		zero_line_color = format_rgb_color(zero_line_color)
		# Set the titles
		# - Horizontal axis
		if not is_null(title_x):
			fig.update_xaxes(title=dict(font_color=label_color, font_size=label_size,
			                            text=to_string(title_x)))
		# - Primary vertical axis
		if not is_null(title_y):
			update_axis_y(fig, yaxis=1,
			              title=dict(font_color=label_color, font_size=label_size,
			                         text=to_string(title_y)))
		# - Secondary vertical axis
		if not is_null(title_y2):
			update_axis_y(fig, yaxis=2,
			              title=dict(font_color=label_color, font_size=label_size,
			                         text=to_string(title_y2)))
		# Set the scale
		if not is_null(scale_ratio_y):
			update_axis_y(fig, yaxis=1,
			              scaleanchor='x', scaleratio=scale_ratio_y)
		if not is_null(scale_ratio_y2):
			update_axis_y(fig, yaxis=2,
			              scaleanchor='x', scaleratio=scale_ratio_y2)
		# Set the layout
		# - Horizontal axis
		fig.update_xaxes(
			# Set the spine
			showline=show_spine, linecolor=axis_color, linewidth=axis_width,
			# Set the grid
			showgrid=show_grid_x, gridcolor=grid_color, gridwidth=grid_width,
			# Set the range
			rangemode='tozero' if range_to_zero_x else None,
			# Set the ticks
			tickmode='array' if not is_null(tick_values_x)
			else 'linear' if not is_null(tick_start_x) or not is_null(tick_step_x)
			else 'auto', nticks=tick_number_x, tick0=tick_start_x, dtick=tick_step_x,
			tickvals=tick_values_x,
			tickcolor=tick_color, ticks=tick_direction, ticklen=tick_length,
			tickwidth=grid_width,
			# Set the zero line
			zeroline=show_zero_line, zerolinecolor=zero_line_color,
			zerolinewidth=zero_line_width)
		# - Primary vertical axis
		update_axis_y(fig, yaxis=1,
		              # Set the spine
		              showline=show_spine, linecolor=axis_color, linewidth=axis_width,
		              # Set the grid
		              showgrid=show_grid_y, gridcolor=grid_color, gridwidth=grid_width,
		              # Set the range
		              rangemode='tozero' if range_to_zero_y else None,
		              # Set the ticks
		              tickmode='array' if not is_null(tick_values_y)
		              else 'linear' if not is_null(tick_start_y) or not is_null(tick_step_y)
		              else 'auto', nticks=tick_number_y, tick0=tick_start_y, dtick=tick_step_y,
		              tickvals=tick_values_y,
		              tickcolor=tick_color, ticks=tick_direction, ticklen=tick_length,
		              tickwidth=grid_width,
		              # Set the zero line
		              zeroline=show_zero_line, zerolinecolor=zero_line_color,
		              zerolinewidth=zero_line_width)
		# - Secondary vertical axis
		update_axis_y(fig, yaxis=2,
		              # Set the spine
		              showline=show_spine, linecolor=axis_color, linewidth=axis_width,
		              # Set the grid
		              showgrid=show_grid_y2, gridcolor=grid_color, gridwidth=grid_width,
		              # Set the range
		              rangemode='tozero' if range_to_zero_y2 else None,
		              # Set the ticks
		              tickmode='array' if not is_null(tick_values_y2)
		              else 'linear' if not is_null(tick_start_y2) or not is_null(tick_step_y2)
		              else 'auto', nticks=tick_number_y2, tick0=tick_start_y2, dtick=tick_step_y2,
		              tickvals=tick_values_y2,
		              tickcolor=tick_color, ticks=tick_direction, ticklen=tick_length,
		              tickwidth=grid_width,
		              # Set the zero line
		              zeroline=show_zero_line, zerolinecolor=zero_line_color,
		              zerolinewidth=zero_line_width)


def update_axis_y(fig, yaxis=0, **kwargs):
	if is_multi_plot(fig):
		if yaxis == 2:
			fig.update_yaxes(secondary_y=True, **kwargs)
		else:
			fig.update_yaxes(secondary_y=False, **kwargs)
	else:
		if yaxis == 2:
			fig.update_layout(yaxis2=dict(**kwargs))
		else:
			fig.update_layout(yaxis=dict(**kwargs))


def update_layout_legend(fig, bg_color=DEFAULT_BG_COLOR, x=0.01, y=0.99):
	if is_matplot(fig):
		for ax in fig.axes:
			handles, _ = ax.get_legend_handles_labels()
			if not is_empty(handles):
				ax.legend(facecolor=bg_color, loc='upper left', bbox_to_anchor=(x, y))
	elif is_plotly(fig):
		bg_color = format_rgb_color(bg_color)
		fig.update_layout(legend=dict(xanchor='left', x=x,
		                              yanchor='top', y=y,
		                              bgcolor=bg_color))


def update_layout_size(fig, width=DEFAULT_WIDTH, height=DEFAULT_HEIGHT, margin=None):
	margin = get_margin(margin, fig=fig)
	if is_matplot(fig):
		fig.set_size_inches(width / 100, height / 100)
		fig.subplots_adjust(left=margin['l'], right=1 - margin['r'],
		                    bottom=margin['b'], top=1 - margin['t'])
	elif is_plotly(fig):
		margin = margin.copy()
		margin['l'] *= width
		margin['r'] *= width
		margin['b'] *= height
		margin['t'] *= height
		fig.update_layout(width=width, height=height, margin=margin)
