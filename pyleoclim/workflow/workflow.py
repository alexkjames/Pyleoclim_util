

"""
Mapping
"""
def mapAllArchive(lipds = None, markersize = 50, projection = 'Robinson',\
                  proj_default = True, background = True,borders = False,\
                  rivers = False, lakes = False, \
                  figsize = [10,4], saveFig = False, dir=None, format='eps'):

    """Map all the available records loaded into the workspace by archiveType.

    Map of all the records into the workspace by archiveType.
        Uses the default color palette. Enter pyleoclim.plot_default for detail.

    Args
    ----

    lipds : dict
           A list of LiPD files. (Optional)
    markersize : int
                The size of the markers. Default is 50
    projection : str
                the map projection. Available projections:
                'Robinson', 'PlateCarree', 'AlbertsEqualArea',
                'AzimuthalEquidistant','EquidistantConic','LambertConformal',
                'LambertCylindrical','Mercator','Miller','Mollweide','Orthographic' (Default),
                'Sinusoidal','Stereographic','TransverseMercator','UTM',
                'InterruptedGoodeHomolosine','RotatedPole','OSGB','EuroPP',
                'Geostationary','NearsidePerspective','EckertI','EckertII',
                'EckertIII','EckertIV','EckertV','EckertVI','EqualEarth','Gnomonic',
                'LambertAzimuthalEqualArea','NorthPolarStereo','OSNI','SouthPolarStereo'
    proj_default : bool
                  If True, uses the standard projection attributes, including centering.
                  Enter new attributes in a dictionary to change them. Lists of attributes
                  can be found in the Cartopy documentation:
                  https://scitools.org.uk/cartopy/docs/latest/crs/projections.html#eckertiv
    background : bool
                If True, uses a shaded relief background (only one available in Cartopy)

    borders : bool
             Draws the countries border. Defaults is off (False).
    rivers : bool
            Draws major rivers. Default is off (False).
    lakes : bool
           Draws major lakes. Default is off (False).

    figsize : list
             the size for the figure
    saveFig : bool
             Default is to not save the figure
    dir : str
         The absolute path of the directory in which to save the
         figure. If not provided, creates a default folder called 'figures'
         in the LiPD working directory (lipd.path).
    format : str
            One of the file extensions supported by the active
            backend. Default is "eps". Most backend support png, pdf, ps, eps,
            and svg.

    Returns
    ------

    "The figure"
    """

    # Get the dictionary of LiPD files
    if lipds is None:
        if 'lipd_dict' not in globals():
            openLipd()
        lipds = lipd_dict

    # Initialize the various lists
    lat = []
    lon = []
    archiveType = []

    # Loop ang grab the metadata
    for idx, key in enumerate(lipds):
        d = lipds[key]
        lat.append(d['geo']['geometry']['coordinates'][1])
        lon.append(d['geo']['geometry']['coordinates'][0])
        archiveType.append(lipdutils.LipdToOntology(d['archiveType']).lower())


    # make sure criteria is in the plot_default list
    for idx,val in enumerate(archiveType):
        if val not in plot_default.keys():
            archiveType[idx] = 'other'


    # Make the map
    fig = visualization.mapAll(lat,lon,archiveType,projection = projection, \
                     proj_default = proj_default,background = background,\
                     borders = borders, rivers = rivers, lakes = lakes,\
                     figsize = figsize, ax = None, palette=plot_default,\
                     markersize = markersize)

    # Save the figure if asked
    if saveFig == True:
        lipdutils.saveFigure('mapLipds_archive', format, dir)
    else:
        plt.show()

    return fig

def mapLipd(timeseries=None, projection = 'Orthographic', proj_default = True,\
           background = True, label = 'default', borders = False, \
           rivers = False, lakes = False,\
           markersize = 50, marker = "default",figsize = [4,4], \
           saveFig = False, dir = None, format="eps"):
    """ Create a Map for a single record

    Orthographic projection map of a single record.

    Args
    ----

    timeseries : object
                a LiPD timeseries object. Will prompt for one if not given
    projection : string
                the map projection. Available projections:
                'Robinson', 'PlateCarree', 'AlbertsEqualArea',
                'AzimuthalEquidistant','EquidistantConic','LambertConformal',
                'LambertCylindrical','Mercator','Miller','Mollweide','Orthographic' (Default),
                'Sinusoidal','Stereographic','TransverseMercator','UTM',
                'InterruptedGoodeHomolosine','RotatedPole','OSGB','EuroPP',
                'Geostationary','NearsidePerspective','EckertI','EckertII',
                'EckertIII','EckertIV','EckertV','EckertVI','EqualEarth','Gnomonic',
                'LambertAzimuthalEqualArea','NorthPolarStereo','OSNI','SouthPolarStereo'
    proj_default : bool
                  If True, uses the standard projection attributes, including centering.
                  Enter new attributes in a dictionary to change them. Lists of attributes
        can be found in the Cartopy documentation:
            https://scitools.org.uk/cartopy/docs/latest/crs/projections.html#eckertiv
    background : bool
                If True, uses a shaded relief background (only one
                available in Cartopy)
    label : str
           label for archive marker. Default is to use the name of the
           physical sample. If no archive name is available, default to
           None. None returns no label.
    borders : bool
             Draws the countries border. Defaults is off (False).
    rivers : bool
            Draws major rivers. Default is off (False).
    lakes : bool
           Draws major lakes. Default is off (False).
    markersize : int
                The size of the marker.
    marker : str or list
            color and type of marker. Default will use the
            default color palette for archives
    figsize : list
             the size for the figure
    saveFig : bool
             default is to not save the figure
    dir : str
         the full path of the directory in which to save the figure.
         If not provided, creates a default folder called 'figures' in the
         LiPD working directory (lipd.path).
    format : str
            One of the file extensions supported by the active
            backend. Default is "eps". Most backend support png, pdf, ps, eps,
            and svg.

    Returns
    -------
    The figure

    """
    # Make sure there are LiPD files to plot
    if timeseries is None:
        if not 'ts_list' in globals():
            fetchTs()
        timeseries = lipdutils.getTs(ts_list)

    # Get latitude/longitude

    lat = timeseries['geo_meanLat']
    lon = timeseries['geo_meanLon']

    # Make sure it's in the palette
    if marker == 'default':
        archiveType = lipdutils.LipdToOntology(timeseries['archiveType']).lower()
        if archiveType not in plot_default.keys():
            archiveType = 'other'
        marker = plot_default[archiveType]

    # Get the label
    if label == 'default':
        for i in timeseries.keys():
            if 'physicalSample_name' in i:
                label = timeseries[i]
            elif 'measuredOn_name' in i:
                label = timeseries[i]
        if label == 'default':
            label = None
    elif label is None:
        label = None
    else:
        assert type(label) is str, 'the argument label should be of type str'

    fig = visualizationap.mapOne(lat, lon, projection = projection, proj_default = proj_default,\
           background = background, label = label, borders = borders, \
           rivers = rivers, lakes = lakes,\
           markersize = markersize, marker = marker, figsize = figsize, \
           ax = None)

    # Save the figure if asked
    if saveFig == True:
        lipdutils.saveFigure(timeseries['dataSetName']+'_map', format, dir)
    else:
        plt.show()

    return fig

class MapFilters():
    """Create the various filters for mapping purposes
    """

    def getData(self, lipd_dict):
        """Initializes the object and store the information into lists
        """
        lat = []
        lon = []
        archiveType = []
        dataSetName =[]

        for idx, key in enumerate(lipd_dict):
            d = lipd_dict[key]
            lat.append(d['geo']['geometry']['coordinates'][1])
            lon.append(d['geo']['geometry']['coordinates'][0])
            archiveType.append(lipdutils.LipdToOntology(d['archiveType']))
            dataSetName.append(d['dataSetName'])

        # make sure criteria is in the plot_default list
        for idx,val in enumerate(archiveType):
            if val not in plot_default.keys():
                archiveType[idx] = 'other'

        return lat, lon, archiveType, dataSetName

    def distSphere(self, lat1,lon1,lat2,lon2):
        """Uses the harversine formula to calculate distance on a sphere

        Args
        ----

        lat1 : float
              Latitude of the first point, in radians
        lon1 : float
              Longitude of the first point, in radians
        lat2 : float
              Latitude of the second point, in radians
        lon2: Longitude of the second point, in radians

        Returns
        -------
        The distance between the two point in km

        """
        R = 6371  #km. Earth's radius
        dlat = lat2-lat1
        dlon = lon2-lon1

        a = np.sin(dlat/2)**2+np.cos(lat1)*np.cos(lat2)*np.sin(dlon/2)**2
        c = 2*np.arctan2(np.sqrt(a),np.sqrt(1-a))
        dist =R*c

        return dist

    def computeDist(self, lat_r, lon_r, lat_c, lon_c):
        """ Computes the distance in (km) between a reference point and an array
        of other coordinates.

        Args
        ----

        lat_r : float
               The reference latitude, in deg
        lon_r : float
               The reference longitude, in deg
        lat_c : list
               An list of latitudes for the comparison points, in deg
        lon_c list : list
                    A list of longitudes for the comparison points, in deg

        Returns
        -------

        dist : list
              a list of distances in km.
        """
        dist = []

        for idx, val in enumerate (lat_c):
            lat1 = np.radians(lat_r)
            lon1 = np.radians(lon_r)
            lat2 = np.radians(val)
            lon2 = np.radians(lon_c[idx])
            dist.append(self.distSphere(lat1,lon1,lat2,lon2))

        return dist

    def filterByArchive(self,archiveType,option):
        """Returns the indexes of the records with the matching archiveType

        Args
        ----

        archiveType : A list of ArchiveType
                     option: the matching string

        Returns
        -------
        idx : list
             The indices matching the query
        """
        idx = [idx for idx,val in enumerate(archiveType) if val==option]
        if not idx:
            print("Warning: Your search criteria doesn't match any record in the database")

        return idx

    def withinDistance(self, distance, radius):
        """ Returns the index of the records that are within a certain distance

        Args
        ----

        distance : list
                  A list containing the distance
        radius : float
                the radius to be considered

        Returns
        -------
        idx : list
             a list of index
        """
        idx = [idx for idx,val in enumerate(distance) if val <= radius]

        return idx

    def filterList(self, lat, lon, archiveType, dist, dataSetName, idx):
        """Filters the list by the given indexes

        Args
        ----

        lat : array
             Array of latitudes
        lon : array
             Array of longitudes
        archiveType : array
                     Array of ArchiveTypes
        dist (array): Array of distances
        dataSetName (array): Array of dataset names
        idx (array): An array of indices used for the filtering

        Returns
        -------
        The previous arrays filtered by indexes.
        """

        lat =  np.array(lat)[idx]
        lon = np.array(lon)[idx]
        archiveType = np.array(archiveType)[idx]
        dataSetName = np.array(dataSetName)[idx]
        dist =np.array(dist)[idx]

        return lat, lon, archiveType, dataSetName, dist


