# -*- coding: utf-8 -*-
# copyright 2013-2015 LOGILAB S.A. (Paris, FRANCE), all rights reserved.
# contact http://www.logilab.fr -- mailto:contact@logilab.fr
#
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU Lesser General Public License as published by the Free
# Software Foundation, either version 2.1 of the License, or (at your option)
# any later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU Lesser General Public License for more
# details.
#
# You should have received a copy of the GNU Lesser General Public License along
# with this program. If not, see <http://www.gnu.org/licenses/>.
"""cubicweb-leaflet views/forms/actions/components for web ui"""
import json

from logilab.mtconverter import xml_escape
from cubicweb.utils import js_dumps, make_uid, JSString
from cubicweb.predicates import multi_columns_rset, adaptable
from cubicweb.view import AnyRsetView

_ = unicode


#############################################################################
# LEAFLET OBJECT ############################################################
#############################################################################
class LeafletMap(object):
    """widget class to render leaflet map

    Typical usage is::

        leaflet_map = LeafletMap()
        self.w(leaflet_map.render(self._cw, my_list_of_markers))

    The list of markers can either a python list or a url to a json file
    """
    default_settings = {
        'divid': 'map-geo',
        'width': '940px',
        'height': '400px',
        'minZoom': 1,
        'maxZoom': 18,
        'initialZoom': 2,  # if unset, leaflet will be asked to fit all markers
        'provider': 'osm',
        'map_options': {},  # see http://leafletjs.com/reference.html#map-options
        }

    providers = {
        'osm': {
            'url': 'http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
            'attribution': (
                '&copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, '
                '<a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>'
            ),
        },
        'esri-topomap': {
            'url':
            'http://server.arcgisonline.com/ArcGIS/rest/services/World_Topo_Map/MapServer/'
            'tile/{z}/{y}/{x}',
            'attribution': ('{attribution.Esri} &mdash; Esri, DeLorme, NAVTEQ, TomTom, Intermap, '
                            'iPC, USGS, FAO, NPS, NRCAN, GeoBase, Kadaster NL, Ordnance Survey, '
                            'Esri Japan, METI, Esri China (Hong Kong), and the GIS User Community')
        },
        'esri-imagery': {
            'url':
            'http://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/'
            'tile/{z}/{y}/{x}',
            'attribution': ('{attribution.Esri} &mdash; Source: Esri, i-cubed, USDA, USGS, AEX, '
                            'GeoEye, Getmapping, Aerogrid, IGN, IGP, UPR-EGP, '
                            'and the GIS User Community')
        }
    }

    def __init__(self, custom_settings=None):
        settings = self.get_settings(custom_settings)
        if isinstance(settings['provider'], basestring):
            settings['provider'] = self.providers[settings['provider']]
        self.settings = settings

    def get_settings(self, custom_settings=None):
        settings = self.default_settings.copy()
        settings.update(custom_settings or {})
        return settings

    def render(self, req, datasource, use_cdn=True):
        req.add_js('cubes.leaflet.js')
        req.add_css('cubes.leaflet.css')
        if use_cdn:
            req.add_js('https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.3/leaflet.js',
                       localfile=False)
            req.add_css('https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.3/leaflet.css',
                        localfile=False)
        else:
            req.add_js('leaflet.js')
            req.add_css('leaflet.css')
        if self.settings.get('cluster'):
            req.add_js('leafletcluster/leaflet.markercluster.js')
            req.add_js('leafletcluster/leaflet.markercluster-src.js')
            req.add_css(('leafletcluster/MarkerCluster.css',
                         'leafletcluster/MarkerCluster.Default.css'))
        self._call_js_onload(req, datasource)
        return self.div_holder()

    def _call_js_onload(self, req, datasource):
        """ Call the JS function """
        req.add_onload("""
function initMap() {
    // this should check if your leaflet is available or wait if not.
    if (typeof L === "undefined") {
        window.setTimeout(initMap, 100);
        return;
    }
    cw.cubes.leaflet.renderLeafLetMap(%s, %s);
};
initMap();""" % (js_dumps(datasource), js_dumps(self.settings)))

    def div_holder(self):
        style = u''
        width = self.settings.get('width', 940)
        if width:
            if isinstance(width, int):
                width = '%spx' % width
            style += 'width: %s;' % width
        height = self.settings.get('height', 400)
        if height:
            if isinstance(height, int):
                height = '%spx' % height
            style += 'height: %s;' % height
        return u'<div id="%s" style="%s"></div>' % (self.settings['divid'], style)


class LeafletMultiPolygon(LeafletMap):
    """ LeafletMap class for plotting multipolygon.
    Should be used in a view.
    """

    js_plotter = 'cw.cubes.leaflet.plotMap'

    def _call_js_onload(self, req, datasource):
        req.add_onload('cw.cubes.leaflet.initMap(%s)' % js_dumps(self.settings))
        req.add_onload('%s(%s, %s)' % (self.js_plotter,
                                       js_dumps(datasource),
                                       js_dumps(self.settings)))


class LeafletMultiPolygonValues(LeafletMultiPolygon):
    """ LeafletMap class for plotting multipolygon with associated values.
    Should be used in a view.
    """

    default_settings = {
        'legend_visibility': True,
        'legend_position': 'bottomright',
        'info_visibility': True,
        'info_position': 'topright',
    }

    js_plotter = 'cw.cubes.leaflet.plotMapValues'

    def get_settings(self, custom_settings=None):
        settings = super(LeafletMultiPolygonValues, self).default_settings.copy()
        settings.update(self.default_settings)
        settings.update(custom_settings or {})
        return settings


