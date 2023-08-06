"""Cisco Spark Rooms-API wrapper classes.

Classes:
    Room: Models a Spark 'room' JSON object as a native Python object.
    RoomsAPI: Wrappers the Cisco Spark Rooms-API and exposes the API calls as
        Python method calls that return native Python objects.

"""


from ciscosparkapi.exceptions import ciscosparkapiException
from ciscosparkapi.helper import utf8, generator_container
from ciscosparkapi.restsession import RestSession
from ciscosparkapi.sparkdata import SparkData


class Room(SparkData):
    """Model a Spark 'room' JSON object as a native Python object."""

    def __init__(self, json):
        """Init a new Room data object from a JSON dictionary or string.

        Args:
            json(dict, unicode, str): Input JSON object.

        Raises:
            TypeError: If the input object is not a dictionary or string.

        """
        super(Room, self).__init__(json)

    @property
    def id(self):
        return self._json[u'id']

    @property
    def title(self):
        return self._json[u'title']

    @property
    def type(self):
        return self._json[u'type']

    @property
    def isLocked(self):
        return self._json[u'isLocked']

    @property
    def lastActivity(self):
        return self._json[u'lastActivity']

    @property
    def created(self):
        return self._json[u'created']

    @property
    def creatorId(self):
        return self._json[u'creatorId']

    @property
    def teamId(self):
        """Return the room teamId, if it exists, otherwise return None.

        teamId is an 'optional' attribute that only exists for Spark rooms that
        are associated with a Spark Team.  To simplify use, rather than
        requiring use of try/catch statements or hasattr() calls, we simply
        return None if a room does not have a teamId attribute.
        """
        return self._json.get(u'teamId', None)


class RoomsAPI(object):
    """Cisco Spark Rooms-API wrapper class.

    Wrappers the Cisco Spark Rooms-API and exposes the API calls as Python
    method calls that return native Python objects.

    Attributes:
        session(RestSession): The RESTful session object to be used for API
            calls to the Cisco Spark service.

    """

    def __init__(self, session):
        """Init a new RoomsAPI object with the provided RestSession.

        Args:
            session(RestSession): The RESTful session object to be used for
                API calls to the Cisco Spark service.

        Raises:
            AssertionError: If the parameter types are incorrect.

        """
        assert isinstance(session, RestSession)
        super(RoomsAPI, self).__init__()
        self.session = session

    @generator_container
    def list(self, max=None, **query_params):
        """List rooms.

        By default, lists rooms to which the authenticated user belongs.

        This method supports Cisco Spark's implementation of RFC5988 Web
        Linking to provide pagination support.  It returns a generator
        container that incrementally yield all rooms returned by the
        query.  The generator will automatically request additional 'pages' of
        responses from Spark as needed until all responses have been returned.
        The container makes the generator safe for reuse.  A new API call will
        be made, using the same parameters that were specified when the
        generator was created, every time a new iterator is requested from the
        container.

        Args:
            max(int): Limits the maximum number of rooms returned from the
                Spark service per request.
            **query_params:
                teamId(unicode, str): Limit the rooms to those associated with
                    a team.
                type(unicode, str):
                    'direct': returns all 1-to-1 rooms.
                    'group': returns all group rooms.

        Yields:
            Room: The the next room from the Cisco Spark query.

        Raises:
            AssertionError: If the parameter types are incorrect.
            SparkApiError: If the Cisco Spark cloud returns an error.

        """
        # Process args
        assert max is None or isinstance(max, int)
        params = {}
        if max:
            params[u'max'] = max
        # Process query_param keyword arguments
        if query_params:
            for param, value in query_params.items():
                if isinstance(value, basestring):
                    value = utf8(value)
                params[utf8(param)] = value
        # API request - get items
        items = self.session.get_items('rooms', params=params)
        # Yield Room objects created from the returned items JSON objects
        for item in items:
            yield Room(item)

    def create(self, title, teamId=None):
        """Create a room.

        The authenticated user is automatically added as a member of the room.

        Args:
            title(unicode, str): A user-friendly name for the room.
            teamId(unicode, str): The team ID with which this room is
                associated.

        Returns:
            Room: With the details of the created room.

        Raises:
            AssertionError: If the parameter types are incorrect.
            SparkApiError: If the Cisco Spark cloud returns an error.

        """
        # Process args
        assert isinstance(title, basestring)
        assert teamId is None or isinstance(teamId, basestring)
        post_data = {}
        post_data[u'title'] = utf8(title)
        if teamId:
            post_data[u'teamId'] = utf8(teamId)
        # API request
        json_obj = self.session.post('rooms', json=post_data)
        # Return a Room object created from the response JSON data
        return Room(json_obj)

    def get(self, roomId):
        """Get the details of a room, by ID.

        Args:
            roomId(unicode, str): The roomId of the room.

        Returns:
            Room: With the details of the requested room.

        Raises:
            AssertionError: If the parameter types are incorrect.
            SparkApiError: If the Cisco Spark cloud returns an error.

        """
        # Process args
        assert isinstance(roomId, basestring)
        # API request
        json_obj = self.session.get('rooms/'+roomId)
        # Return a Room object created from the response JSON data
        return Room(json_obj)

    def update(self, roomId, **update_attributes):
        """Update details for a room.

        Args:
            roomId(unicode, str): The roomId of the room to be updated.

        **update_attributes:
            title(unicode, str): A user-friendly name for the room.

        Returns:
            Room: With the updated Spark room details.

        Raises:
            AssertionError: If the parameter types are incorrect.
            ciscosparkapiException: If an update attribute is not provided.
            SparkApiError: If the Cisco Spark cloud returns an error.

        """
        # Process args
        assert isinstance(roomId, basestring)
        # Process update_attributes keyword arguments
        if not update_attributes:
            error_message = "At least one **update_attributes keyword " \
                            "argument must be specified."
            raise ciscosparkapiException(error_message)
        put_data = {}
        for param, value in update_attributes.items():
            if isinstance(value, basestring):
                value = utf8(value)
            put_data[utf8(param)] = value
        # API request
        json_obj = self.session.post('rooms/'+roomId, json=put_data)
        # Return a Room object created from the response JSON data
        return Room(json_obj)

    def delete(self, roomId):
        """Delete a room.

        Args:
            roomId(unicode, str): The roomId of the room to be deleted.

        Raises:
            AssertionError: If the parameter types are incorrect.
            SparkApiError: If the Cisco Spark cloud returns an error.

        """
        # Process args
        assert isinstance(roomId, basestring)
        # API request
        self.session.delete('rooms/'+roomId)
