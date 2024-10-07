def fetch_star_data(inp_ra, inp_dec):
    # Right ascension (RA) (basically east to west on sphere) and 
    # declination (Dec) (basically north south on a sphere)
    # are celestial coordinates that specify the position of an object in the sky.
    coord = SkyCoord(ra=inp_ra, dec=inp_dec, unit=(u.degree, u.degree))
    # width = u.Quantity(16, u.deg)
    # height = u.Quantity(9, u.deg)
    # # this returns a bunch of celestial coordinates in ascending order of distance
    # r = Gaia.query_object_async(coordinate=coord, width=width, height=height)

    # r.pprint(max_width=130)

    #GET THIS TO ACTUALLY GIVE US GOOD DATA PLEASE WEHHHHHHHHHHH
    # job = Gaia.cone_search_async(coord, radius=0.5*u.deg)
    job = Gaia.launch_job_async("select top 2000 ra, dec, distance_gspphot, teff_gspphot "
                                "from gaiadr3.gaia_source_lite order by source_id",
                                dump_to_file=False, output_format='csv')
    r = job.get_data()
    # r.pprint()

    # Function to map teff_gspphot to star colors
    def map_teff_to_star_color(teff_gspphot):
        """
        Map stellar temperature (Teff) to a color based on astronomical star types.

        Parameters:
        teff_gspphot (array-like): Array of effective temperatures (Teff).

        Returns:
        star_colors (list): List of colors corresponding to the temperatures.
        """
        star_colors = []
        for teff in teff_gspphot:
            if teff > 10000:  # Blue
                star_colors.append('blue')
            elif 7500 < teff <= 10000:  # White
                star_colors.append('white')
            elif 5000 < teff <= 7500:  # Yellow
                star_colors.append('yellow')
            elif 3500 < teff <= 5000:  # Orange
                star_colors.append('orange')
            else:  # Red stars (coolest)
                star_colors.append('red')
        return star_colors

    # Map teff_gspphot values to star colors
    r['star_colors'] = map_teff_to_star_color(r['teff_gspphot'])



    # this removes all rows that do not have a distance_gspphot entry
    i = 0
    remove_list = []
    for row in r:
        if not row[2]:
            remove_list.append(i)
        i += 1

    r.remove_rows(remove_list)
    # r.pprint()


    planet_location = EarthLocation(lat=45*u.deg, lon=120*u.deg, height=0*u.m)
    azimuths = []
    altitudes = []

    for star in r:
        star_location = SkyCoord(ra=star['ra'], dec=star['dec'], unit=(u.degree, u.degree))
        star_altaz = star_location.transform_to(AltAz(obstime=Time.now(), location=planet_location))
        azimuths.append(star_altaz.az)
        altitudes.append(star_altaz.alt)
    r['azimuth'] = azimuths
    r['altitude'] = altitudes

    azimuth_rad = np.radians(r['azimuth'])
    altitude_rad = np.radians(r['altitude'])
    distance = r['distance_gspphot'] #add distances to scale with actual distance
    # Convert spherical coordinates to Cartesian coordinates
    x = distance * np.cos(altitude_rad) * np.cos(azimuth_rad)
    y = distance * np.cos(altitude_rad) * np.sin(azimuth_rad)
    z = distance * np.sin(altitude_rad)

    starColor = np.array(r['star_colors'])

    return np.column_stack((x, y, z), starColor)