def mapNearRecords(ts = None, lipds = None, n = 5, radius = None, \
                   sameArchive = False, projection = 'Orthographic',\
                   proj_default = True, borders = False, rivers = False, \
                   lakes = False, background = True , markersize = 200,\
                   markersize_adjust = True, marker_r = "ko", \
                   marker_c = "default", cmap = "Reds", colorbar = True,\
                   location = "right", label = "Distance in km",
                   figsize = [4,4],ax = None, saveFig = False, dir = None, \
                   format = "eps"):

    """ Map the nearest records from the record of interest

    Args
    ----

    ts : dict
        A timeseries object. If none given, will prompt for one
    lipds : list
           A list of LiPD files. (Optional)
    n : int
       the number of records to match
    radius : float
            The distance (in km) to search for nearby records. Default is to search the entire globe
    sameArchive : bool
                 Returns only records with the same archiveType. Default is not to do so.

    projection : string
                the map projection. Available projections:
               'Robinson', 'PlateCarree', 'AlbertsEqualArea',
               'AzimuthalEquidistant','EquidistantConic','LambertConformal',
               'LambertCylindrical','Mercator','Miller','Mollweide','Orthographic' (Default),
               'Sinusoidal','Stereographic','TransverseMercator','UTM',
               'InterruptedGoodeHomolosine','RotatedPole','OSGB','EuroPP',
               'Geostationary','NearsidePerspective','EckertI','EckertII',
               'EckertIII','EckertIV','EckertV','EckertVI','EqualEarth','Gnomonic',
               'LambertAzimuthalEqualArea','NorthPolarStereo','OSNI','SouthPolarStereo'
    proj_default : bool
                  If True, uses the standard projection attributes, including centering.
                  Enter new attributes in a dictionary to change them. Lists of attributes
                  can be found in the Cartopy documentation:
                  https://scitools.org.uk/cartopy/docs/latest/crs/projections.html#eckertiv
    background : bool
                If True, uses a shaded relief background (only one
                available in Cartopy)
    borders : bool
             Draws the countries border. Defaults is off (False).
    rivers : bool
            Draws major rivers. Default is off (False).
    lakes : bool
           Draws major lakes. Default is off (False)

    markersize : int
                the size of the marker
    markersize_adjust : bool
                       If True, will proportionaly adjust the size of
                       the marker according to distance.
    marker_r : list or str
              The color and shape of the marker for the
              reference record.
    marker_c : list or str
              The color and shape of the marker for the other
              records. Default is to use the color palette by archiveType. If set
              to None then the color of the marker will represent the distance from
              the reference records.
    cmap : str
          The colormap to use to represent the distance from the
          reference record if no marker is selected.
    colorbar : bool
              Create a colorbar. Default is True
    location : str
              Location of the colorbar
    label : str
           Label for the colorbar.
    figsize : list
             the size for the figure
    ax : ax
        Return as axis instead of figure (useful to integrate plot into a subplot)
    saveFig : bool
             default is to not save the figure
    dir : str
         the full path of the directory in which to save the figure.
         If not provided, creates a default folder called 'figures' in the
         LiPD working directory (lipd.path).
    format : str
            One of the file extensions supported by the active
            backend. Default is "eps". Most backend support png, pdf, ps, eps,
            and svg.


    Returns
    -------
    ax : axis
        The figure

    """

    # Get the dictionary of LiPD files
    if lipds is None:
        if 'lipd_dict' not in globals():
            openLipd()
        lipds = lipd_dict

    # Get a timeseries if not given
    if ts is None:
        if not 'ts_list' in globals():
            fetchTs()
        ts = lipdutils.getTs(ts_list)

    # Get the data
    newfilter = MapFilters()
    lat, lon, archiveType, dataSetName = newfilter.getData(lipds)
    # Calculate the distance
    dist = newfilter.computeDist(ts["geo_meanLat"],
                                 ts["geo_meanLon"],
                                 lat,
                                 lon)

    # Filter to remove the reference record from the list
    idx_zero = np.flatnonzero(np.array(dist))
    if len(idx_zero)==0:
        raise ValueError("No matching records found. Change your search criteria!")
    lat, lon, archiveType, dataSetName, dist = newfilter.filterList(lat,lon,
                                                                    archiveType,
                                                                    dist,
                                                                    dataSetName,
                                                                    idx_zero)

    #Filter to be within the radius
    if radius:
       idx_radius = newfilter.withinDistance(dist, radius)
       if len(idx_radius)==0:
           raise ValueError("No matching records found. Change your search criteria!")
       lat, lon, archiveType, dataSetName, dist = newfilter.filterList(lat,lon,
                                                                    archiveType,
                                                                    dist,
                                                                    dataSetName,
                                                                    idx_radius)

    # Same archive if asked
    if sameArchive == True:
        idx_archive = newfilter.filterByArchive(archiveType,ts["archiveType"])
        if len(idx_archive)==0:
            raise ValueError("No matching records found. Change your search criteria!")
        lat, lon, archiveType, dataSetName, dist = newfilter.filterList(lat,lon,
                                                                    archiveType,
                                                                    dist,
                                                                    dataSetName,
                                                                    idx_archive)

    #Print a warning if plotting less than asked because of the filters
    if n>len(dist):
        print("Warning: Number of matching records is less"+\
              " than the number of neighbors chosen. Including all records "+\
              " in the analysis.")
        n = len(dist)

    # Sort the distance array
    sort_idx = np.argsort(dist)
    lat, lon, archiveType, dataSetName, dist = newfilter.filterList(lat,lon,
                                                                    archiveType,
                                                                    dist,
                                                                    dataSetName,
                                                                    sort_idx)

    # Grab the right number of records
    dist = dist[0:n]
    lat = lat[0:n]
    lon = lon[0:n]
    archiveType = archiveType[0:n]
    dataSetName = dataSetName[0:n]

    # Make the map
    # get the projection:
    if proj_default is True:
        proj_default = {'central_longitude':ts["geo_meanLon"]}
    proj = visualization.setProj(projection=projection, proj_default=proj_default)

    if not ax:
        fig, ax = plt.subplots(figsize=figsize,subplot_kw=dict(projection=proj))
    # draw the coastlines
    ax.coastlines()

    # Background
    if background is True:
        ax.stock_img()

    #Other extra information
    if borders is True:
        ax.add_feature(cfeature.BORDERS)
    if lakes is True:
        ax.add_feature(cfeature.LAKES)
    if rivers is True:
        ax.add_feature(cfeature.RIVERS)

    # Make the scatter plot
    ax.scatter(ts["geo_meanLon"],
               ts["geo_meanLat"],
               s= markersize,
               facecolor = marker_r[0],
               marker = marker_r[1],
               zorder = 10,
               transform=ccrs.PlateCarree())


    #Either plot single color or gradient

    if marker_c is None:
        CS = ax.scatter(lon,lat,
               s= markersize,
               c = dist,
               zorder = 10,
               cmap = cmap,
               marker = '^',
               transform=ccrs.PlateCarree())
        if colorbar == True:
           cb = map.colorbar(CS,location)
           if not not label:
               cb.set_label(label)
    elif marker_c == "default":
        dist_max = np.max(dist)
        dist_adj = np.ceil(dist*markersize/dist_max)
        #Use the archive specific markers
        for archive in archiveType:
           index = [i for i,x, in enumerate(archiveType) if x == archive]
           if markersize_adjust == True:
               ax.scatter(np.array(lon)[index], np.array(lat)[index],
                       s = dist_adj[index],
                       facecolor = plot_default[archive][0],
                       marker = plot_default[archive][1],
                       zorder = 10,
                       transform=ccrs.PlateCarree())
           else:
               ax.scatter(np.array(lon)[index], np.arry(lat)[index],
                       s = markersize,
                       facecolor = plot_default[archive][0],
                       marker = plot_default[archive][1],
                       zorder = 10,
                       transform=ccrs.PlateCarree())
    else:
        dist_max = np.max(dist)
        dist_adj = np.ceil(dist*markersize/dist_max)
        if markersize_adjust == True:
            ax.scatter(np.array(lon), np.array(lat),
                    s=dist_adj, zorder =10,
                    marker = marker_c[1],
                    facecolor = marker_c[0],
                    transform=ccrs.PlateCarree())
        else:
            ax.scatter(np.array(lon), np.array(lat),
                    s=markersize, zorder =10, marker = marker_c[1],
                    facecolor = marker_c[0],transform=ccrs.PlateCarree())

    # Save the figure if asked
    if saveFig == True:
        lipdutils.saveFigure(ts['dataSetName']+'_map', format, dir)
    else:
        plt.show()

    return ax


"""
Plotting
"""

def plotTs(ts = None, x_axis = None, markersize = 50,\
            marker = "default", figsize =[10,4],\
            saveFig = False, dir = None,\
            format="eps"):
    """Plot a single time series.

    Args
    ----

    ts : array
        By default, will prompt the user for one.
    x_axis : str
            The representation against which to plot the paleo-data.
            Options are "age", "year", and "depth". Default is to let the
            system choose if only one available or prompt the user.
    markersize : int
                default is 50.
    marker : str
            a string (or list) containing the color and shape of the
            marker. Default is by archiveType. Type pyleo.plot_default to see
            the default palette.
    figsize : list
             the size for the figure
    saveFig : bool
             default is to not save the figure
    dir : str
         the full path of the directory in which to save the figure.
         If not provided, creates a default folder called 'figures' in the
         LiPD working directory (lipd.path).
    format : str
            One of the file extensions supported by the active
            backend. Default is "eps". Most backend support png, pdf, ps, eps,
            and svg.

    Returns
    -------

    The figure.

    """
    if ts is None:
        if not 'ts_list' in globals():
            fetchTs()
        ts = lipdutils.getTs(ts_list)

    y = np.array(ts['paleoData_values'], dtype = 'float64')
    x, label = lipdutils.checkXaxis(ts, x_axis=x_axis)

    # remove nans and sort time axis
    y,x = analysis.clean_ts(y,x)

    # get the markers
    if marker == 'default':
        archiveType = lipdutils.LipdToOntology(ts['archiveType']).lower()
        if archiveType not in plot_default.keys():
            archiveType = 'other'
        marker = plot_default[archiveType]

    # Get the labels
    # title
    title = ts['dataSetName']
    # x_label
    if label+"Units" in ts.keys():
        x_label = label[0].upper()+label[1:]+ " ("+ts[label+"Units"]+")"
    else:
        x_label = label[0].upper()+label[1:]
    # ylabel
    if "paleoData_inferredVariableType" in ts.keys():
        #This if loop is needed because some files appear to have two
        #different inferredVariableType/proxyObservationType, which
        #should not be possible in the ontology. Just build some checks
        # in the system
        if type(ts["paleoData_inferredVariableType"]) is list:
            var = ts["paleoData_inferredVariableType"][0]
        else:
            var = ts["paleoData_inferredVariableType"]
        if "paleoData_units" in ts.keys():
            y_label = var + \
                      " (" + ts["paleoData_units"]+")"
        else:
            y_label = var
    elif "paleoData_proxyObservationType" in ts.keys():
        if type(ts["paleoData_proxyObservationType"]) is list:
            var = ts["paleoData_proxyObservationType"][0]
        else:
            var = ts["paleoData_proxyObservationType"]
        if "paleoData_units" in ts.keys():
            y_label = var + \
                      " (" + ts["paleoData_units"]+")"
        else:
            y_label = var
    else:
        if "paleoData_units" in ts.keys():
            y_label = ts["paleoData_variableName"] + \
                      " (" + ts["paleoData_units"]+")"
        else:
            y_label = ts["paleoData_variableName"]

    # make the plot
    fig = visualization.plot(x,y,markersize=markersize,marker=marker,x_label=x_label,\
              y_label=y_label, title=title, figsize = figsize, ax=None)

    #Save the figure if asked
    if saveFig == True:
        name = 'plot_timeseries_'+ts["dataSetName"]+\
            "_"+y_label
        lipdutils.saveFigure(name,format,dir)
    else:
        plt.show()

    return fig

