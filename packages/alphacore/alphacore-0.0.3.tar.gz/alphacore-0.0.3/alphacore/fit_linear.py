import numpy as np
from scipy.optimize import curve_fit
from alphacore.utils import linear_models, objectConverters, removeNegativesInX


class fit_linear_model:
    def __init__(self, model, xdata, ydata):
        xmin = None
        guess = None
        if model.upper() in [
            "LINEAR",
            "POLY_1",
            "POLY1",
            "POLYNOMIAL_1",
            "POLYNOMIAL1",
        ]:
            param_names = ["a", "b"]
            func = linear_models.linear
        elif model.upper() in [
            "QUADRATIC",
            "POLY_2",
            "POLY2",
            "POLYNOMIAL_2",
            "POLYNOMIAL2",
        ]:
            param_names = ["a", "b", "c"]
            func = linear_models.poly_2
        elif model.upper() in [
            "CUBIC",
            "POLY_3",
            "POLY3",
            "POLYNOMIAL_3",
            "POLYNOMIAL3",
        ]:
            param_names = ["a", "b", "c", "d"]
            func = linear_models.poly_3
        elif model.upper() in [
            "QUARTIC",
            "POLY_4",
            "POLY4",
            "POLYNOMIAL_4",
            "POLYNOMIAL4",
        ]:
            param_names = ["a", "b", "c", "d", "e"]
            func = linear_models.poly_4
        elif model.upper() in [
            "QUINTIC",
            "POLY_5",
            "POLY5",
            "POLYNOMIAL_5",
            "POLYNOMIAL5",
        ]:
            param_names = ["a", "b", "c", "d", "e", "f"]
            func = linear_models.poly_5
        elif model.upper() in [
            "SEXTIC",
            "POLY_6",
            "POLY6",
            "POLYNOMIAL_6",
            "POLYNOMIAL6",
        ]:
            param_names = ["a", "b", "c", "d", "e", "f", "g"]
            func = linear_models.poly_6
        elif model.upper() in ["LOG", "LOGARITHMIC"]:
            param_names = ["a", "b", "c"]
            func = linear_models.logarithmic
            xdata, ydata = removeNegativesInX(xdata, ydata)
            xmin = 0
        elif model.upper() in ["EXP", "EXPON", "EXPONENTIAL"]:
            param_names = ["a", "b", "c"]
            func = linear_models.exponential
            guess = [1, -0.001, 0]
            xmin = 0
        elif model.upper() in ["POWER", "PWR", "POW"]:
            param_names = ["a", "b"]
            func = linear_models.power
            xdata, ydata = removeNegativesInX(xdata, ydata)
            xmin = 0
        else:
            raise ValueError("model not recognised")

        # print('xdata:',xdata)
        # print('ydata:',ydata)

        fit = curve_fit(f=func, xdata=xdata, ydata=ydata, method="trf", p0=guess)
        params = fit[0].tolist()

        objectConverters.list2object(
            object_to_use=self, keys=param_names, values=params
        )

        # generate plotting limits
        xrange = max(xdata) - min(xdata)
        yrange = max(ydata) - min(ydata)
        if xmin is None:
            self.xmin = float(min(xdata) - xrange * 0.2)
        else:
            self.xmin = float(xmin)
        self.xmax = float(max(xdata) + xrange * 0.2)
        self.ymin = float(min(ydata) - yrange * 0.2)
        self.ymax = float(max(ydata) + yrange * 0.2)

        # generate fitted line from model parameters
        xline = np.linspace(min(xdata) - xrange, max(xdata) + xrange, 200)
        if xmin == 0:
            xline = removeNegativesInX(xline)
        yline = func(*[xline, *params])
        self.xline = xline.tolist()
        self.yline = yline.tolist()
