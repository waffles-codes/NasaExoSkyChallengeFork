import numpy as np
from astropy.coordinates import SkyCoord, AltAz, EarthLocation
from astroquery.gaia import Gaia
from astropy.time import Time
import astropy.units as u
from flask import Flask, jsonify, request
from flask_cors import CORS
app = Flask(__name__) #create a flask app
CORS(app)

def fetch_star_data(inp_ra, inp_dec):
    Gaia.MAIN_GAIA_TABLE = "gaiadr3.gaia_source"  # Reselect Data Release 3, default
    Gaia.ROW_LIMIT = 1000

    # Right ascension (RA) (basically east to west on sphere) and 
    # declination (Dec) (basically north south on a sphere)
    # are celestial coordinates that specify the position of an object in the sky.
    coord = SkyCoord(ra=inp_ra, dec=inp_dec, unit=(u.degree, u.degree))
    width = u.Quantity(1.6, u.deg)
    height = u.Quantity(0.9, u.deg)
    columns = ["ra", "dec", "distance_gspphot", "teff_gspphot"]
    # this returns a bunch of celestial coordinates in ascending order of angular distance
    r = Gaia.query_object_async(coordinate=coord, width=width, height=height, columns=columns)

    # this filters out all our rows without a distance
    filtered_r = r[r['distance_gspphot'].mask == False]

    non_empty_columns = [col for col in filtered_r.colnames if not all(filtered_r[col].mask)]
    r = filtered_r[non_empty_columns]

    # currently IT ONLY SHOWS THE PROJECTION FROM EARTH WHAT THE F*** WHO ADDED THIS (it was me, i added this)
    planet_location = EarthLocation(
        lon=0* u.deg,
        lat=0* u.deg,
        height=0 * u.m
    )
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
    color = r["teff_gspphot"]

    return np.column_stack((x, y, z, color))

def gnomonic_projection(x, y, z, ra0, dec0):
    # Calculate spherical coordinates from Cartesian coordinates
    r = np.sqrt(x**2 + y**2 + z**2)
    ra = np.arctan2(y, x)  # Right Ascension
    dec = np.arcsin(z / r)  # Declination

    # Convert center coordinates to radians
    ra0 = np.radians(ra0)
    dec0 = np.radians(dec0)

    # Gnomonic projection formulas
    cos_c = np.sin(dec0) * np.sin(dec) + np.cos(dec0) * np.cos(dec) * np.cos(ra - ra0)
    x_proj = np.cos(dec) * np.sin(ra - ra0) / cos_c
    y_proj = (np.cos(dec0) * np.sin(dec) - np.sin(dec0) * np.cos(dec) * np.cos(ra - ra0)) / cos_c

    return x_proj, y_proj

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

@app.route('/api/get_coords', methods=['GET'])
def get_coords():
    inp_ra = request.args.get('inp_ra', default=None, type=float)
    inp_dec = request.args.get('inp_dec', default=None, type=float)
    if inp_ra is None or inp_dec is None:
        return jsonify({"error": "Both inp_ra and inp_dec are required"}), 400

    data = fetch_star_data(inp_ra, inp_dec)
    data = np.array(data)
    x_coords = data[:, 0]
    y_coords = data[:, 1]
    z_coords = data[:, 2]
    color = data[:, 3]
    color = map_teff_to_star_color(color)
    x_proj, y_proj = gnomonic_projection(x_coords, y_coords, z_coords, inp_ra, inp_dec)
    coordsncolor = [{'x': float(x), 'y': float(y), 'color': str(color)} for x, y, color in zip(x_proj, y_proj, color)]
    return jsonify(coordsncolor)

if __name__ == '__main__':
    app.run(port=5000)