def plotEnsTs(ts = None, lipd = None, ensTableName = None, ens = None, \
              color = "default", \
              alpha = 0.005, figsize = [10,4], \
              saveFig = False, dir = None,\
              format="eps"):
    """ Plot timeseries on various ensemble ages

    Args
    ----

    ts : dict
        LiPD timeseries object. By default, will prompt for one
    lipd : dict
          The LiPD dictionary. MUST be provided if timeseries is set.
    ensTableName : str
                  The name of the ensemble table, if known.
    ens : int
         Number of ensembles to plot. By default, will plot either the
         number of ensembles stored in the chronensembleTable or 500 of them,
         whichever is lower
    color : str
           The line color. If None, uses the default color palette
    alpha : float
           Transparency setting for each line. Default is 0.005.
    figsize : list
             the size for the figure
    saveFig : bool
             default is to not save the figure
    dir : str
         the full path of the directory in which to save the figure.
         If not provided, creates a default folder called 'figures' in the
         LiPD working directory (lipd.path).
    format : str
            One of the file extensions supported by the active
            backend. Default is "eps". Most backend support png, pdf, ps, eps,
            and svg.

    Returns
    -------

    The figure

    """
    if ts is None:
        if not 'ts_list' in globals():
            fetchTs()
        ts = lipdutils.getTs(ts_list)
    elif lipd is None and type(ts) is dict:
        raise ValueError("LiPD file should be provided when timeseries is set.")

    # Get the csv files
    if lipd is None:
        if 'archiveType' in lipd_dict.keys():
            csv_dict = lpd.getCsv[lipd_dict]
        else:
            if ts["dataSetName"] not in lipd_dict.keys():
                # Print out warnings
                print("Dataset name and LiPD file name don't match!")
                print("Select your LiPD file from the list")
                # Get the name of the LiPD files stored in memory
                keylist = []
                for val in lipd_dict.keys():
                    keylist.append(val)
                #Print them out for the users
                for idx, val in enumerate(keylist):
                    print(idx,": ",val)
                # Ask the user to pick one
                sel = int(input("Enter the number of the LiPD file: "))
                lipd_name = keylist[sel]
                # Grab the csv list
                csv_dict = lpd.getCsv(lipd_dict[lipd_name])

            else: #Just grab the csv directly
                csv_dict = lpd.getCsv(lipd_dict[ts["dataSetName"]])
    else:
        if 'archiveType' in lipd.keys():
            csv_dict = lpd.getCsv(lipd)
        else:
            if ts["dataSetName"] not in lipd.keys():
                # Print out warnings
                print("Dataset name and LiPD file name don't match!")
                print("Select your LiPD file from the list")
                # Get the name of the LiPD files stored in memory
                keylist = []
                for val in lipd.keys():
                    keylist.append(val)
                #Print them out for the users
                for idx, val in enumerate(keylist):
                    print(idx,": ",val)
                # Ask the user to pick one
                sel = int(input("Enter the number of the LiPD file: "))
                lipd_name = keylist[sel]
                # Grab the csv list
                csv_dict = lpd.getCsv(lipd[lipd_name])
            else: #Just grab the csv directly
                csv_dict = lpd.getCsv(lipd[ts["dataSetName"]])

    # Get the ensemble tables
    if not ensTableName:
        chronEnsembleTables, paleoEnsembleTables = lipdutils.isEnsemble(csv_dict)
    elif ensTableName not in csv_dict.keys():
        print("The name of the table you entered doesn't exist, selecting...")
    else:
        chronEnsembleTables = ensTableName

    # Check the number of Chron Tables
    if len(chronEnsembleTables) == 0:
        raise ValueError("No chronEnsembleTable available")
    elif len(chronEnsembleTables) > 1:
        print("More than one ensemble table available.")
        for idx, val in enumerate(chronEnsembleTables):
            print(idx,": ",val)
        sel = int(input("Enter the number of the table you'd like to use: "))
        ensemble_dict = csv_dict[chronEnsembleTables[sel]]
    else:
        ensemble_dict = csv_dict[chronEnsembleTables[0]]

    # Get depth and values
    depth, ensembleValues = lipdutils.getEnsembleValues(ensemble_dict)

    # Get the paleoData values
    ys = np.array(ts["paleoData_values"], dtype = 'float64')
    ds = np.array(ts["depth"], dtype = 'float64')
    # Remove NaNs
    ys_tmp = np.copy(ys)
    ys = ys[~np.isnan(ys_tmp)]
    ds = ds[~np.isnan(ys_tmp)]

    # Bring the ensemble values to common depth
    ensembleValuestoPaleo = lipdutils.mapAgeEnsembleToPaleoData(ensembleValues, depth, ds)

    # Get plot information
    title = ts['dataSetName']
    x_label = "Age"
    # y_label
    if "paleoData_inferredVariableType" in ts.keys():
        #This if loop is needed because some files appear to have two
        #different inferredVariableType/proxyObservationType, which
        #should not be possible in the ontology. Just build some checks
        # in the system
        if type(ts["paleoData_inferredVariableType"]) is list:
            var = ts["paleoData_inferredVariableType"][0]
        else:
            var = ts["paleoData_inferredVariableType"]
        if "paleoData_units" in ts.keys():
            y_label = var + \
                      " (" + ts["paleoData_units"]+")"
        else:
            y_label = var
    elif "paleoData_proxyObservationType" in ts.keys():
        if type(ts["paleoData_proxyObservationType"]) is list:
            var = ts["paleoData_proxyObservationType"][0]
        else:
            var = ts["paleoData_proxyObservationType"]
        if "paleoData_units" in ts.keys():
            y_label = var + \
                      " (" + ts["paleoData_units"]+")"
        else:
            y_label = var
    else:
        if "paleoData_units" in ts.keys():
            y_label = ts["paleoData_variableName"] + \
                      " (" + ts["paleoData_units"]+")"
        else:
            y_label = ts["paleoData_variableName"]

    # Get the color
    if color == "default":
        archiveType = lipdutils.LipdToOntology(ts['archiveType']).lower()
        if archiveType not in plot_default.keys():
            archiveType = 'other'
        color = plot_default[archiveType][0]

    # Make the plot
    fig = visualization.plotEns(ensembleValuestoPaleo, ys, ens = ens, color = color,\
                       alpha = alpha, x_label = x_label, y_label = y_label,\
                       title = title, figsize = figsize, ax = None)

    # Save the figure if asked
    if saveFig == True:
        name = 'plot_ens_timeseries_'+ts["dataSetName"]+\
            "_"+y_label
        lipdutils.saveFigure(name,format,dir)
    else:
        plt.show()

    return fig

def histTs(ts = None, bins = None, hist = True, \
             kde = True, rug = False, fit = None, hist_kws = {"label":"Histogram"},\
             kde_kws = {"label":"KDE fit"}, rug_kws = {"label":"Rug"}, \
             fit_kws = {"label":"Fit"}, color = "default", vertical = False, \
             norm_hist = True, figsize = [5,5],\
             saveFig = False, format ="eps",\
             dir = None):
    """ Plot a univariate distribution of the PaleoData values

    This function is based on the seaborn displot function, which is
    itself a combination of the matplotlib hist function with the
    seaborn kdeplot() and rugplot() functions. It can also fit
    scipy.stats distributions and plot the estimated PDF over the data.

    Args
    ----
    ts : array
        A timeseries. By default, will prompt the user for one.
    bins : int
          Specification of hist bins following matplotlib(hist),
          or None to use Freedman-Diaconis rule
    hist : bool
          Whether to plot a (normed) histogram
    kde : bool
         Whether to plot a gaussian kernel density estimate
    rug : bool
         Whether to draw a rugplot on the support axis
    fit : object
         Random variable object. An object with fit method, returning
         a tuple that can be passed to a pdf method of positional
         arguments following a grid of values to evaluate the pdf on.
    hist _kws : Dictionary
    kde_kws : Dictionary
    rug_kws : Dictionary
    fit_kws : Dictionary
             Keyword arguments for underlying plotting functions.
             If modifying the dictionary, make sure the labels "hist",
             "kde","rug","fit" are stall passed.
    color : str
           matplotlib color. Color to plot everything but the
           fitted curve in. Default is to use the default paletter for each
           archive type.
    vertical : bool
              if True, oberved values are on y-axis.
    norm_hist : bool
               If True (default), the histrogram height shows
               a density rather than a count. This is implied if a KDE or
               fitted density is plotted
    figsize : list
             the size for the figure
    saveFig : bool
             default is to not save the figure
    dir : bool
        the full path of the directory in which to save the figure.
        If not provided, creates a default folder called 'figures' in the
        LiPD working directory (lipd.path).
    format : str
            One of the file extensions supported by the active
            backend. Default is "eps". Most backend support png, pdf, ps, eps,
            and svg.

    Returns
    -------

        fig : The figure

    """
    if ts is None:
        if not 'ts_list' in globals():
            fetchTs()
        ts = lipdutils.getTs(ts_list)

    # Get the values
    y = np.array(ts['paleoData_values'], dtype = 'float64')

    # Remove NaNs
    index = np.where(~np.isnan(y))[0]
    y = y[index]

    # Get the y_label
    if "paleoData_inferredVariableType" in ts.keys():
        #This if loop is needed because some files appear to have two
        #different inferredVariableType/proxyObservationType, which
        #should not be possible in the ontology. Just build some checks
        # in the system
        if type(ts["paleoData_inferredVariableType"]) is list:
            var = ts["paleoData_inferredVariableType"][0]
        else:
            var = ts["paleoData_inferredVariableType"]
        if "paleoData_units" in ts.keys():
            y_label = var + \
                      " (" + ts["paleoData_units"]+")"
        else:
            y_label = var
    elif "paleoData_proxyObservationType" in ts.keys():
        if type(ts["paleoData_proxyObservationType"]) is list:
            var = ts["paleoData_proxyObservationType"][0]
        else:
            var = ts["paleoData_proxyObservationType"]
        if "paleoData_units" in ts.keys():
            y_label = var + \
                      " (" + ts["paleoData_units"]+")"
        else:
            y_label = var
    else:
        if "paleoData_units" in ts.keys():
            y_label = ts["paleoData_variableName"] + \
                      " (" + ts["paleoData_units"]+")"
        else:
            y_label = ts["paleoData_variableName"]

    # Grab the color
    if color == 'default':
        archiveType = lipdutils.LipdToOntology(ts['archiveType']).lower()
        if archiveType not in plot_default.keys():
            archiveType = 'other'
        color = plot_default[archiveType][0]

    # Make this histogram
    fig = visualization.plot_hist(y, bins = bins, hist = hist, \
        kde = kde, rug = rug, fit = fit, hist_kws = hist_kws,\
        kde_kws = kde_kws, rug_kws = rug_kws, \
        fit_kws = fit_kws, color = color, vertical = vertical, \
        norm_hist = norm_hist, label = y_label, figsize = figsize, ax=None)

    #Save the figure if asked
    if saveFig == True:
        name = 'plot_timeseries_'+ts["dataSetName"]+\
            "_"+y_label
        lipdutils.saveFigure(name,format,dir)
    else:
        plt.show()

    return fig

"""
SummaryPlots
"""

