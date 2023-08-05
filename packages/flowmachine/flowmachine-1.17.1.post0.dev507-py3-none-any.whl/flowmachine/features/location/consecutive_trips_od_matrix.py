# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

# -*- coding: utf-8 -*-

from typing import List

from flowmachine.features.location.flows import FlowLike
from flowmachine.core.query import Query
from flowmachine.features.utilities.subscriber_locations import SubscriberLocations


class ConsecutiveTripsODMatrix(FlowLike, Query):
    """
    An object which represents a count of subscriber who made consecutive visits between locations.

    Originally added as the FlowKit implementation of COVID-19 aggregate[1]_[2]_.

    Parameters
    ----------
    subscriber_locations : SubscriberLocations

    Examples
    --------
    >>> ConsecutiveTripsODMatrix(subscriber_locations=SubscriberLocations('2016-01-01 13:30:30','2016-01-02 16:25:00')).head()
      location_id_from location_id_to  value
    0         0RIMKYtf       ZOsVSeQS      3
    1         0RIMKYtf       ypbTrAkZ      1
    2         0RIMKYtf       yPANTB8f      1
    3         0RIMKYtf       wQ7i3Z8n      1
    4         0RIMKYtf       WET2L101      2

    References
    ----------
    .. [1] https://github.com/Flowminder/COVID-19/issues/9
    .. [2] https://covid19.flowminder.org

    """

    def __init__(self, subscriber_locations: SubscriberLocations):
        self.spatial_unit = subscriber_locations.spatial_unit
        self.subscriber_locations = subscriber_locations
        super().__init__()

    @property
    def index_cols(self):
        cols = self.spatial_unit.location_id_columns
        return [["{}_from".format(x) for x in cols], ["{}_to".format(x) for x in cols]]

    @property
    def column_names(self) -> List[str]:
        cols = self.spatial_unit.location_id_columns
        return (
            [f"{col}_from" for col in cols] + [f"{col}_to" for col in cols] + ["value"]
        )

    def _make_query(self):
        loc_cols = self.spatial_unit.location_id_columns

        loc_cols_from_string = ",".join([f"{col}_from" for col in loc_cols])
        loc_cols_to_string = ",".join([f"{col}_to" for col in loc_cols])

        loc_cols_from_aliased_string = ",".join(
            [f"source.{col} AS {col}_from" for col in loc_cols]
        )
        loc_cols_to_aliased_string = ",".join(
            [f"sink.{col} AS {col}_to" for col in loc_cols]
        )

        grouped = f"""
        WITH located AS (
            SELECT subscriber,
              {", ".join(loc_cols)},
              row_number() OVER (PARTITION BY subscriber ORDER BY time ASC) AS rank
            FROM ({self.subscriber_locations.get_query()}) _
            )
        SELECT
            {loc_cols_from_string},
            {loc_cols_to_string},
            count(*) as value
        FROM 
            (
            SELECT
            subscriber,
            {loc_cols_from_aliased_string},
            {loc_cols_to_aliased_string}
            FROM
            located AS source
            INNER JOIN
            (
                SELECT subscriber,
                  {", ".join(loc_cols)},
                 rank-1 AS rank
                FROM located
            ) AS sink
            USING (subscriber, rank)
            GROUP BY
                subscriber, {loc_cols_from_string}, {loc_cols_to_string}
            ) AS joined
        GROUP BY {loc_cols_from_string}, {loc_cols_to_string}
        ORDER BY {loc_cols_from_string}, {loc_cols_to_string} DESC
        """

        return grouped
