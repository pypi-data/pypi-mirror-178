"""Module for a yearly/monthly track summary."""


class Summary:
    """A summary of a user's tracks.

    :ivar years: Mapping of year to :class:`YearSummary`.
    :vartype years: dict[int, YearSummary]
    """

    def __init__(self):
        self.years = {}

    def __iter__(self):
        items = list(self.years.values())
        items.sort(key=lambda y: y.year)
        return iter(items)

    def all_tracks(self):
        """Returns all tracks of the summary.

        :return: All tracks.
        :rtype: list[fietsboek.model.track.Track]
        """
        return [track for year in self for month in year for track in month.all_tracks()]

    def add(self, track):
        """Add a track to the summary.

        This automatically inserts the track into the right yearly summary.

        :param track: The track to insert.
        :type track: fietsboek.model.track.Track
        """
        year = track.date.year
        self.years.setdefault(year, YearSummary(year)).add(track)

    @property
    def total_length(self):
        """Returns the total length of all tracks in this summary.

        :return: The total length in meters.
        :rtype: float
        """
        return sum(track.length for track in self.all_tracks())


class YearSummary:
    """A summary over a single year.

    :ivar year: Year number.
    :vartype year: int
    :ivar months: Mapping of month to :class:`MonthSummary`.
    :vartype months: dict[int, MonthSummary]
    """

    def __init__(self, year):
        self.year = year
        self.months = {}

    def __iter__(self):
        items = list(self.months.values())
        items.sort(key=lambda x: x.month)
        return iter(items)

    def all_tracks(self):
        """Returns all tracks of the summary.

        :return: All tracks.
        :rtype: list[fietsboek.model.track.Track]
        """
        return [track for month in self for track in month]

    def add(self, track):
        """Add a track to the summary.

        This automatically inserts the track into the right monthly summary.

        :param track: The track to insert.
        :type track: fietsboek.model.track.Track
        """
        month = track.date.month
        self.months.setdefault(month, MonthSummary(month)).add(track)

    @property
    def total_length(self):
        """Returns the total length of all tracks in this summary.

        :return: The total length in meters.
        :rtype: float
        """
        return sum(track.length for track in self.all_tracks())


class MonthSummary:
    """A summary over a single month.

    :ivar month: Month number (1-12).
    :vartype month: int
    :ivar tracks: List of tracks in this month.
    :vartype tracks: list[fietsboek.model.track.Track]
    """
    def __init__(self, month):
        self.month = month
        self.tracks = []

    def __iter__(self):
        items = self.tracks[:]
        items.sort(key=lambda t: t.date)
        return iter(items)

    def all_tracks(self):
        """Returns all tracks of the summary.

        :return: All tracks.
        :rtype: list[fietsboek.model.track.Track]
        """
        return self.tracks[:]

    def add(self, track):
        """Add a track to the summary.

        :param track: The track to insert.
        :type track: fietsboek.model.track.Track
        """
        self.tracks.append(track)

    @property
    def total_length(self):
        """Returns the total length of all tracks in this summary.

        :return: The total length in meters.
        :rtype: float
        """
        return sum(track.length for track in self.all_tracks())