def summaryTs(ts = None, x_axis = None, saveFig = False, dir = None,
               format ="eps"):
    """Basic summary plot

    Plots the following information: the time series, a histogram of
    the PaleoData_values, location map, spectral density using the wwz
    method, and metadata about the record.

    Args
    ----

    ts : object
        a timeseries object. By default, will prompt for one
    x_axis : str
            The representation against which to plot the paleo-data.
            Options are "age", "year", and "depth". Default is to let the
            system choose if only one available or prompt the user.
    saveFig : bool
             default is to not save the figure
    dir : str
         the full path of the directory in which to save the figure.
         If not provided, creates a default folder called 'figures' in the
         LiPD working directory (lipd.path).
    format : str
            One of the file extensions supported by the active
            backend. Default is "eps". Most backend support png, pdf, ps, eps,
            and svg.

    Returns
    -------

    The figure

    """

    if ts is None:
        if not 'ts_list' in globals():
            fetchTs()
        ts = lipdutils.getTs(ts_list)

    # get the necessary metadata
    metadata = visualization.getMetadata(ts)

    # get the information about the timeseries
    x,y,archiveType,x_label,y_label = visualization.TsData(ts, x_axis=x_axis)

    # Clean up
    y,x = analysis.clean_ts(y,x)

    # Make the figure
    fig = plt.figure(figsize=(11,8))
    plt.style.use("ggplot")
    gs = gridspec.GridSpec(2, 5)
    gs.update(left=0, right =1.1)

    # Plot the timeseries
    ax1 = fig.add_subplot(gs[0,:-3])
    archiveType = lipdutils.LipdToOntology(ts['archiveType']).lower()
    if archiveType not in plot_default.keys():
        archiveType = 'other'
    marker = plot_default[archiveType]
    markersize = 50

    visualization.plot(x,y,markersize=markersize, marker = marker, x_label=x_label,\
              y_label=y_label, title = ts['dataSetName'], ax=ax1)
    axes = plt.gca()
    ymin, ymax = axes.get_ylim()

    # Plot the histogram and kernel density estimates
    ax2 = fig.add_subplot(gs[0,2])
    sns.distplot(y, vertical = True, color = marker[0], \
                hist_kws = {"label":"Histogram"},
                kde_kws = {"label":"KDE fit"})
    plt.xlabel('PDF')
    ax2.set_ylim([ymin,ymax])
    ax2.set_yticklabels([])

    # Plot the Map
    lat = ts["geo_meanLat"]
    lon = ts["geo_meanLon"]


    proj_default = {'central_longitude':lon}
    proj = visualization.setProj(projection='Orthographic', proj_default=proj_default)
    ax3 = fig.add_subplot(gs[1,0], projection = proj)
    ax3.coastlines() # add coastlines
    ax3.stock_img() # add the relief
    ax3.scatter(np.array(lon),np.array(lat),
               s= 150,
               facecolor = marker[0],
               marker = marker[1],
               zorder = 10,
               transform=ccrs.PlateCarree())



    # Spectral analysis

    if not 'age' in ts.keys() and not 'year' in ts.keys():
        print("No age or year information available, skipping spectral analysis")
    else:
        ax4 = fig.add_subplot(gs[1,2])
        if 'depth' in x_label.lower():
            if 'age' in ts.keys() and 'year' in ts.keys():
                print("Both age and year information are available.")
                x_axis = input("Which one would you like to use? ")
                if x_axis.lower() != "year" and x_axis.lower() != "age":
                    raise ValueError("Enter either 'age' or 'year'")
            elif 'age' in ts.keys():
                x_axis = 'age'
            elif 'year' in ts.keys():
                x_axis = 'year'
            y = np.array(ts['paleoData_values'], dtype = 'float64')
            x, label = lipdutils.checkXaxis(ts, x_axis=x_axis)
            y,x = analysis.clean_ts(y,x)

    # Perform the analysis
        default = {'tau':None,
                           'freqs': None,
                           'c':1e-3,
                           'nproc':8,
                           'nMC':200,
                           'detrend':'no',
                           'params' : ["default",4,0,1],
                           'gaussianize': False,
                           'standardize':True,
                           'Neff':3,
                           'anti_alias':False,
                           'avgs':1,
                           'method':'Kirchner_f2py',
                           }
        psd, freqs, psd_ar1_q95, psd_ar1 = spectral.wwz_psd(y,x,**default)

        # Make the plot
        ax4.plot(1/freqs, psd, linewidth=1,  label='PSD', color = marker[0])
        ax4.plot(1/freqs, psd_ar1_q95, linewidth=1,  label='AR1 95%', color=sns.xkcd_rgb["pale red"])
        plt.ylabel('Spectral Density')
        plt.xlabel('Period ('+\
                    x_label[x_label.find("(")+1:x_label.find(")")][0:x_label.find(" ")-1]+')')

        plt.xscale('log', nonposx='clip')
        plt.yscale('log', nonposy='clip')

        ax4.set_aspect('equal')

        plt.gca().invert_xaxis()
        plt.legend()

    #Add the metadata
    textstr = "archiveType: " + metadata["archiveType"]+"\n"+"\n"+\
              "Authors: " + metadata["authors"]+"\n"+"\n"+\
              "Year: " + metadata["Year"]+"\n"+"\n"+\
              "DOI: " + metadata["DOI"]+"\n"+"\n"+\
              "Variable: " + metadata["Variable"]+"\n"+"\n"+\
              "units: " + metadata["units"]+"\n"+"\n"+\
              "Climate Interpretation: " +"\n"+\
              "    Climate Variable: " + metadata["Climate_Variable"] +"\n"+\
              "    Detail: " + metadata["Detail"]+"\n"+\
              "    Seasonality: " + metadata["Seasonality"]+"\n"+\
              "    Direction: " + metadata["Interpretation_Direction"]+"\n \n"+\
              "Calibration: \n" + \
              "    Equation: " + metadata["Calibration_equation"] + "\n" +\
              "    Notes: " + metadata["Calibration_notes"]
    plt.figtext(0.7, 0.4, textstr, fontsize = 12)

    #Save the figure if asked
    if saveFig == True:
        name = 'plot_timeseries_'+ts["dataSetName"]+\
            "_"+y_label
        lipdutils.saveFigure(name,format,dir)
    else:
        plt.show()

    return fig

"""
Statistics
"""

def statsTs(ts=None):
    """ Calculate simple statistics of a timeseries

    Args
    ----

    ts : object
        system will prompt for one if not given

    Returns
    -------

    the mean, median, min, max, standard deviation and the
    inter-quartile range (IQR) of a timeseries.

    Examples
    --------
     mean, median, min_, max_, std, IQR = pyleo.statsTs(timeseries)

    """
    if ts is None:
        if not 'ts_list' in globals():
            fetchTs()
        ts = lipdutils.getTs(ts_list)

    # get the values
    y = np.array(ts['paleoData_values'], dtype = 'float64')

    mean, median, min_, max_, std, IQR = analysis.simpleStats(y)

    return mean, median, min_, max_, std, IQR

def corrSigTs(ts1 = None, ts2 = None, x_axis = None, \
                 autocorrect = True, autocorrect_param = 1950, interp_method = 'interpolation',\
                 interp_step = None, start = None, end = None, nsim = 1000, \
                 method = 'isospectral', alpha = 0.05):
    """ Estimates the significance of correlations between non IID timeseries.
    Args
    ----

    timeseries1 : object
                 timeseries object. Default is blank.
    timeseries2 : object
             timeseries object. Default is blank.

    x-axis : str
        The representation against which to express the
        paleo-data. Options are "age", "year", and "depth".
        Default is to let the system choose if only one available
        or prompt the user.
    interp_method : str
               If the timeseries are not on the same axis, which
               interpolation method to use. Valid entries are 'interpolation'
               (default) and 'bin'.
    autocorrect : bool
             If applicable, convert age to year automatically.
             If set to False, timeseries objects should have converted time
             axis and updated units label in the dictionary
    autocorrect_param : float
                   Reference for age/year conversion.
    interp_step : float
             the step size. By default, will prompt the user.
    start : float
       Start time/age/depth. Default is the maximum of
       the minima of the two timeseries
    end : float
     End time/age/depth. Default is the minimum of the
     maxima of the two timeseries
    nsim : int
      the number of simulations. Default is 1000
    method : str
        method used to estimate the correlation and significance.
        Available methods include:
        - 'ttest': T-test where the degrees of freedom are corrected for
        the effect of serial correlation \n
        - 'isopersistant': AR(1) modeling of the two timeseries \n
        - 'isospectral' (default): phase randomization of original
        inputs.
        The T-test is parametric test, hence cheap but usually wrong
        except in idyllic circumstances.
        The others are non-parametric, but their computational
        requirements scales with nsim.
    alpha : float
       significance level for critical value estimation. Default is 0.05

    Returns
    -------
    r : float
       correlation between the two timeseries \n
    sig : bool
         Returns True if significant, False otherwise \n
    p : real
       the p-value

    """
    if not ts1:
        if not 'ts_list' in globals():
            fetchTs()
        ts1 = lipdutils.getTs(ts_list)

    if not ts2:
        if not 'ts_list' in globals():
            fetchTs()
        ts2 = lipdutils.getTs(ts_list)


    # Get the first time and paleoData values
    y1 = np.array(ts1['paleoData_values'], dtype = 'float64')
    x1, label1 = lipdutils.checkTimeAxis(ts1, x_axis=x_axis)

    # Get the second one
    y2 = np.array(ts2['paleoData_values'], dtype = 'float64')
    x2, label2 = lipdutils.checkTimeAxis(ts2, x_axis=x_axis)

    #Make sure that the label is the same
    if label1 != label2:
        if autocorrect == True:
            print("Converting year to age...")
            if label1 == 'year':
                x1 = autocorrect_param-x1
                units1 = 'yr BP'
                units2 = ts2[label2+'Units']
                label1 = 'year B.P.'
            elif label2 == 'year':
                x2 = autocorrect_param-x2
                units2 = 'yr BP'
                units1 = ts1[label1+'Units']
        else:
            raise ValueError("The two timeseries share a different time representation")
    else:
        units2 = ts2[label2+'Units']
        units1 = ts1[label1+'Units']

    # Tranform the units if necessary

    if units1 != units2:
        units1_group = lipdutils.timeUnitsCheck(units1)
        units2_group = lipdutils.timeUnitsCheck(units2)
        assert units1_group != 'unknown', 'Units unknown, manual conversion needed'
        assert units2_group != 'unknown', 'Units unknown, manual conversion needed'
        if units1_group == 'undefined':
            if label1 == 'year':
                units1_group = 'year_units'
            elif label1 == 'age':
                units2_group = 'age_units'
        if units2_group == 'undefined':
            if label2 == 'year':
                units2_group = 'year_units'
            elif label2 == 'age':
                units2_group = 'age_units'
        #convert kyr to yr if needed
        if units1_group != units2_group:
            if units1_group == 'kage_units':
                x1 = x1*1000
            if units2_group == 'kage_units':
                x2 = x2*1000

    # Remove NaNs and ordered
    y1,x1 = analysis.clean_ts(y1,x1)
    y2,x2 = analysis.clean_ts(y2,x2)

    #Check that the two timeseries have the same lenght and if not interpolate
    if len(y1) != len(y2):
        print("The two series don't have the same length. Interpolating ...")
        xi1, xi2, interp_values1, interp_values2 = analysis.onCommonAxis(x1,y1,x2,y2,
                                                                     method = interp_method,
                                                                     step = interp_step,
                                                                     start =start,
                                                                     end=end)
    elif min(x1) != min(x2) and max(x1) != max(x2):
        print("The two series don't have the same length. Interpolating ...")
        xi1, xi2, interp_values1, interp_values2 = analysis.onCommonAxis(x1,y1,x2,y2,
                                                                     method = interp_method,
                                                                     step = interp_step,
                                                                     start =start,
                                                                     end=end)
    else:
        #xi = x1
        interp_values1 = y1
        interp_values2 = y2

    #Make sure that these vectors are not empty, otherwise return an error
    if np.size(interp_values1) == 0 or np.size(interp_values2) == 0:
        raise ValueError("No common time period between the two time series.")

    r, sig, p = analysis.corrsig(interp_values1,interp_values2,nsim=nsim,
                                 method=method,alpha=alpha)

    return r, sig, p

"""
Timeseries manipulation
"""

def binTs(timeseries = None, x_axis = None, bin_size = None, \
          start = None, end = None):
    """Bin the paleoData values of the timeseries

    Args
    ----
        timeseries : str
                    By default, will prompt the user for one.
        x-axis : str
                The representation against which to plot the paleo-data.
                Options are "age", "year", and "depth". Default is to let the
                system  choose if only one available or prompt the user.
        bin_size : float
                  the size of the bins to be used. By default,
                  will prompt for one
        start (float): Start time/age/depth. Default is the minimum
        end (float): End time/age/depth. Default is the maximum

    Returns
    -------

    binned_values : list
                   the binned output
    bins : int
          the bins (centered on the median, i.e. the 100-200 bin is 150),\n
    n : list
       number of data points in each bin
    error : float
           the standard error on the mean in each bin\n

    """
    if not timeseries:
        if not 'ts_list' in globals():
            fetchTs()
        timeseries = lipdutils.getTs(ts_list)

    # Get the values
    y = np.array(timeseries['paleoData_values'], dtype = 'float64')
    x, label = lipdutils.checkXaxis(timeseries, x_axis=x_axis)

    #remove nans
    y,x = analysis.clean_ts(y,x)

    #Bin the timeseries:
    bins, binned_values, n, error = analysis.binvalues(x,y, bin_size = bin_size,\
                                                   start = start, end = end)

    return bins, binned_values, n, error

def interpTs(timeseries = None, x_axis = None, interp_step = None,\
             start = None, end = None):
    """Simple linear interpolation

    Simple linear interpolation of the data using the numpy.interp method

    Args
    ----
    timeseries : object
                Default is blank, will prompt for it
    x-axis : str
            The representation against which to plot the paleo-data.
            Options are "age", "year", and "depth". Default is to let the
            system choose if only one available or prompt the user.
    interp_step : float
                 the step size. By default, will prompt the user.
    start : float
           Start year/age/depth. Default is the minimum
    end : float
         End year/age/depth. Default is the maximum
    Returns
    -------
    interp_age : list
                the interpolated age/year/depth according to the end/start
                and time step, \n
    interp_values : list
                   the interpolated values

    """
    if not timeseries:
        if not 'ts_list' in globals():
            fetchTs()
        timeseries = lipdutils.getTs(ts_list)

    # Get the values
    y = np.array(timeseries['paleoData_values'], dtype = 'float64')
    x, label = lipdutils.checkXaxis(timeseries, x_axis=x_axis)

    #remove nans
    y,x = analysis.clean_ts(y,x)

    #Interpolate the timeseries
    interp_age, interp_values = analysis.interp(x,y,interp_step = interp_step,\
                                                  start= start, end=end)

    return interp_age, interp_values

