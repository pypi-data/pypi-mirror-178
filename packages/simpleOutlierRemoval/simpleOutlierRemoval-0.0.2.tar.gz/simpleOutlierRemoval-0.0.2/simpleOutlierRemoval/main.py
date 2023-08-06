import numpy as np

class removeOutlier:
    '''
    Use this package only if the assumption is that series is normally distributed.
    Also it will return only the elements which are not outliers
    '''
    def __init__(self, data_series):
        '''
        :param data_series: list or pandas series
        '''
        self.series_1 = np.array(data_series)

    def outlier_treatment_lower_upper(self):
        mean = np.mean(self.series_1)
        Q1 = np.percentile(self.series_1, 25, interpolation='midpoint')
        Q3 = np.percentile(self.series_1, 75, interpolation='midpoint')
        IQR = Q3 - Q1
        self.low_lim = mean - 3 * (IQR)
        self.up_lim = mean + 3 * (IQR)


    def get(self):
        self.outlier_treatment_lower_upper()
        b = np.where((self.series_1 < self.up_lim) & (self.series_1 > self.low_lim))
        return self.series_1[b]

