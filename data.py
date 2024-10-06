import numpy as np
from astropy.coordinates import SkyCoord, AltAz, EarthLocation
from astroquery.gaia import Gaia
from astropy.time import Time
import astropy.units as u
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from scipy.stats import linregress
# from flask import Flask
# app = Flask(__name__) #create a flask app

Gaia.ROW_LIMIT = 200
Gaia.MAIN_GAIA_TABLE = "gaiadr3.gaia_source"  # Reselect Data Release 3, default

# Right ascension (RA) (basically east to west on sphere) and 
# declination (Dec) (basically north south on a sphere)
# are celestial coordinates that specify the position of an object in the sky.
coord = SkyCoord(ra=280, dec=-60, unit=(u.degree, u.degree))
width = u.Quantity(0.16, u.deg)
height = u.Quantity(0.09, u.deg)
# # this returns a bunch of celestial coordinates in ascending order of distance
# r = Gaia.query_object_async(coordinate=coord, width=width, height=height)

# r.pprint(max_width=130)

job = Gaia.launch_job_async("select top 200 ra, dec, distance_gspphot "
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
distance = r['distance_gspphot'] #add distances to scale with actual distance
# Convert spherical coordinates to Cartesian coordinates
x = distance * np.cos(altitude_rad) * np.cos(azimuth_rad)
y = distance * np.cos(altitude_rad) * np.sin(azimuth_rad)
z = distance * np.sin(altitude_rad)

# Perform linear regression to find the line of best fit in the xy plane
slope, intercept, _, _, _ = linregress(x, y)

# Calculate the direction vector of the line of best fit (Tangent vector)
tangent_vector = np.array([1, slope, 0])
tangent_vector /= np.linalg.norm(tangent_vector)

# Calculate the normal vector to the line of best fit
normal_vector = np.cross(tangent_vector, np.array([0, 0, 1]))
normal_vector /= np.linalg.norm(normal_vector)

# Calculate the binormal vector
binormal_vector = np.cross(tangent_vector, normal_vector)
binormal_vector /= np.linalg.norm(binormal_vector)

# Create the transformation matrix from XYZ to TNB
transformation_matrix = np.vstack((tangent_vector, normal_vector, binormal_vector)).T

# Transform the points into the TNB coordinate system
transformed_points = np.dot(transformation_matrix, np.vstack((x, y, z)))

# Extract the transformed coordinates
t_transformed = transformed_points[0, :]
n_transformed = transformed_points[1, :]
b_transformed = transformed_points[2, :]

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
scatter = ax.scatter(t_transformed, n_transformed, b_transformed, cmap='viridis', s=5)
cbar = plt.colorbar(scatter)
cbar.set_label('Altitude (Degrees)')
ax.set_xlabel('T Coordinate')
ax.set_ylabel('N Coordinate')
ax.set_zlabel('B Coordinate')
ax.set_title('3D Star Positions from Exoplanet')
ax.view_init(280, 60)
plt.show()

# @app.route('/api/get_coords', methods=['GET'])
# def get_coords():
#     return json_df

# if __name__ == '__main__':
#     app.run(port=5000)