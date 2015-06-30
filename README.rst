CityTour
--------

How to use::

    >>> from citytour import CityMap
	>>> from citytour import findQuickestPath

    >>> citymap = CityMap()
    >>> citymap.setEdges(value)
    >>> citymap.setDistances(value)
    >>> citymap.setWaitTimes(value)
    >>> citymap.setAvgSpeed(value)
    >>> citymap.setXWaitingList(props['leftright_of_X'],props['topbottom_of_X'],props['leftWait'],props['rightWait'],props['topWait'],props['bottomWait'])

    >>> findshortestpath(citymap,'?','$') # ? and $ being nodes added to the map