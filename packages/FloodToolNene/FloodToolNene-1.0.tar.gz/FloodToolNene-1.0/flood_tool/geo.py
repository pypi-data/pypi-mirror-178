from numpy import array, asarray, mod, sin, cos, tan, sqrt, arctan2, floor, rad2deg, deg2rad, stack, pi
from scipy.linalg import inv
import numpy as np

__all__ = ['get_easting_northing_from_gps_lat_long',
           'get_gps_lat_long_from_easting_northing']


class Ellipsoid(object):
    """ Data structure for a global ellipsoid. """

    def __init__(self, a, b, F_0):
        self.a = a
        self.b = b
        self.n = (a - b) / (a + b)
        self.e2 = (a ** 2 - b ** 2) / a ** 2
        self.F_0 = F_0


class Datum(Ellipsoid):
    """ Data structure for a global datum. """

    def __init__(self, a, b, F_0, phi_0, lam_0, E_0, N_0, H):
        super().__init__(a, b, F_0)
        self.phi_0 = phi_0
        self.lam_0 = lam_0
        self.E_0 = E_0
        self.N_0 = N_0
        self.H = H
        self.af0 = self.a * self.F_0
        self.bf0 = self.b * self.F_0


def dms2rad(deg, min=0, sec=0):
    """Convert degrees, minutes, seconds to radians.

    Parameters
    ----------
    deg: array_like
        Angle in degrees.
    min: array_like
        (optional) Angle component in minutes.
    sec: array_like
        (optional) Angle component in seconds.

    Returns
    -------
    numpy.ndarray
        Angle in radians.
    """
    deg = asarray(deg)
    return deg2rad(deg + min / 60. + sec / 3600.)


def rad2dms(rad, dms=False):
    """Convert radians to degrees, minutes, seconds.

    Parameters
    ----------

    rad: array_like
        Angle in radians.
    dms: bool
        Use degrees, minutes, seconds format. If False, use decimal degrees.

    Returns
    -------
    numpy.ndarray
        Angle in degrees, minutes, seconds or decimal degrees.
    """

    rad = asarray(rad)
    deg = rad2deg(rad)
    if dms:
        min = 60.0 * mod(deg, 1.0)
        sec = 60.0 * mod(min, 1.0)
        return stack((floor(deg), floor(min), sec.round(4)))
    else:
        return deg


osgb36 = Datum(a=6377563.396,
               b=6356256.910,
               F_0=0.9996012717,
               phi_0=deg2rad(49.0),
               lam_0=deg2rad(-2.),
               E_0=400000,
               N_0=-100000,
               H=24.7)

wgs84 = Ellipsoid(a=6378137,
                  b=6356752.3142,
                  F_0=0.9996)


def lat_long_to_xyz(phi, lam, rads=False, datum=osgb36):
    """Convert input latitude/longitude in a given datum into
    Cartesian (x, y, z) coordinates.

    Parameters
    ----------

    phi: array_like
        Latitude in degrees (if radians=False) or radians (if radians=True).
    lam: array_like
        Longitude in degrees (if radians=False) or radians (if radians=True).
    rads: bool (optional)
        If True, input latitudes and longitudes are in radians.
    datum: Datum (optional)
        Datum to use for conversion.
    """
    if not rads:
        phi = deg2rad(phi)
        lam = deg2rad(lam)

    nu = datum.a * datum.F_0 / sqrt(1 - datum.e2 * sin(phi) ** 2)

    return array(((nu + datum.H) * cos(phi) * cos(lam),
                  (nu + datum.H) * cos(phi) * sin(lam),
                  ((1 - datum.e2) * nu + datum.H) * sin(phi)))