#############################################################################
# LEAFLET VIEWS #############################################################
#############################################################################

class AbstractLeafletView(AnyRsetView):
    __abstract__ = True
    __regid__ = 'leaflet'
    title = _('Leaflet')
    paginable = False
    plotclass = LeafletMap

    def call(self, custom_settings=None, use_cdn=True):
        """ View call """
        markers = self.build_markers()
        settings = self._update_settings(custom_settings)
        geomap = self.plotclass(settings)
        self.w(geomap.render(self._cw, datasource=markers, use_cdn=use_cdn))

    def _update_settings(self, custom_settings):
        """ Update the default settings with custom settings and form"""
        settings = custom_settings.copy() if custom_settings else {}
        for attr, value in self._cw.form.iteritems():
            if attr in settings:
                settings[attr] = value
        if 'cluster' in self._cw.form:
            settings['cluster'] = True
        return settings

    def build_markers(self):
        """ Build the markers from the current cw_rset """
        markers = []
        for rownum, _ in enumerate(self.cw_rset.rows):
            marker = self._build_markers_from_row(rownum)
            if marker:
                markers.append(marker)
        return markers

    def _build_markers_from_row(self, rownum):
        """ Build the markers from the ``rownum`` of the current cw_rset """
        raise NotImplementedError


class IGeocodableLeafletView(AbstractLeafletView):
    """ Simple leaflet view for IGeocodable entities.
    """
    __select__ = AbstractLeafletView.__select__ & adaptable('IGeocodable')

    def _build_markers_from_row(self, rownum):
        """ Build a marker from an igeocodable entity """
        entity = self.cw_rset.get_entity(rownum, 0)
        igeocodable = entity.cw_adapt_to('IGeocodable')
        if not igeocodable.latitude or not igeocodable.longitude:
            return
        marker = {}
        marker['eid'] = entity.eid
        marker['latitude'] = igeocodable.latitude
        marker['longitude'] = igeocodable.longitude
        marker['title'] = entity.dc_title()
        marker['url'] = entity.absolute_url()
        marker['description'] = entity.dc_description(format='text/html') or ''
        marker['icon_options'] = {'iconUrl': self.marker_icon(entity)}
        marker['popup'] = '<h3><a href="{url}">{title}</a></h3>{description}'
        return marker

    def marker_icon(self, entity):
        return entity.cw_adapt_to('IGeocodable').marker_icon


class RowLeafletView(AbstractLeafletView):
    """ Simple leaflet view that try to convert the first column to latitude
    and the second column to longitude.
    """
    __select__ = AbstractLeafletView.__select__ & multi_columns_rset(2)

    def _build_markers_from_row(self, rownum):
        """ Build a marker from the ``rownum`` of the current cw_rset,
        probably floats"""
        marker = {}
        marker['eid'] = make_uid('marker')
        row = self.cw_rset[rownum]
        if not len(row) >= 2 or not row[0] or not row[1]:
            return
        try:
            marker['latitude'] = float(row[0])
            marker['longitude'] = float(row[1])
        except (TypeError, ValueError):
            return
        data = []
        for i in range(2, len(row)):
            if rset.description[rownum][i] == 'String' and row[i]:
                data.append(xml_escape(row[i]))
        if data:
            marker['title'] = data[0]
            marker['notes'] = data[1:]
            _d = [d for d in data if d.startswith('http://')]
            if _d:
                marker['url'] = _d[0]
        return marker


#############################################################################
# LEAFLET POLYGON VIEW ######################################################
#############################################################################
class GeoJsonView(AbstractLeafletView):
    """ Leaflet view that work on a single column rset.
    It expects GeoJson on the single column and will plot Multipolygon
    based on this GeoJson. This should be used with the postgis cube
    and the 'ASJSON' RQL function
    """
    title = _('GeoJson')
    __regid__ = 'leaflet-geojson'
    paginable = False
    __select__ = AbstractLeafletView.__select__ & multi_columns_rset(1)
    plotclass = LeafletMultiPolygon

    def build_markers(self):
        """ Build the markers from an rset """
        return JSString('[%s]' % ', '.join(row[0] for row in self.cw_rset.rows))


class GeoJsonValuesView(AbstractLeafletView):
    """Leaflet view that works on a multicolumns rset.

    It expects GeoJson on the first column. It will plot Multipolygon
    based on this GeoJson. This should be used with the postgis cube
    and the 'ASJSON' RQL function.

    If the second column contains numbers, they are used to colorize
    geometries. Otherwize, the row index is used to colorize the
    geometry.
    """
    title = _('GeoJson')
    __regid__ = 'leaflet-geojson'
    paginable = False
    __select__ = (AbstractLeafletView.__select__ &
                  multi_columns_rset())

    plotclass = LeafletMultiPolygonValues

    def _get_geo(self, row):
        return row[0]

    def _get_data(self, row):
        return js_dumps(row[1:])

    def build_markers(self):
        """ Build the markers from an rset """
        datafmt = ('{"type": "Feature", '
                   ' "id": %(id)s, '
                   ' "properties": %(vals)s, '
                   ' "geometry": %(geo)s}')
        data = ', '.join(datafmt % {'id': i,
                                    'vals': self._get_data(row),
                                    'geo': self._get_geo(row)}
                         for i, row in enumerate(self.cw_rset))
        return JSString('{"type": "FeatureCollection","features": [%s]}' % data)
