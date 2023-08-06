0.3 (unreleased)
----------------

- No changes yet

0.2 (2016-09-20)
------------------

- Fixed bug arising from changes to distutils.ConfigParser [#177, #187, #191]

- Removed the sites module from astroplan, since it was ported to astropy [#168]

- Removed dependence on PyEphem, now using jplephem for the solar system
  ephemeris [#167]

- New API for scheduling observations (still in development)

- New ``plot_finder_image`` function makes quick finder charts [#115]

- Updates to astropy helpers and the package template [#177, #180]