def xyz_to_lat_long(x, y, z, rads=False, datum=osgb36):
    p = sqrt(x ** 2 + y ** 2)

    lam = arctan2(y, x)
    phi = arctan2(z, p * (1 - datum.e2))

    for _ in range(10):
        nu = datum.a * datum.F_0 / sqrt(1 - datum.e2 * sin(phi) ** 2)
        dnu = -datum.a * datum.F_0 * cos(phi) * sin(phi) / (1 - datum.e2 * sin(phi) ** 2) ** 1.5

        f0 = (z + datum.e2 * nu * sin(phi)) / p - tan(phi)
        f1 = datum.e2 * (nu ** cos(phi) + dnu * sin(phi)) / p - 1.0 / cos(phi) ** 2
        phi -= f0 / f1

    if not rads:
        phi = rad2dms(phi)
        lam = rad2dms(lam)

    return phi, lam


def get_easting_northing_from_gps_lat_long(phis, lams, rads=False):
    """ Get OSGB36 easting/northing from GPS latitude and longitude pairs.

    Parameters
    ----------
    phis: float/arraylike
        GPS (i.e. WGS84 datum) latitude value(s)
    lams: float/arrayling
        GPS (i.e. WGS84 datum) longitude value(s).
    rads: bool (optional)
        If true, specifies input is is radians.
    Returns
    -------
    numpy.ndarray
        Easting values (in m)
    numpy.ndarray
        Northing values (in m)
        Examples
    --------
    >>> get_easting_northing_from_gps_lat_long([55.5], [-1.54])
    (array([429157.0]), array([623009]))
    References
    ----------
    Based on the formulas in "A guide to coordinate systems in Great Britain".
    See also https://webapps.bgs.ac.uk/data/webservices/convertForm.cfm
    """

    if not isinstance(phis, list) and not isinstance(phis,np.ndarray):
        phis = [phis]
        lams = [lams]
    assert len(phis) == len(lams)

    res_east = []
    res_north = []
    for i, phi in enumerate(phis):
        lam = lams[i]
        if not rads:
            phi = deg2rad(phi)
            lam = deg2rad(lams[i])
        M = bigM(osgb36.bf0, osgb36.n, osgb36.phi_0, phi)
        nu = osgb36.af0 / (sqrt(1 - (osgb36.e2 * ((sin(phi)) ** 2))))
        rho = (nu * (1 - osgb36.e2)) / (1 - (osgb36.e2 * (sin(phi)) ** 2))
        eta2 = (nu / rho) - 1

        I = M + osgb36.N_0
        II = (nu / 2) * sin(phi) * cos(phi)
        III = (nu / 24) * sin(phi) * cos(phi) ** 3 * (5 - tan(phi) ** 2 + 9 * eta2)
        IIIA = (nu / 720) * sin(phi) * cos(phi) ** 5 * (61 - 58 * tan(phi) ** 2 + tan(phi) ** 4)
        IV = nu * cos(phi)
        V = (nu / 6) * cos(phi) ** 3 * (nu / rho - tan(phi) ** 2)
        VI = (nu / 120) * cos(phi) ** 5 * (
                5 - 18 * tan(phi) ** 2 + tan(phi) ** 4 + 14 * eta2 - 58 * tan(phi) ** 2 * eta2)
        diff = lam - osgb36.lam_0
        N = I + II * diff ** 2 + III * diff ** 4 + IIIA * diff ** 6
        E = osgb36.E_0 + IV * diff + V * diff ** 3 + VI * diff ** 5
        res_east.append(round(E,0))
        res_north.append(round(N,0))

    return res_east, res_north


def bigM(bf0, n, PHI0, PHI):
    """
    Compute meridional arc.
    Input:
     - ellipsoid semi major axis multiplied by central meridian scale factor (bf0) in meters;
     - n (computed from a, b and f0);
     - lat of false origin (PHI0) and initial or final latitude of point (PHI) IN RADIANS.
    """
    M = bf0 * (((1 + n + ((5 / 4) * (n ** 2)) + ((5 / 4) * (n ** 3))) * (PHI - PHI0))
               - (((3 * n) + (3 * (n ** 2)) + ((21 / 8) * (n ** 3))) * (sin(PHI - PHI0)) * (
                cos(PHI + PHI0)))
               + ((((15 / 8) * (n ** 2)) + ((15 / 8) * (n ** 3))) * (sin(2 * (PHI - PHI0))) * (
                cos(2 * (PHI + PHI0))))
               - (((35 / 24) * (n ** 3)) * (sin(3 * (PHI - PHI0))) * (cos(3 * (PHI + PHI0)))))
    return M