def standardizeTs(timeseries = None, scale = 1, ddof = 0, eps = 1e-3):
    """ Centers and normalizes the paleoData values of a  given time series.

    Constant or nearly constant time series not rescaled.

    Args
    ----

    timeseries : array
                A LiPD timeseries object
    scale : real
           a scale factor used to scale a record to a match a given variance
    ddof : int
          degress of freedom correction in the calculation of the standard deviation
    eps : real
         a threshold to determine if the standard deviation is too close to zero

    Returns
    -------

    z : array
       the standardized time series (z-score), Z = (X - E[X])/std(X)*scale, NaNs allowed \n
    mu : real
        the mean of the original time series, E[X] \n
    sig : real
         the standard deviation of the original time series, std[X] \n

    References


    1. Tapio Schneider's MATLAB code: http://www.clidyn.ethz.ch/imputation/standardize.m
    2. The zscore function in SciPy: https://github.com/scipy/scipy/blob/master/scipy/stats/stats.py

    @author: fzhu
    """
    if not timeseries:
        if not 'ts_list' in globals():
            fetchTs()
        timeseries = lipdutils.getTs(ts_list)

    # get the values
    y = np.array(timeseries['paleoData_values'], dtype = 'float64')

    # Remove NaNs
    y_temp = np.copy(y)
    y = y[~np.isnan(y_temp)]

    #Standardize
    z, mu, sig = analysis.standardize(y,scale=1,axis=None,ddof=0,eps=1e-3)

    return z, mu, sig

def segmentTs(timeseries = None, factor = 2):
    """Divides a time series into several segments using a gap detection algorithm

    Gap detection rule: If the time interval between some two data points is
    larger than some factor times the mean resolution of the timeseries, then
    a brak point is applied and the timseries is divided.

    Args
    ----

    timeseries : object
                a LiPD timeseries object
    factor : float
            factor to adjust the threshold. threshold = factor*dt_mean.
            Default is 2.

    Returns
    -------

    seg_y : list
           a list of several segments with potentially different length
    seg_t : list
           A list of the time values for each y segment.
    n_segs : int
            the number of segments


    """

    if not timeseries:
        if not 'ts_list' in globals():
            fetchTs()
        timeseries = lipdutils.getTs(ts_list)

    # Get the values
    # Raise an error if age or year not in the keys
    if not 'age' in timeseries.keys() and not 'year' in timeseries.keys():
        raise ValueError("No time information available")
    elif 'age' in timeseries.keys() and 'year' in timeseries.keys():
        print("Both age and year information are available.")
        x_axis = input("Which one would you like to use? ")
        if x_axis.lower() != "year" and x_axis.lower() != "age":
            raise ValueError("Enter either 'age' or 'year'")
    elif 'age' in timeseries.keys():
        x_axis = 'age'
    elif 'year' in timeseries.keys():
        x_axis = 'year'

    # Get the values
    ys = np.array(timeseries['paleoData_values'], dtype = 'float64')
    ts, label = lipdutils.checkXaxis(timeseries, x_axis=x_axis)

    # remove NaNs
    ys,ts = analysis.clean_ts(ys,ts)

    #segment the timeseries
    seg_y, seg_t, n_segs = analysis.ts2segments(ys, ts, factor)

    return seg_y, seg_t, n_segs

#"""
# Spectral and Wavelet Analysis
#"""

def wwzTs(timeseries = None, lim = None, wwz = False, psd = True, wwz_default = True,
          psd_default = True, fig = True, wwaplot_default = True, psdplot_default = True,
          saveFig = False, dir = None, format = "eps"):
    """Weigthed wavelet Z-transform analysis

    Wavelet analysis for unevenly spaced data adapted from Foster et al. (1996)

    Args
    ----
    timeseries : dict
                A LiPD timeseries object (Optional, will prompt for one.)
    lim : list
         Truncate the timeseries between min/max time (e.g., [0,10000])
    wwz : bool
         If True, will perform wavelet analysis
    psd : bool
         If True, will inform the power spectral density of the timeseries
    wwz_default : bool
                 If True, will use the following default parameters:
                 wwz_default = {'tau':None,
                               'freqs':None,
                               'c':1/(8*np.pi**2),
                               'Neff':3,
                               'Neff_coi':3,
                               'nMC':200,
                               'nproc':8,
                               'detrend':False,
                               'params' : ["default",4,0,1],
                               'gaussianize': False,
                               'standardize':True,
                               'method':'Kirchner_f2py',
                               'bc_mode':'reflect',
                               'reflect_type':'odd',
                               'len_bd':0}
                 Modify the values for specific keys to change the default behavior.
                 See spectral.wwz for details

    psd_default : bool
                If True, will use the following default parameters:
                psd_default = {'tau':None,
                           'freqs': None,
                           'c':1e-3,
                           'nproc':8,
                           'nMC':200,
                           'detrend':False,
                           'params' : ["default",4,0,1],
                           'gaussianize': False,
                           'standardize':True,
                           'Neff':3,
                           'anti_alias':False,
                           'avgs':2,
                           'method':'Kirchner_f2py',
                           }

                Modify the values for specific keys to change the default behavior.
                See spectral.wwz_psd for details
    fig : bool
          If True, plots the figure
    wwaplot_default : bool
                     If True, will use the following default parameters:
                     wwaplot_default={'AR1_q':AR1_q,
                                      'coi':coi,
                                      'levels':None,
                                      'tick_range':None,
                                      'yticks':None,
                                      'yticks_label': None,
                                      'ylim':None,
                                      'xticks':None,
                                      'xlabels':None,
                                      'figsize':[20,8],
                                      'clr_map':'OrRd',
                                      'cbar_drawedges':False,
                                      'cone_alpha':0.5,
                                      'plot_signif':True,
                                      'signif_style':'contour',
                                      'plot_cone':True,
                                      'title':None,
                                      'ax':None,
                                      'xlabel': the chondata label,
                                      'ylabel': 'Period (units from ChronData)',
                                      'plot_cbar':'True',
                                      'cbar_orientation':'vertical',
                                      'cbar_pad':0.05,
                                      'cbar_frac':0.15,
                                      'cbar_labelsize':None}

                     Modify the values for specific keys to change the default behavior.
    psdplot_default : bool
                     If True, will use the following default parameters:
                           psdplot_default={'lmstyle':'-',
                                            'linewidth':None,
                                             'color': sns.xkcd_rgb["denim blue"],
                                             'ar1_lmstyle':'-',
                                             'ar1_linewidth':1,
                                             'period_ticks':None,
                                             'period_tickslabel':None,
                                             'psd_lim':None,
                                             'period_lim':None,
                                             'alpha':1,
                                             'figsize':[20,8],
                                             'label':'PSD',
                                             'plot_ar1':True,
                                             'psd_ar1_q95':95% quantile from psd,
                                             'title': None,
                                             'legend': 'True'
                                             'psd_ar1_color':sns.xkcd_rgb["pale red"],
                                             'ax':None,
                                             'vertical':False,
                                             'plot_gridlines':True,
                                             'period_label':'Period (units of age)',
                                             'psd_label':'Spectral Density',
                                             'zorder' : None}

                     Modify the values for specific keys to change the default behavior.

    saveFig : bool
             default is to not save the figure
    dir : str
         the full path of the directory in which to save the figure.
         If not provided, creates a default folder called 'figures' in the
         LiPD working directory (lipd.path).
    format : str
            One of the file extensions supported by the active
            backend. Default is "eps". Most backend support png, pdf, ps, eps,
            and svg.

    Returns
    -------


    dict_out : dict
              A dictionary of outputs.

    For wwz:

    - wwa : array
           The weights wavelet amplitude

    - AR1_q : array
             AR1 simulations

    - coi : array
           cone of influence

    - freqs : array
             vector for frequencies

    - tau : array
           the evenly-spaced time points, namely the time
           shift for wavelet analysis.

    - Neffs : array
             The matrix of effective number of points in the
             time-scale coordinates.

    - coeff : array
             The wavelet transform coefficients

    For psd :

    - psd : array
           power spectral density

    - freqs : array
             vector of frequency

    - psd_ar1_q95 : array
                   the 95% quantile of the psds of AR1 processes

    fig : The figure

    References
    ----------
    Foster, G. (1996). Wavelets for period analysis of unevenly
    sampled time series. The Astronomical Journal, 112(4), 1709-1729.

    Examples
    --------
    To run both wwz and psd:

    >>> dict_out, fig = pyleoclim.wwzTs(wwz=True)

    Note: This will return a single figure with wwa and psd

    To change a default behavior:

    >>> dict_out, fig = pyleoclim.wwzTs(psd_default = {'nMC':1000})

    """

    # Make sure there is something to compute
    if wwz is False and psd is False:
        raise ValueError("Set 'wwz' and/or 'psd' to True")

    # Get a timeseries
    if not timeseries:
        if not 'ts_list' in globals():
            fetchTs()
        timeseries = lipdutils.getTs(ts_list)

    # Raise an error if age or year not in the keys
    ts, label = lipdutils.checkTimeAxis(timeseries)

    # Set the defaults
    #Make sure the default have the proper type
    if psd_default is not True and type(psd_default) is not dict:
        raise TypeError('The default for the psd calculation should either be provided'+
                 ' as a dictionary or set to True')
    if psdplot_default is not True and type(psdplot_default) is not dict:
        raise TypeError('The default for the psd figure should either be provided'+
                 ' as a dictionary or  set to True')
    if wwz_default is not True and type(wwz_default) is not dict:
        raise TypeError('The default for the wwz calculation should either be provided'+
                 ' as a dictionary or  set to True')
    if wwaplot_default is not True and type(wwaplot_default) is not dict:
        raise TypeError('The default for the wwa figure should either be provided'+
                 ' as a dictionary or set to True')

    # Get the values
    ys = np.array(timeseries['paleoData_values'], dtype = 'float64')

    # remove NaNs
    ys,ts = analytis.clean_ts(ys,ts)

    # Truncate the timeseries if asked
    if lim != None:
        idx_low = np.where(ts>=lim[0])[0][0]
        idx_high = np.where(ts<=lim[1])[0][-1]
        ts = ts[idx_low:idx_high]
        ys = ys[idx_low:idx_high]

    #Get the time units
    s = timeseries[label+"Units"]
    ageunits = s[0:s.find(" ")]

    # Perform the calculations
    if psd is True and wwz is False: # PSD only
        if psd_default == True:
            psd, freqs, psd_ar1_q95, psd_ar1 = spectral.wwz_psd(ys, ts)
        elif type(psd_default) is dict:
            psd, freqs, psd_ar1_q95, psd_ar1 = spectral.wwz_psd(ys, ts, **psd_default)
        else:
            raise TypeError('Options for psd calculation must be passed as a dictionary')
        # Wrap up the output dictionary
        dict_out = {'psd':psd,
               'freqs':freqs,
               'psd_ar1_q95':psd_ar1_q95,
               'psd_ar1':psd_ar1}

        # Plot if asked
        if fig is True:
            if psdplot_default == True:
                psdplot_default={'ar1_linewidth':1,
                                 'plot_ar1':True,
                                 'psd_ar1_q95':psd_ar1_q95,
                                 'period_label':'Period ('+ageunits+')'}

            if type(psdplot_default) == dict: #necessary since not same defaults
                if 'ar1_linewidth' not in psdplot_default.keys():
                    psdplot_default['ar1_linewidth'] =1
                if 'plot_ar1' not in psdplot_default.keys():
                    psdplot_default['plot_ar1'] = True
                if 'psd_ar1_q95' not in psdplot_default.keys():
                    psdplot_default['psd_ar1_q95'] = psd_ar1_q95
                if 'period_label' not in psdplot_default.keys():
                    psdplot_default['period_label'] = 'Period ('+ageunits+')'

            else:
                raise TypeError('Options for psd plot must be passed as a dictionary')

            fig = spectral.plot_psd(psd,freqs,**psdplot_default)

            if saveFig is True:
                lipdutils.saveFigure(timeseries['dataSetName']+'_PSDplot',format,dir)
            else:
                plt.show()

        else:
            fig = None

    elif psd is False and wwz is True: #WWZ only
        # Set default
        if wwz_default == True:
            #Perform the calculation
            wwa, phase, AR1_q, coi, freqs, tau, Neffs, coeff = spectral.wwz(ys,ts)

        elif type(wwz_default) is dict:
            #Perform the calculation
            wwa, phase, AR1_q, coi, freqs, tau, Neffs, coeff = spectral.wwz(ys,ts, **wwz_default)

        else:
            raise TypeError('Options for wwz calculation must be passed as a dictionary')

        #Wrap up the output dictionary
        dict_out = {'wwa':wwa,
                    'phase':phase,
                    'AR1_q':AR1_q,
                    'coi':coi,
                    'freqs':freqs,
                    'tau':tau,
                    'Neffs':Neffs,
                    'coeff':coeff}

        #Plot if asked
        if fig is True:
            # Set the plot default
            if wwaplot_default == True:
                wwaplot_default = {'AR1_q':AR1_q,
                                   'coi':coi,
                                   'plot_signif':True,
                                   'plot_cone':True,
                                   'xlabel': label,
                                   'ylabel': 'Period ('+ageunits+')'}

            elif type(wwaplot_default) is dict: #necessary since not same defaults
                if 'AR1_q' not in wwaplot_default:
                    wwaplot_default['AR1_q'] = AR1_q
                if 'coi' not in wwaplot_default:
                    wwaplot_default['coi']=coi
                if 'plot_signif' not in wwaplot_default:
                    wwaplot_default['plot_signif'] = True
                if 'xlabel' not in wwaplot_default:
                    wwaplot_default['xlabel'] = s
                if 'ylabel' not in wwaplot_default:
                    wwaplot_default['ylabel'] = 'Period ('+ageunits+')'

            else:
                raise TypeError('Options for wwz plot must be passed as a dictionary')

            fig = spectral.plot_wwa(wwa, freqs, tau, **wwaplot_default)

            if saveFig is True:
                lipdutils.saveFigure(timeseries['dataSetName']+'_PSDplot',format,dir)
            else:
                plt.show()
        else:
            fig = None

    elif psd is True and wwz is True: # perform both

        # PSD calculations
        if psd_default == True:
            psd, freqs, psd_ar1_q95, psd_ar1 = spectral.wwz_psd(ys, ts)
        elif type(psd_default) is dict:
            psd, freqs, psd_ar1_q95, psd_ar1 = spectral.wwz_psd(ys, ts, **psd_default)
        else:
            raise TypeError('Options for psd calculation must be passed as a dictionary')

        #WWZ calculations
        if wwz_default == True:
            #Perform the calculation
            wwa, phase, AR1_q, coi, freqs, tau, Neffs, coeff = spectral.wwz(ys,ts)

        elif type(wwz_default) is dict:
            #Perform the calculation
            wwa, phase, AR1_q, coi, freqs, tau, Neffs, coeff = spectral.wwz(ys,ts, **wwz_default)

        else:
            raise TypeError('Options for wwz calculation must be passed as a dictionary')

        #Wrap up the output dictionary
        dict_out = {'wwa':wwa,
                    'phase':phase,
                    'AR1_q':AR1_q,
                    'coi':coi,
                    'freqs':freqs,
                    'tau':tau,
                    'Neffs':Neffs,
                    'coeff':coeff,
                    'psd':psd,
                    'psd_ar1_q95':psd_ar1_q95,
                    'psd_ar1':psd_ar1}

        # Make the plot if asked
        if fig is True:
            #Figure out the figure size
            if type(wwaplot_default) is dict and type(psdplot_default)is dict:
                if 'figsize' in wwaplot_default.keys():
                    figsize = wwaplot_default['figsize']
                elif 'figsize' in psdplot_default.keys():
                    figsize = psdplot_default['figsize']
                else: figsize = [20,8]
            elif type(wwaplot_default) is dict:
                if 'figsize' in wwaplot_default.keys():
                    figsize = wwaplot_default['figsize']
                else:
                    figsize = [20,8]
            elif type(psdplot_default) is dict:
                if 'figsize' in psdplot_default.keys():
                    figsize = psdplot_default['figsize']
                else:
                    figsize = [20,8]
            else: figsize = [20,8]


            fig = plt.figure(figsize = figsize)
            ax1 = plt.subplot2grid((1,3),(0,0), colspan =2)

            if wwaplot_default == True:
                wwaplot_default = {'AR1_q':AR1_q,
                                   'coi':coi,
                                   'plot_signif':True,
                                   'plot_cone':True,
                                   'xlabel': label,
                                   'ylabel': 'Period ('+ageunits+')',
                                   'ax':ax1}

            elif type(wwaplot_default) is dict: #necessary since not same defaults
                if 'AR1_q' not in wwaplot_default:
                    wwaplot_default['AR1_q'] = AR1_q
                if 'coi' not in wwaplot_default:
                    wwaplot_default['coi']=coi
                if 'plot_signif' not in wwaplot_default:
                    wwaplot_default['plot_signif'] = True
                if 'xlabel' not in wwaplot_default:
                    wwaplot_default['xlabel'] = s
                if 'ylabel' not in wwaplot_default:
                    wwaplot_default['ylabel'] = 'Period ('+ageunits+')'
                if 'ax' not in wwaplot_default:
                    wwaplot_default['ax'] = ax1

            else:
                raise TypeError('Options for wwz plot must be passed as a dictionary')


            spectral.plot_wwa(wwa, freqs, tau, **wwaplot_default)

            ax2 = plt.subplot2grid((1,3),(0,2))

            if psdplot_default == True:
                psdplot_default={'ar1_linewidth':1,
                                 'plot_ar1':True,
                                 'psd_ar1_q95':psd_ar1_q95,
                                 'period_label':'Period ('+ageunits+')',
                                 'ax': ax2}

            if type(psdplot_default) is dict: #necessary since not same defaults
                if 'ar1_linewidth' not in psdplot_default.keys():
                    psdplot_default['ar1_linewidth'] =1
                if 'plot_ar1' not in psdplot_default.keys():
                    psdplot_default['plot_ar1'] = True
                if 'psd_ar1_q95' not in psdplot_default.keys():
                    psdplot_default['psd_ar1_q95'] = psd_ar1_q95
                if 'period_label' not in psdplot_default.keys():
                    psdplot_default['period_label'] = 'Period ('+ageunits+')'
                if 'ax' not in psdplot_default.keys():
                    psdplot_default['ax'] = ax2

            else:
                raise TypeError('Options for psd plot must be passed as a dictionary')

            spectral.plot_psd(psd,freqs,**psdplot_default)

            if saveFig is True:
                lipdutils.saveFigure(timeseries['dataSetName']+'_PSDplot',format,dir)
            else:
                plt.show()
        else:
            fig = None

    return dict_out, fig

