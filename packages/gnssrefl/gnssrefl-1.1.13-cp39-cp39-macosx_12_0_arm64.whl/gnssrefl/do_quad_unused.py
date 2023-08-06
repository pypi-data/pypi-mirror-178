def do_quad(vquad, year, year_end):
    """
    is this used?

    Parameters
    ----------
    vquad : ?? 
    year : int
        first year

    year_end : int
        final year

    Returns 
    -------
    vout : 3 vector (year, doy, phase)

    requires at least 3 values for an average
    """
    vout = np.empty(shape=[0, 3])
    y1 = vquad[:, 0]
    d1 = vquad[:, 1]
    phq = vquad[:, 2]
    for year in range(year, year_end+1):
        for doy in range(1, 367):
            ph1 = phq[(y1 == year) & (d1 == doy)]
            if len(ph1) > 3:
                meanphase = np.mean(ph1)
                newl = np.hstack((year, doy, meanphase))
                # in which kristine learns tha vertically stacking
                # the transpose is the same as horizontally stacking ;-)
                #newl = np.vstack((year,doy,meanphase)).T
                vout = np.vstack((vout, newl))
    return vout