def getNewPhi(North, datum):
    PHI1 = ((North - datum.N_0) / datum.af0) + datum.phi_0
    M = bigM(datum.bf0, datum.n, datum.phi_0, PHI1)

    # Calculate new PHI value (PHI2)
    PHI2 = ((North - datum.N_0 - M) / datum.af0) + PHI1

    # Iterate to get final value for InitialLat
    while abs(North - datum.N_0 - M) > 0.00001:
        PHI2 = ((North - datum.N_0 - M) / datum.af0) + PHI1
        M = bigM(datum.bf0, datum.n, datum.phi_0, PHI2)
        PHI1 = PHI2

    return PHI2


def get_gps_lat_long_from_easting_northing(easts: float, norths: float, rads=False, dms=False):
    """ Get OSGB36 easting/northing from GPS latitude and
    longitude pairs.
    Parameters
    ----------
    east: float/arraylike
        OSGB36 easting value(s) (in m).
    north: float/arrayling
        OSGB36 easting value(s) (in m).
    rads: bool (optional)
        If true, specifies ouput is radians.
    dms: bool (optional)
        If true, output is in degrees/minutes/seconds. Incompatible
        with rads option.
    Returns
    -------
    numpy.ndarray
        GPS (i.e. WGS84 datum) latitude value(s).
    numpy.ndarray
        GPS (i.e. WGS84 datum) longitude value(s).
    Examples
    --------
    >>> get_gps_lat_long_from_easting_northing([429157], [623009])
    (array([55.5]), array([-1.540008]))
    References
    ----------
    Based on the formulas in "A guide to coordinate systems in Great Britain".
    See also https://webapps.bgs.ac.uk/data/webservices/convertForm.cfm
    """
    if not isinstance(easts, list) and not isinstance(easts,np.ndarray):
        easts = [easts]
        norths = [norths]
    assert len(easts) == len(norths)
    res_lat = []
    res_lon = []
    for i, east in enumerate(easts):
        north = norths[i]
        Et = east - osgb36.E_0
        PHId = getNewPhi(north, datum=osgb36)
        nu = osgb36.af0 / (sqrt(1 - (osgb36.e2 * ((sin(PHId)) ** 2))))
        rho = (nu * (1 - osgb36.e2)) / (1 - (osgb36.e2 * (sin(PHId)) ** 2))
        eta2 = (nu / rho) - 1

        # Compute Latitude
        VII = (tan(PHId)) / (2 * rho * nu)
        VIII = ((tan(PHId)) / (24 * rho * (nu ** 3))) * (
                5 + (3 * ((tan(PHId)) ** 2)) + eta2 - (9 * eta2 * ((tan(PHId)) ** 2)))
        IX = ((tan(PHId)) / (720 * rho * (nu ** 5))) * (
                61 + (90 * ((tan(PHId)) ** 2)) + (45 * ((tan(PHId)) ** 4)))

        X = ((cos(PHId)) ** -1) / nu
        XI = (((cos(PHId)) ** -1) / (6 * (nu ** 3))) * ((nu / rho) + (2 * ((tan(PHId)) ** 2)))
        XII = (((cos(PHId)) ** -1) / (120 * (nu ** 5))) * (
                5 + (28 * ((tan(PHId)) ** 2)) + (24 * ((tan(PHId)) ** 4)))
        XIIA = (((cos(PHId)) ** -1) / (5040 * (nu ** 7))) * (
                61 + (662 * ((tan(PHId)) ** 2)) + (1320 * ((tan(PHId)) ** 4)) + (
                720 * ((tan(PHId)) ** 6)))
        E_N_Lat = PHId - ((Et ** 2) * VII) + ((Et ** 4) * VIII) - ((Et ** 6) * IX)
        E_N_Long = osgb36.lam_0 + (Et * X) - ((Et ** 3) * XI) + ((Et ** 5) * XII) - ((Et ** 7) * XIIA)
        if not rads:
            E_N_Lat = rad2dms(E_N_Lat, dms=dms)
            E_N_Long = rad2dms(E_N_Long, dms=dms)
        res_lat.append(E_N_Lat)
        res_lon.append(E_N_Long)
    return res_lat, res_lon