## Cross wavelet transform
def xwcTs(timeseries1 = None, timeseries2 = None, lim= None, x_axis = None,
          autocorrect = True, autocorrect_param =1950, xwc_default = True,
          fig = True, xwcplot_default = True,
          saveFig = False, dir = None, format = "eps"):
    """Cross Wavelet transform of two timeseries

    Args
    ----

    timeseries1 : dict
                 a LiPD timeseries object (Optional, will prompt for one)
    timseries2 : dict
                 a LiPD timeseries object (Optional, will prompt for one)
    lim : list
         Truncate the timeseries between min/max time (e.g., [0,10000])
    x-axis : str
            The representation against which to express the
            paleo-data. Options are "age", "year", and "depth".
            Default is to let the system choose if only one available
            or prompt the user.
    autocorrect : bool
                 If applicable, convert age to year automatically.
                 If set to False, timeseries objects should have converted time
                 axis and updated units label in the dictionary
    autocorrect_param : float
                       Reference for age/year conversion.
    xwt_default : bool
                 If True, will use the following default parameters
                 xwt_default = {'tau': None,
                                'feqs': None,
                                'c': 1/(8*np.pi**2),
                                'Neff': 3,
                                'Neff_coi': 6,
                                'nproc': 8,
                                'detrend': False,
                                'params': ['default', 4, 0, 1],
                                'gaussianize': False,
                                'standardize':True,
                                'method':'Kirchner_f2py'}
                 Modify the values for specific keys to change the default behavior.
                 See spectral.xwt for details
    fig : bool
         If True, plots the figure
    xwcplot_default : bool
                     If True, will use the following default parameters:

                     wwaplot_default={'pt':0.5,
                                      'levels':None,
                                      'tick_range':None,
                                      'basey':2,
                                      'yticks': None,
                                      'ylime':None,
                                      'xticks':None,
                                      'xlabels':None,
                                      'figsize':[20,8],
                                      'clr_map':'OrRd',
                                      'skip_x':5,
                                      'skip_y':5,
                                      'scale':30,
                                      'width':0.004,
                                      'cbar_drawedges':False
                                      'cone_alpha':0.5,
                                      'plot_signif':True,
                                      'signif_style':'contour'
                                      'title':None,
                                      'plot_cone':True,
                                      'ax':None,
                                      'xlabel':Age representation,
                                      'ylabel': "Period (year)",
                                      'cbar_orientation':'vertical',
                                      'cbar_pad':0.05,
                                      'cbar_frac':0.15,
                                      'cbar_labelsize':None
                                      }
    saveFig (bool) : bool
                    default is to not save the figure
    dir : str
         the full path of the directory in which to save the figure.
         If not provided, creates a default folder called 'figures' in the
         LiPD working directory (lipd.path).
    format : str
            One of the file extensions supported by the active
            backend. Default is "eps". Most backend support png, pdf, ps, eps,
            and svg.

    Returns
    -------
    res : dict
         contains the cross wavelet coherence, cross-wavelet phase,
         vector of frequency, evenly-spaced time points, AR1 sims, cone of influence

    fig : Figure

    """
    #Get timeseries
    if not timeseries1:
        if not 'ts_list' in globals():
            fetchTs()
        timeseries1 = lipdutils.getTs(ts_list)
    if not timeseries2:
        if not 'ts_list' in globals():
            fetchTs()
        timeseries2 = lipdutils.getTs(ts_list)

    # Get the first time and paleoData values
    y1 = np.array(timeseries1['paleoData_values'], dtype = 'float64')
    x1, label1 = lipdutils.checkTimeAxis(timeseries1, x_axis=x_axis)

    # Get the second one
    y2 = np.array(timeseries2['paleoData_values'], dtype = 'float64')
    x2, label2 = lipdutils.checkTimeAxis(timeseries2, x_axis=x_axis)

    #Make sure that the label is the same
    if label1 != label2:
        if autocorrect == True:
            print("Converting year to age...")
            if label1 == 'year':
                x1 = autocorrect_param-x1
                units1 = 'yr BP'
                units2 = timeseries2[label2+'Units']
                label1 = 'year B.P.'
            elif label2 == 'year':
                x2 = autocorrect_param-x2
                units2 = 'yr BP'
                units1 = timeseries1[label1+'Units']
        else:
            raise ValueError("The two timeseries share a different time representation")
    else:
        units2 = timeseries2[label2+'Units']
        units1 = timeseries1[label1+'Units']

    # Tranform the units if necessary

    if units1 != units2:
        units1_group = lipdutils.timeUnitsCheck(units1)
        units2_group = lipdutils.timeUnitsCheck(units2)
        assert units1_group != 'unknown', 'Units unknown, manual conversion needed'
        assert units2_group != 'unknown', 'Units unknown, manual conversion needed'
        if units1_group == 'undefined':
            if label1 == 'year':
                units1_group = 'year_units'
            elif label1 == 'age':
                units2_group = 'age_units'
        if units2_group == 'undefined':
            if label2 == 'year':
                units2_group = 'year_units'
            elif label2 == 'age':
                units2_group = 'age_units'
        #convert kyr to yr if needed
        if units1_group != units2_group:
            if units1_group == 'kage_units':
                x1 = x1*1000
                label1 = 'age'
                units1 = 'yr  BP'
            if units2_group == 'kage_units':
                x2 = x2*1000
                label2 = 'age'
                units2 = 'yr BP'

    # Remove NaNs and ordered
    y1,x1 = analysis.clean_ts(y1,x1)
    y2,x2 = analysis.clean_ts(y2,x2)

    #Check that the timeseries are on a common axis
    if lim == None:
        xi1, xi2, interp_values1, interp_values2 = analysis.onCommonAxis(x1,y1,x2,y2,
                                                                       method=None)
    else:
        if type(lim) != list:
            raise TypeError('The time series limits should be of type list')
        xi1, xi2, interp_values1, interp_values2 = analysis.onCommonAxis(x1,y1,x2,y2,
                                                                       start=lim[0],
                                                                       end=lim[1])
    #perform the cross-wavelet analysis
    if xwc_default == True:
        res = spectral.xwc(interp_values1, xi1, interp_values2,xi2)
    elif type(xwc_default) is dict:
        res = spectral.xwc(interp_values1, xi1, interp_values2,xi2, **xwc_default)
    else:
        raise TypeError('Options for the x-wavelet calculation must be passed as a dictionary')


    # Figure if asked
    if fig == True:
        xwcplot_default={'plot_signif': True,
                         'plot_cone':True,
                         'xlabel': units1,
                         'ylabel':'Period (years)'}
        if type(xwcplot_default) == dict:
            if 'plot_signif' not in xwcplot_default:
                xwcplot_default['plot_signif']=True
            if 'plot_cone' not in xwcplot_default:
                xwcplot_default['plot_cone']=True
            if 'xlabel' not in xwcplot_default:
                xwcplot_default['xlabel']=units1
            if 'ylabel' not in xwcplot_default:
                xwcplot_default['ylabel']='Period (years)'
        else:
            raise TypeError('Options for the x-wavelet plot must be passed as a dictionary')

        fig = spectral.plot_coherence(res,**xwcplot_default)

        if saveFig is True:
            lipdutils.saveFigure(timeseries1['dataSetName']+'_'+\
                                 timeseries2['dataSetName']+\
                                 '_coherenceplot',format,dir)
        else:
            plt.show()

    else:
        fig = None

    return res, fig

