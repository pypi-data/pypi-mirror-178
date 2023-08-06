# Remove the outliers from Series

####### Assuming the series is normally distributed

### Instructions

1. Install:

        pip install simpleOutlierRemoval


2. Calculate the co-effecient of variance

        from simpleOutlierRemoval import main
        # get the output of the series without any outliers
        cov = main.removeOutlier(series).get()
