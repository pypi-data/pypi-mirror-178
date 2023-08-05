# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""
Methods for calculating area representations from a
collection of infrastructure elements. These elements 
need to be point collections with geographic properties.



"""
import structlog
from typing import List

from ...core.query import Query
from ...core.mixins import GeoDataMixin

from .versioned_infrastructure import VersionedInfrastructure

logger = structlog.get_logger("flowmachine.debug", submodule=__name__)


class _viewshedSlopes(Query):
    """
    Private class for generating a slopes vector
    for the `viewshed` method used in the LocationArea()
    class. This class is only instantiated by that
    other class and not used to be called directly.

    Parameters
    ----------
    radius_query : str
        An SQL statement as generated by the method
        LocationArea()._radius(). This is used
        as an alias for creating buffer areas
        that clipped a DEM raster.

    dem : str
        Digital Elevation Model raster table to
        use. This is passed down from LocationArea().

    above_ground_position : int or float
        Position above base elevation where observer is
        positioned. This is passed down from LocationArea().

    """

    def __init__(self, radius_query, dem, band, above_ground_position):

        self.radius_query = radius_query
        self.dem = dem
        self.band = band
        self.above_ground_position = above_ground_position

        super().__init__()

    @property
    def column_names(self) -> List[str]:
        return [
            "location_id",
            "geom_point",
            "od_line_identifier",
            "geom",
            "distance",
            "slope",
        ]

    def _make_query(self):

        sql = """
       
        SELECT
            A.location_id,
            A.geom_point,
            B.od_line_identifier,
            B.geom AS geom,
            ST_Distance(
                A.geom_point::geography, 
                ST_Centroid(B.geom)::geography
            ) AS distance,
            (B.val - (first_value(B.val) OVER (ORDER BY ST_Distance(
                    A.geom_point::geography, 
                    ST_Centroid(B.geom
                )::geography) + {observer_position})) 
                / ST_Distance(A.geom_point::geography, ST_Centroid(B.geom)::geography)) AS slope
        FROM ({radius_table}) AS A
        JOIN (
            SELECT
                A.location_id,
                A.geom_point,
                A.od_line_identifier,
                B.*
            FROM (
                SELECT
                    A.location_id,
                    A.geom_point,
                    uuid_generate_v4() AS od_line_identifier,
                    ST_MakeLine(A.geom_point::geometry, ST_Centroid(B.geom)) as geom
                FROM ({radius_table}) AS A
                JOIN (
                    SELECT
                        A.location_id,
                        B.*
                    FROM ({radius_table}) AS A,
                        (
                            SELECT
                                (ST_PixelAsPolygons(rast)).*
                            FROM (
                                SELECT
                                    A.location_id,
                                    ST_Clip(B.rast, ARRAY[{band}], A.geom_radius::geometry) AS rast
                                FROM ({radius_table}) as A,
                                     {dem_table} AS B
                                WHERE ST_Intersects(B.rast, A.geom_radius::geometry)
                            ) AS A
                        ) AS B
                    WHERE ST_Intersects(ST_ExteriorRing(A.geom_radius::geometry)::geometry, B.geom)
                ) AS B
                  ON A.location_id = B.location_id
            ) AS A,
              (
                SELECT
                    (ST_PixelAsPolygons(rast)).*
                FROM (
                    SELECT
                        A.location_id,
                        ST_Clip(B.rast, ARRAY[{band}], A.geom_radius::geometry) AS rast
                    FROM ({radius_table}) as A,
                         {dem_table} AS B
                    WHERE ST_Intersects(B.rast, A.geom_radius::geometry)
                ) AS A
              ) AS B
            WHERE ST_Intersects(A.geom::geometry, B.geom)
        ) AS B
          ON A.location_id = B.location_id
        ORDER BY ST_Distance(A.geom_point::geography, ST_Centroid(B.geom)::geography) ASC

        """.format(
            radius_table=self.radius_query,
            dem_table=self.dem,
            band=self.band,
            observer_position=self.above_ground_position,
        )

        return sql


class _computeArea(Query):
    """
    Private class for providing flowmachine Query()
    object used for calculating the metric area
    of a LocationArea() instance.

    Parameters
    ----------
    location_area_query : str
        Query from a LocationArea().get_query()
        method.

    geom_area_column : str
        Column that contains the geometric data
        that represents the polygon of a
        LocationArea() object.
    """

    def __init__(self, location_area_query, geom_area_column):

        self.location_area_query = location_area_query
        self.geom_area_column = geom_area_column

        super().__init__()

    @property
    def column_names(self) -> List[str]:
        return ["location_id", "geom_point", self.geom_area_column, "area"]

    def _make_query(self):

        sql = """

            WITH location_area_table AS ({location_area_query})
            SELECT
                location_id,
                geom_point,
                {geom_area},
                ST_Area({geom_area}::geography) as area
            FROM location_area_table

        """.format(
            location_area_query=self.location_area_query,
            geom_area=self.geom_area_column,
        )

        return sql


class LocationArea(GeoDataMixin, Query):
    """
    Class for generating a location area. This class is
    designed for generating surface area representation
    for a given point collection. Areas can be circles
    (generated from a given radius), Voronoi polygons,
    or a combination of those. Other more advanced methods
    will be implemented in the future.

    This class implements the Viewshed algorithm as proposed
    by

        Franklin, W.R., C.K. Ray, and S. Mehta, 1994. "Geometric
            Algorithms for Siting of Air Defense Missile
            Batteries", Technical Report DAAL03-86-D-0001,
            Battelle, Columbus Division, Columbus, Ohio, 129 p.

    Parameters
    ----------
    point_collection : str or list, default 'sites'
        A point collection with longitude and latitudes.
        This parameter can fetch a table in the database (if a
        str is passed) or a list collection of tuples.

    location_identifier : str, default 'id'
        Location identifier from the point table to use. This
        identifier must be unique to each location.

    geometry_identifier : str, default 'geom_point'
        Geometry column to use in computations. If
        calling a table from the database the column must
        have type `GEOMETRY` or `GEOGRAPHY`.

    date : str, default None
        If using infrastructure.* tables (`sites` or `cells`)
        then a date is needed to determine which version
        of locations to use (because infrastructure elements
        may change locations). If no date is provided,
        the current date is used.

    method : str, default 'voronois'
        Method to use to compute polygons. The method can
        be one of the following:

            * 'voronois':           Computes a Voronoi tessellation.
            * 'radius-voronois':    Calculates a Voronoi tessellation
                                    that is clipped based on a generated
                                    circle.
            * 'radius':             Generates a circle based on a given
                                    input radius.
            * 'viewshed':           Computes viewshed polygons from point
                                    collection.
            * 'radio-propagation':  Computes radio propagation polygons
                                    from point collection (not implemented).

    radius : int, default 35
        Radius of buffer area around circle to generate
        in Km. Default value is 35km.

    envelope_table : str, default 'geography.admin0'
        Table to use for keeping all geometries within a
        certain envelope. This is generally used to keep
        generated polygons within the boundaries of a
        region or country. Default is `geography.admin0`.
        The table must contain a PostGIS `geom` column.

    dem : str, default 'elevation.nasa_srtm1'
        Digital elevation model table. The default table is `nasa_srtm1`.

    band : int, default 1
        Band number identifier used to fetch data from the DEM.
        The default is `1` for this parameter, and rarely changes.

    above_ground_position : int or float, default 0
        Position above ground in which the observer is placed.
        This position is used to place the observer above
        the elevation of its position. It is common that
        transmitters are placed on towers. This parameter
        indicates the height of the transmitters. It should
        match the unit of the DEM dataset provided in `dem`.

    """

    def __init__(
        self,
        point_collection="sites",
        date=None,
        method="voronois",
        envelope_table="geography.admin0",
        radius=35,
        dem="elevation.nasa_srtm1",
        band=1,
        location_identifier="id",
        geometry_identifier="geom_point",
        above_ground_position=0,
    ):

        self.point_collection = point_collection
        self.date = date
        self.method = method
        self.envelope_table = envelope_table
        self.radius = radius * 1000
        self.dem = dem
        self.band = band
        self.location_identifier = location_identifier
        self.geometry_identifier = geometry_identifier
        self.above_ground_position = float(above_ground_position)
        self.column_name = "geom_" + self.method.replace("-", "_")

        if self.point_collection in ("sites", "cells"):
            self.versioned_infrastructure = VersionedInfrastructure(
                table=self.point_collection, date=self.date
            )

        if self.method not in (
            "voronois",
            "radius-voronois",
            "radius",
            "viewshed",
            "radio-propagation",
        ):
            raise ValueError("Method %s not recognized" % self.method)

        if self.method in ("radius", "radius-voronois") and self.radius is None:
            logger.info(
                'Using 10km radius. Use the "radius" parameter to change '
                + "this figure."
            )

        if self.method in ("viewshed") and self.dem is None:
            raise ValueError(
                "Please provide Digital Elevation Model table "
                + "with the `dem` parameter."
            )

        if self.method == "viewshed":
            self.viewshedslopes = _viewshedSlopes(
                radius_query=self.__radius(),
                dem=self.dem,
                band=self.band,
                above_ground_position=self.above_ground_position,
            )
        if self.method in ("radio-propagation"):
            raise NotImplementedError(
                "Method `{}` not yet implemented.".format(self.method)
            )

        if not isinstance(self.above_ground_position, float):
            raise ValueError("Parameter `above_ground_position` must be a number.")

        super().__init__()

        self.computed_area = _computeArea(
            location_area_query=self.get_query(), geom_area_column=self.column_name
        )

    @property
    def column_names(self) -> List[str]:
        return ["location_id", "geom_point", self.column_name]

    def __get_point_statement(self):
        """
        Protected method that generates SQL statement
        for a point collection. The point collection
        can either be a table from the database
        or an array of tuples passed in the
        "points" parameter.

        Returns
        -------
        sql : str
            SQL string that represents a table containing
            both a unique identifier and a geometry (geom_point).
        """
        if isinstance(self.point_collection, str):
            if self.point_collection in ("sites", "cells"):
                sql_points = "(" + self.versioned_infrastructure.get_query() + ")"
            else:
                sql_points = self.point_collection

            sql = """

            SELECT
                {location_identifier},
                {geometry_identifier} AS geom_point
            FROM {table} AS A

            """.format(
                location_identifier=self.location_identifier,
                geometry_identifier=self.geometry_identifier,
                table=sql_points,
            )

        else:
            raise NotImplementedError(
                'Parsing of {} for the "point_collection" '
                + "parameter is not yet implemented.".format(
                    type(self.point_collection)
                )
            )

        return sql

    def __set_envelope(self, statement, columns):
        """
        Protected method for generating SQL that
        returns an envelope table.

        Parameters
        ----------
        statement : str
            SQL statement of a resulting geography table.
            The geometries from this table will be
            clipped to a specified envelope.

        columns : list
            List with the list of columns from the
            prepared table. The last columns must
            be the geography columns to be
            clipped.

        Returns
        -------
        str
            SQL string that clips inside geometries using
            an envelope geometry.

        """
        identity_columns_statement = """
        {}
        """.format(
            ",".join(columns[0:-1])
        )

        sql = """

            WITH envelope_table AS (
                SELECT
                    geom as geom_envelope
                FROM {table}
            ),
            geometry_table AS ({geometry_table_statement})
            SELECT
                {identity_columns},
                ST_Intersection(
                    E.geom_envelope::geometry,
                    G.{geometry_column}::geometry
                )::geography as {geometry_column}
            FROM geometry_table AS G,
                 envelope_table as E
            WHERE ST_Intersects(E.geom_envelope, G.{geometry_column})

        """.format(
            table=self.envelope_table,
            geometry_table_statement=statement,
            identity_columns=identity_columns_statement,
            geometry_column=columns[-1],
        )

        return sql

    def __radius(self):
        """
        Protected method for generating SQL that performs
        the calculation of a buffer area around a point
        collection. Point collections have to be defined
        as a table and generated via the method
        _get_point_statement().

        Returns
        -------
        str
            SQL statement that creates a buffer area
            based on a given radius.
        """
        sql = """

            SELECT
                point_table.{location_identifier} as location_id,
                point_table.geom_point as geom_point,
                ST_Buffer(point_table.geom_point::geography,
                          {radius}) as geom_radius
            FROM ({table}) AS point_table

        """.format(
            location_identifier=self.location_identifier,
            table=self.__get_point_statement(),
            radius=self.radius,
        )

        return sql

    def __voronoi_tesselation(self):
        """
        Protected method for generating SQL that
        computes the Voronoi tessellation based on a
        point collection. The point collection comes
        from the method _get_point_statement().

        Return
        ------
        str
            SQL string that creates a Voronoi
            tessellation based on a point collection.

        """
        sql = """

            WITH point_table AS ({table}),
            point_join AS (
               SELECT 
                    (geom).geom AS geom_polygon
                FROM (
                    SELECT
                        ST_Dump(
                            ST_VoronoiPolygons(ST_Collect(point_table.geom_point::geometry))
                        ) AS geom
                    FROM point_table
                ) AS voronoi
            )
            SELECT
                S.{location_identifier} AS location_id,
                S.geom_point::geography AS geom_point,
                P.geom_polygon::geography AS geom_voronois
            FROM point_table AS S
            JOIN point_join AS P
                ON ST_Within(S.geom_point::geometry, P.geom_polygon::geometry)

        """.format(
            location_identifier=self.location_identifier,
            table=self.__get_point_statement(),
        )

        return sql

    def __radius_voronois(self):
        """
        Protected method for generating SQL that performs
        the clipping each voronoi of a Voronoi tessellation
        based on a circle created via the _radius() method.

        Returns
        -------
        str
            SQL string that creates a Voronoi tessellation
            using buffer areas to create a maximum coverage
            distance.
        """
        sql = """

            SELECT
                R.location_id,
                R.geom_point,
                ST_Intersection(R.geom_radius::geography,
                                V.geom_voronois::geography) as geom_radius_voronois
            FROM ({radius_table}) AS R
            JOIN ({voronois_table}) AS V
                ON R.location_id = V.location_id

        """.format(
            radius_table=self.__radius(), voronois_table=self.__voronoi_tesselation()
        )

        return sql

    def __viewshed(self):
        """
        Protected method for generating SQL that generates
        a viewshed area visible from a given point on the
        surface of the Earth.
        """

        logger.info("Computing elevation slopes.")

        self.viewshedslopes.store().result()

        logger.info("Computing viewshed polygons.")
        sql = """

            SELECT 
                location_id,
                geom_point,
                ST_Union(geom_viewshed) AS geom_viewshed
            FROM viewshed('{table_name}')
            WHERE visible
            GROUP BY location_id, geom_point

        """.format(
            table_name=self.viewshedslopes.fully_qualified_table_name
        )

        return sql

    def __radio_propagation(self):
        """
        Protected method for generating SQL that generates
        areas that represent radio coverage based on a
        specified radio propagation model.
        """
        pass

    def _make_query(self):
        if self.method == "voronois":
            sql = self.__voronoi_tesselation()

        elif self.method == "radius":
            sql = self.__radius()

        elif self.method == "radius-voronois":
            sql = self.__radius_voronois()

        elif self.method == "viewshed":
            logger.warning("The method `viewshed` is currently **experimental**.")
            logger.warning(
                "The `viewshed` method is very computationally expensive. "
                + "The algorithm can take a few hours to complete depending "
                + "on the spatial resolution of the Digital Elevation Model, "
                + "on how many infrastructure elements exist, and the size "
                + "of the `radius` used. It is recommended to start with a small "
                + "radius (0.01km) then move up accordingly."
            )

            sql = self.__viewshed()

        if self.envelope_table:
            columns = ["location_id", "geom_point", self.column_name]
            sql = self.__set_envelope(sql, columns)

        return sql

    def _geo_augmented_query(self):
        sql_base = self.get_query()
        sql = (
            """

            SELECT
                location_id AS gid,
                {geometry_column} AS geom
            FROM ({base_query}) AS A

        """.format(
                geometry_column=self.column_name, base_query=sql_base
            ),
            ["gid", "geom"],
        )

        return sql

    def area(self):
        """
        Short-hand method for calculating the area of each
        LocationArea() representation computed. This method
        uses the projection from Flowdb (WGS84 by default).
        This could compute incorrect distances depending
        on the scenario.

        Returns
        -------
        DataFrame
            pandas.DataFrame containing areas in Km.
        """
        return self.computed_area.get_dataframe()
