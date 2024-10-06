import numpy as np
from astropy.coordinates import SkyCoord, AltAz, EarthLocation
from astroquery.gaia import Gaia
from astropy.time import Time
import astropy.units as u
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from flask import Flask, jsonify, request
from flask_cors import CORS
app = Flask(__name__) #create a flask app
CORS(app)


Gaia.ROW_LIMIT = 1000
Gaia.MAIN_GAIA_TABLE = "gaiadr3.gaia_source"  # Reselect Data Release 3, default

def fetch_star_data(inp_ra, inp_dec):
    # Right ascension (RA) (basically east to west on sphere) and 
    # declination (Dec) (basically north south on a sphere)
    # are celestial coordinates that specify the position of an object in the sky.
    coord = SkyCoord(ra=inp_ra, dec=inp_dec, unit=(u.degree, u.degree))
    width = u.Quantity(16, u.deg)
    height = u.Quantity(9, u.deg)
    # # this returns a bunch of celestial coordinates in ascending order of distance
    # r = Gaia.query_object_async(coordinate=coord, width=width, height=height)

    # r.pprint(max_width=130)

    job = Gaia.launch_job_async("select top 1000 ra, dec, distance_gspphot "
                                "from gaiadr3.gaia_source_lite order by source_id",
                                dump_to_file=False, output_format='csv')
    r = job.get_data()

    # this removes all rows that do not have a distance_gspphot entry
    i = 0
    remove_list = []
    for row in r:
        if not row[2]:
            remove_list.append(i)
        i += 1

    r.remove_rows(remove_list)
    r.pprint()


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
    dist = r['distance_gspphot'] #add distances to scale with actual distance
    x = dist * np.cos(altitude_rad) * np.sin(azimuth_rad)
    y = dist * np.cos(altitude_rad) * np.cos(azimuth_rad)
    z = dist * np.sin(altitude_rad)

    return np.column_stack((x, y, z))

def project_to_2d(xyz):
    # Simple perspective projection
    z_values = xyz[:, 2] + 1e-10
    x_2d = np.divide(xyz[:, 0], z_values, where=z_values!=0)
    y_2d = np.divide(xyz[:, 1], z_values, where=z_values!=0)
    return np.column_stack((x_2d, y_2d))

@app.route('/api/get_coords', methods=['GET'])
def get_coords():
    inp_ra = request.args.get('inp_ra', default=None, type=float)
    inp_dec = request.args.get('inp_dec', default=None, type=float)
    if inp_ra is None or inp_dec is None:
        return jsonify({"error": "Both inp_ra and inp_dec are required"}), 400

    xyz = fetch_star_data(inp_ra, inp_dec)
    xyz = np.array(xyz)
    projection_2d = project_to_2d(xyz)
    coords = [{'x': float(coord[0]), 'y': float(coord[1])} for coord in projection_2d]
    return jsonify(coords)

if __name__ == '__main__':
    app.run(port=5000)