"""
Age model
"""

def Bchron(lipd, modelNum = None, objectName = None, rejectAges = None,\
           calCurves = None, reservoirAgeCorr = None, predictPositions = "paleo",\
           positionsThickness = None, outlierProbs =None, iterations =1000,\
           burn = 2000, thin = 8, extractDate = 1950-datetime.datetime.now().year,\
           maxExtrap = 500, thetaMhSd = 0.5, muMhSd = 0.1, psiMhSd = 0.1,\
           ageScaleVal = 1000, positionScaleVal = 100, saveLipd = True,\
           plot_age = True, figsize = [4,8], flipCoor = False,xlabel = None, ylabel = None,
           xlim = None, ylim = None, violinColor = '#8B008B',\
           medianLineColor = "black", medianLineWidth = 2.0,\
           CIFillColor = "Silver", samplePaths = True, samplePathNumber =10,\
           alpha = 0.5, saveFig = False, dir = None, format = "eps"):
    """ Runs Bchron and plot if asked

    Fits a non-parametric chronology model to age/position data according to
    the Compound Poisson-Gamma model defined by Haslett and Parnell (2008).
    This version used a slightly modified Markov chain Monte-Carlo fitting
    algorithm which aims to converge quicker and requires fewer iterations.
    It also a slightly modified procedure for identifying outliers.

    The Bchronology functions fits a compounf Poisson-Gamma distribution to the
    incrememnts between the dated levels. This involves a stochastic linear
    interpolation step where the age gaps are Gamma distributed, and the position
    gaps are Exponential. Radiocarbon and non-radiocarbon dates (including outliers)
    are updated within the fucntion also by MCMC.

    This function also allows to save the ensemble, distributions, and probability
    tables as well as the parameters with which the model was run into the LiPD file.

    Finally allows to make a plot.

    Args
    ----

    lipd : dict
          A dictionary containing the entry of a LiPD file. Can be
          obtained from lipd.readLipd() or pyleoclim.openLipd(). Please note
          that the Bchron function currently only allows for a single LiPD file
          (i.e., not the entire directory).
    modelNum : int
              The model number in which to place the Bchron output.
              If None, the function will create a new model.
    objectName : str
                The name of the chron object in which to store the new
                model (e.g. "chron0"). If modelNum is selected, objectName
                should be provided
    rejectAges : vector
                A vector of 1/0 where 1 include the dates to be rejected.
                Default it None.
    calCurves : list(Optional)
               A vector of values containing either 'intcal13',
              'marine13', 'shcal13', or 'normal'. If none is provided, will
               prompt the user. Should be either of length =1 if using the same
               calibration for each age or the same length as the vector of ages.
               reservoirAgeCorr (array): (Optional) A list (matrix) of two floats that correspond to the
               DeltaR and DeltaR uncertainty. If already added to the ages and
               ages standard deviation, then enter [0,0] to bypass the prompt.
               Will only be applied if CalCurves is set to 'marine13'. Otherwise,
               leave to none.
    predictPositions : vector(optional)
                      a vector of positions
                     (e.g. depths) at which predicted age values are required.
                     Defaults to a sequence of length 100 from the top position to the
                     bottom position.
    positionsThicknes : array(Optional)
                       Thickness values for each of the positions.
                       The thickness values should be the full thickness value of the
                       slice. By default set to zero.
    outlierProbs : array
                  A vector of prior outlier probabilities,
                  one for each age. Defaults to 0.01
    iterations : int(Optional)
                The number of iterations to start the procedure.
        Default and minimum should be 10000.
    burn : int(Optional)
          The number of starting iterations to discard.
          Default is 200
    thin : int(Optional)
          The step size for every iteration to keep beyond
          the burnin. Default is 8.
    extractDate : float(Optional)
                 The top age of the core. Used for
                 extrapolation purposes so that no extrapolated ages go beyond the
                 top age of the core. Defaults to the current year.
    maxExtrap : int(Optional)
               The maximum number of extrapolations to
               perform before giving up and setting the predicted ages to NA.
               Useful for when large amounts of extrapolation are required, i.e.
               some of the predictPositions are a long way from the dated
               positions. Defaults to 500.
    thetaMhSd : float(Optional)
               The Metropolis-Hastings standard
               deviation for the age parameters. Defaults to 0.5.
    muMhSd : float(Optional)
            The Metropolis-Hastings standard deviation
            for the compound Poisson-Gamma Scale. Defaults to 0.1
    psiMhSd : float(Optional)
             The Metropolis-Hastings standard deviation
             for the Compound Poisson-Gamma Scale.
    ageScaleVal : int(Optional)
                 A scale value for the ages.
                 Bchronology works best when the ages are scaled to be
                 approximately between 0 and 100.
                 The default value is thus 1000 for ages given in years.
    positionScaleVal : int(Optional)
                      A scale value for the positions.
                      Bchronology works best when the positions are scaled to be
                      approximately between 0 and 100. The default value is thus
                      100 for positions given in cm.
    saveLipd : bool
              If True, saves the ensemble, distribution, and probability
              tables along with the parameters used to run the model in the LiPD
              file.
    plot_age : bool
              If True, makes a plot for the chronology
    figsize : list
             The figure size. Default is [4,8]
    flipCoor : bool
              If True, plots depth on the y-axis.
    xlabel : str
            The label for the x-axis
    ylabel : str
            The label for the y-axis
    xlim : list
          Limits for the x-axis. Default corresponds to the min/max
          of the depth vector.
    ylim : list
          Limits for the y-axis. Default set by matplotlib
    violinColor : str
                 The color for the violins. Default is purple
    medianLineColor : str
                     The color for the median line. Default is black.
    medianLineWidth : float
                     The width for the median line
    CIFillColor : str
                 Fill color in between the 95% confidence interval.
                 Default is silver.
    samplePaths : bool
                 If True, draws sample paths from the distribution.
                 Use the same color as the violins.
    samplePathNumber : int
                      The number of sample paths to draw. Default is 10.
                      Note: samplePaths need to be set to True.
    alpha : float
           The violins' transparency. Number between 0 and 1
    saveFig : bool
             default is to not save the figure
    dir : str
         the full path of the directory in which to save the figure.
         If not provided, creates a default folder called 'figures' in the
         LiPD working directory (lipd.path).
    format : str
            One of the file extensions supported by the active
            backend. Default is "eps". Most backend support png, pdf, ps, eps,
            and svg.

    Returns
    -------
    depth : float
           the predicted positions (either same as the user or the default)
    chron : array
           a numpy array of possible chronologies in each column.
           The number of rows is the same as the length of depth
    ageDist : list
             the distribution of ages around each dates.
    fig : the figure
    run : object
         the full R object containing the outputs of the Bchron run

    Warnings
    --------
    - This function requires R and the Bchron package and all its
      dependencies to be installed on the same machine.

    References
    ----------
    - Haslett, J., and Parnell, A. C. (2008). A simple monotone
    process with application to radiocarbon-dated depth
    chronologies. Journal of the Royal Statistical Society,
    Series C, 57, 399-418. DOI:10.1111/j.1467-9876.2008.00623.x
    - Parnell, A. C., Haslett, J., Allen, J. R. M., Buck, C. E.,
    and Huntley, B. (2008). A flexible approach to assessing
    synchroneity of past events using Bayesian reconstructions
    of sedimentation history. Quaternary Science Reviews,
    27(19-20), 1872-1885. DOI:10.1016/j.quascirev.2008.07.009

    """

    # Get the csv_list
    csv_dict = lpd.getCsv(lipd)
    # Get the list of possible measurement tables
    chronMeasurementTables, paleoMeasurementTables = lipdutils.isMeasurement(csv_dict)
    #Check that there is a measurement table or exit
    if not chronMeasurementTables:
        raise ValueError("No ChronMeasurementTables available to run BChron!")
    # Selct measurement table
    csvName = lipdutils.whichMeasurement(chronMeasurementTables, csv_dict)
    # Get the ts-like object from selected measurement table
    ts_list = lipdutils.getMeasurement(csvName, lipd)
    # Make sure there is no model associated with the choice
    if not modelNum and not objectName:
        model, objectName = lipdutils.isModel(csvName, lipd)
        modelNum = lipdutils.modelNumber(model)
    elif modelNum and not objectName:
        raise ValueError("You must provide a DataObject when specifying a model.")
    ## look for the inputs for Bchron
    # Find an age column
    print("Looking for age data...")
    match = lipdutils.searchVar(ts_list,["radiocarbon","age14C"])
    if not match:
        raise ValueError("No age data available")
    ages = ts_list[match]['values']
    ages = np.array(ages,dtype='float64')
    # Remove NaNs (can happen in mixed chronologies)
    idx = np.where(~np.isnan(ages))[0]
    ages = ages[idx]
    if "units" in ts_list[match].keys():
        agesUnit = ts_list[match]['units']
    else:
        agesUnit =[]
    print("Age data found.")

    # Find a depth column
    print("Looking for a depth/position column...")
    match = lipdutils.searchVar(ts_list,["depth"])
    if not match:
        raise ValueError("No age data available")
    positions = ts_list[match]['values']
    positions = np.array(positions,dtype='float64')
    positions = positions[idx]
    if "units" in ts_list[match].keys():
        positionsUnits = ts_list[match]['units']
    else:
        positionsUnits = []
    print("Depth information found.")

    # Find the uncertainty
    print("Looking for age uncertainty...")
    match = lipdutils.searchVar(ts_list,["uncertainty"],exact=False)
    if not match:
        raise ValueError("No uncertainty data available")
    agesStd = ts_list[match]['values']
    agesStd = np.array(agesStd,dtype='float64')
    agesStd = agesStd[idx]
    print("Uncertainty data found.")

    # See if there is a column of reject ages
    if rejectAges == True:
        print("Looking for a column of rejected ages...")
        match = lipdutils.searchVar(ts_list,["rejectAges"], exact=False)
        if not match:
            print("No column of rejected ages found.")
            rejectAges = None
            print("No ages rejected.")
        else:
            rejectAges = ts_list[match]['values']
            rejectAges = rejectAges[idx]
            print("Rejected ages found.")

    # Check if there are calibration curves
    if not calCurves:
        print("Looking for calibration curves...")
        match = lipdutils.searchVar(ts_list,["calCurves"], exact=False)
        if not match:
            calCurves = agemodel.chooseCalCurves()
            calCurves = agemodel.verifyCalCurves(calCurves)
            if len(calCurves) == 1 and len(positions)!=1:
                calCurves = list(chain(*[[i]*len(positions) for i in calCurves]))
        else:
            calCurves = ts_list[match]['values']
            calCurves = agemodel.verifyCalCurves(calCurves)
    elif len(calCurves)==1 and len(positions)!=1:
        calCurves = agemodel.verifyCalCurves(calCurves)
        calCurves = list(chain(*[[i]*len(positions) for i in calCurves]))
    else:
        assert len(calCurves) == len(positions)
        calCurves = agemodel.verifyCalCurves(calCurves)
    print("Calibration curves found.")

    #Check for a reservoir age

    if reservoirAgeCorr == None:
        print("Looking for a reservoir age correction.")
        match = lipdutils.searchVar(ts_list,\
                                    ["reservoir","reservoirAge","correction"],\
                                    exact=True)
        if len(match)==1:
            ageCorr = ts_list[match]['values']
            ageCorr = ageCorr[idx]
            print("Reservoir Age correction found.")
            print("Looking for correction uncertainty...")
            match = lipdutils.searchVar(ts_list,["reservoirUncertainty"],\
                                                 exact=True)
            if not match:
                print("No match found.")
                corrU = float(input("Enter a value for the correction uncertainty: "))
                ageCorrStd = corrU*np.ones((len(ageCorr),1))
            else:
                ageCorrStd = ts_list[match]['values']
                ageCorrStd = ageCorrStd[idx]

        else:
            print("No match found.")
            ageCorr, ageCorrStd = agemodel.reservoirAgeCorrection()
        reservoirAgeCorr = np.column_stack((ageCorr,ageCorrStd))
        reservoirAgeCorr = reservoirAgeCorr.flatten()

    elif reservoirAgeCorr == True:
        ageCorr, ageCorrStd = agemodel.reservoirAgeCorrection()
        reservoirAgeCorr = np.column_stack((ageCorr,ageCorrStd))
        reservoirAgeCorr = reservoirAgeCorr.flatten()
    else:
        if type(reservoirAgeCorr)!=np.ndarray:
            if type(reservoirAgeCorr) == list:
                reservoirAgeCorr = np.array(reservoirAgeCorr)
            else:
                raise TypeError("The reservoir age correction should be either None, True or an array.")

    #Predict positions
    if predictPositions == "paleo":
        # Grab the paleomeasurementTables
        paleoCsvName = lipdutils.whichMeasurement(paleoMeasurementTables, csv_dict)
        # Get the various timeseries
        paleots_list = lipdutils.getMeasurement(paleoCsvName, lipd)
        #Look for a depth column
        match = lipdutils.searchVar(paleots_list,["depth"], exact=True)
        if not match:
            print("No paleoDepth information available, using Bchron default")
            predictPositions = None
        else:
            predictPositions = paleots_list[match]['values']
            if "units" in paleots_list[match].keys():
                predictPositionsUnits = paleots_list[match]['units']
            else:
                predictPositionsUnits = []

    # Raise an error if the depth units don't correspond
    if predictPositionsUnits and positionsUnits:
        if predictPositionsUnits != positionsUnits:
            print("Depth units in the paleoData table and the chronData table don't match!")
            print("PaleoDepth are expressed in "+predictPositionsUnits+\
                  " while ChronDepth is expressed in "+positionsUnits)
            factor = float(input("Enter a correction value to bring Chron to Paleo scale"+\
                                 " or press Enter to exit."+\
                                 " Enter 1 if the units are in fact the same but"+\
                                 " written differently (e.g., m vs meter): "))
            if not factor:
                raise ValueError("No correction factor entered.")
            else:
                positions = positions*factor

    # Run Bchron
    print("Running Bchron. This could take a few minutes...")
    depth, chron, ageDist, run = agemodel.runBchron(ages, agesStd,positions,\
                                                    rejectAges = rejectAges,\
                                                    calCurves = calCurves,\
                                                    reservoirAgeCorr = reservoirAgeCorr,\
                                                    predictPositions = predictPositions,
                                                    positionsThickness= positionsThickness,\
                                                    outlierProbs=outlierProbs,\
                                                    iterations=iterations,\
                                                    burn=burn, thin=thin,\
                                                    extractDate=extractDate,\
                                                    maxExtrap=maxExtrap,\
                                                    thetaMhSd = thetaMhSd,\
                                                    muMhSd=muMhSd,psiMhSd = psiMhSd,\
                                                    ageScaleVal=ageScaleVal,\
                                                    positionScaleVal =positionScaleVal)

    ## Write into the LiPD file is asked

    print("Placing all the tables in the LiPD object...")
    if "model" in lipd["chronData"][objectName].keys():
        T = lipd["chronData"][objectName]["model"]
    else:
        T = lipd["chronData"][objectName].update({"model":{}})
    #Grab the part of the LiPD dictionary with the chronObject/model
    T = lipd["chronData"][objectName]["model"]

    ## methods
    inputs={"calCurves":calCurves,
            "iterations":iterations,
            "burn":burn,
            "thin":thin,
            "extractDate":extractDate,
            "maxExtrap": maxExtrap,
            "thetaMhSd": thetaMhSd,
            "muMhSd":muMhSd,
            "psiMhSd":psiMhSd,
            "ageScaleVal":ageScaleVal,
            "positionScaleVal":positionScaleVal}

    # Other None objects
    if type(reservoirAgeCorr) is np.ndarray:
        reservoirAgeCorr = reservoirAgeCorr.tolist()
        inputs.update({"reservoirAgeCorr":reservoirAgeCorr})
    else:
        inputs.update({"reservoirAgeCorr":"Not provided"})
    if type(rejectAges) is np.ndarray:
        rejectAges = rejectAges.tolist()
        inputs.update({"rejectAges":rejectAges})
    else:
        inputs.update({"rejectAges":"Not provided"})
    if type(positionsThickness) is np.ndarray:
        positionsThickness = positionsThickness.tolist()
        inputs.update({"positionsThickness":positionsThickness})
    else:
        inputs.update({"positionsThickness":"Not provided"})
    if type(outlierProbs) is np.ndarray:
        outlierProbs = outlierProbs.tolist()
        inputs.update({"outlierProbs":outlierProbs})
    else:
        inputs.update({"outlierProbs":"Not provided"})

    methods = {"algorithm":"Bchron", "inputs":inputs,"runEnv":"python"}

    #create the key for the new model
    key = str(objectName)+"model"+str(modelNum)
    # Add the method to object
    T.update({key:{}})
    T[key].update({"method":methods})

    ##EnsembleTable
    d = OrderedDict()
    T[key].update({"ensembleTable": d})
    key_ens = key+"ensemble0" # Key for the ensemble table
    T[key]["ensembleTable"].update({key_ens:{}})
    d = OrderedDict() #RESET VERY IMPORTANT
    T[key]["ensembleTable"][key_ens].update({"columns": d})

    #store age and depth info
    number_age = np.arange(2,np.shape(chron)[1]+2,1)
    number_age = number_age.tolist()
    chron_list = np.transpose(chron).tolist()
    age_dict = {"number": number_age,
                "units":agesUnit,
                "variableName":"age",
                "values":chron_list}
    depth_dict = {"number":1,
                  "units":predictPositionsUnits,
                  "variableName":"depth",
                  "values":depth}
    T[key]["ensembleTable"][key_ens]["columns"].update({"depth":depth_dict})
    T[key]["ensembleTable"][key_ens]["columns"].update({"age":age_dict})

    ## Summary Table
    # First calculate some summary stats
    quant = mquantiles(chron,[0.025,0.5,0.975],axis=1)
    # Save as list for JSON
    lower95 = quant[:,0].tolist()
    medianAge = quant[:,1].tolist()
    upper95 = quant[:,2].tolist()
    meanVal = np.mean(chron, axis=1)
    meanVal = meanVal.tolist()
    # Put everything where it belongs
    d = OrderedDict()
    T[key].update({"summaryTable": d})
    key_sum = key+"summary0"
    T[key]["summaryTable"].update({key_sum:{}})
    d = OrderedDict()
    T[key]["summaryTable"][key_sum].update({"columns": d})
    # Place each column as separate dictionary
    T[key]["summaryTable"][key_sum]["columns"].update({"depth":{"variableName":"depth",
                                                                "units":predictPositionsUnits,
                                                                "values":depth,
                                                                "number":1}})
    T[key]["summaryTable"][key_sum]["columns"].update({"meanAge":{"variableName":"meanAge",
                                                                "units":agesUnit,
                                                                "values":meanVal,
                                                                "number":2}})
    T[key]["summaryTable"][key_sum]["columns"].update({"medianAge":{"variableName":"medianAge",
                                                                "units":agesUnit,
                                                                "values":medianAge,
                                                                "number":3}})
    T[key]["summaryTable"][key_sum]["columns"].update({"95Lower":{"variableName":"95Lower",
                                                                "units":agesUnit,
                                                                "values":lower95,
                                                                "number":4}})
    T[key]["summaryTable"][key_sum]["columns"].update({"95Higher":{"variableName":"95Higher",
                                                                "units":agesUnit,
                                                                "values":upper95,
                                                                "number":5}})

    ## DistributionTables
    d = OrderedDict()
    T[key].update({"distributionTable": d})

    for i in np.arange(0,np.shape(ageDist)[1],1):
        #Get the output in list form
        i = int(i)
        key_dist = key+"distribution"+str(i)
        T[key]["distributionTable"].update({key_dist:{}})
        d = OrderedDict()
        T[key]["distributionTable"][key_dist].update({"age14C":list(run[6][i][0])[0],
                                                     "calibrationCurve":calCurves[i],
                                                     "columns":d,
                                                     "depth":list(run[6][i][2])[0],
                                                     "depthUnits":predictPositionsUnits,
                                                     "sd14C":list(run[6][i][1])[0]})
        age_dict = {"number":1,
                    "variableName":"age",
                    "units":agesUnit,
                    "values":list(run[6][i][4])}
        density_dict = {"number":2,
                    "variableName":"probabilityDensity",
                    "values":list(run[6][i][5])}

        T[key]["distributionTable"][key_dist]["columns"].update({"age":age_dict,
                                                                 "probabilityDensity":density_dict})
        ## Finally write it out
    if saveLipd is True:
        print("Writing LiPD file...")
        lpd.writeLipd(lipd,path=os.getcwd())

    #Plot if asked
    if plot_age is True:
        print("Plotting...")
        if flipCoor is True:
            if ylabel == None:
                if len(predictPositionsUnits)!=0:
                    ylabel = "Depth ("+str(predictPositionsUnits)+")"
                else:
                    ylabel = "Depth"
            if xlabel == None:
                if len(agesUnit)!=0:
                    xlabel = "Age ("+str(agesUnit)+")"
                else:
                    xlabel = "Age"
        else:
            if xlabel == None:
                if len(predictPositionsUnits)!=0:
                    xlabel = "Depth ("+str(predictPositionsUnits)+")"
                else:
                    xlabel = "Depth"
            if ylabel == None:
                if len(agesUnit)!=0:
                    ylabel = "Age ("+str(agesUnit)+")"
                else:
                    ylabel = "Age"
        fig = agemodel.plotBchron(depth,chron,positions,ageDist, flipCoor=flipCoor,\
                                 xlabel =xlabel, ylabel=ylabel,\
                                 xlim = xlim, ylim = ylim,\
                                 violinColor = violinColor,\
                                 medianLineColor = medianLineColor,\
                                 medianLineWidth = medianLineWidth,\
                                 CIFillColor = CIFillColor,\
                                 samplePaths = samplePaths,\
                                 samplePathNumber = samplePathNumber,
                                 alpha = alpha, figsize = figsize)
        if saveFig is True:
            lipdutils.saveFigure(lipd['dataSetName']+'_Bchron',format,dir)
        else:
            plt.show()
    else:
        fig = None

    return depth, chron, positions, ageDist, fig
