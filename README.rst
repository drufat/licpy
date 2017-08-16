LicPy
==========================

There are a number of techniques to image vector fields. The most common one, known as hedgehog, is to draw an arrow at each point with a heading and a size matching the direction and magnitude of the vector field at that particular point (e.g. ``quiver`` in Matplotlib). Recently Cabral and Leedom proposed a new method to image vector fields called *line integral convolution* (LIC). LicPy is our implementation in Python of the LIC method.