class HelmertTransform(object):
    """Callable class to perform a Helmert transform."""

    def __init__(self, s, rx, ry, rz, T):
        self.T = T.reshape((3, 1))

        self.M = array([[1 + s, -rz, ry],
                        [rz, 1 + s, -rx],
                        [-ry, rx, 1 + s]])

    def __call__(self, X):
        X = X.reshape((3, -1))
        return self.T + self.M @ X


class HelmertInverseTransform(object):
    """Callable class to perform the inverse of a Helmert transform."""

    def __init__(self, s, rx, ry, rz, T):
        self.T = T.reshape((3, 1))

        self.M = inv(array([[1 + s, -rz, ry],
                            [rz, 1 + s, -rx],
                            [-ry, rx, 1 + s]]))

    def __call__(self, X):
        X = X.reshape((3, -1))
        return self.M @ (X - self.T)


OSGB36transform = HelmertTransform(20.4894e-6,
                                   -dms2rad(0, 0, 0.1502),
                                   -dms2rad(0, 0, 0.2470),
                                   -dms2rad(0, 0, 0.8421),
                                   array([-446.448, 125.157, -542.060]))

WGS84transform = HelmertInverseTransform(20.4894e-6,
                                         -dms2rad(0, 0, 0.1502),
                                         -dms2rad(0, 0, 0.2470),
                                         -dms2rad(0, 0, 0.8421),
                                         array([-446.448, 125.157, -542.060]))


def WGS84toOSGB36(phi, lam, rads=False):
    """Convert WGS84 latitude/longitude to OSGB36 latitude/longitude.

    Parameters
    ----------
    phi : array_like or float
        Latitude in degrees or radians on WGS84 datum.
    lam : array_like or float
        Longitude in degrees or radians on WGS84 datum.
    rads : bool, optional
        If True, phi and lam are in radians. If False, phi and lam are in degrees.

    Returns
    -------
    tuple of numpy.ndarrays
        Latitude and longitude on OSGB36 datum in degrees or radians.
    """
    xyz = OSGB36transform(lat_long_to_xyz(asarray(phi), asarray(lam),
                                          rads=rads, datum=wgs84))
    return xyz_to_lat_long(*xyz, rads=rads, datum=osgb36)


def OSGB36toWGS84(phi, lam, rads=False):
    """Convert OSGB36 latitude/longitude to WGS84 latitude/longitude.

    Parameters
    ----------
    phi : array_like or float
        Latitude in degrees or radians on OSGB36 datum.
    lam : array_like or float
        Longitude in degrees or radians on OSGB36 datum.
    rads : bool, optional
        If True, phi and lam are in radians. If False, phi and lam are in degrees.

    Returns
    -------
    tuple of numpy.ndarrays
        Latitude and longitude on WGS84 datum in degrees or radians.
    """
    xyz = WGS84transform(lat_long_to_xyz(asarray(phi), asarray(lam),
                                         rads=rads, datum=osgb36))
    return xyz_to_lat_long(*xyz, rads=rads, datum=wgs84)


if __name__ == "__main__":
    print(get_easting_northing_from_gps_lat_long([55.5], [-1.54]))
