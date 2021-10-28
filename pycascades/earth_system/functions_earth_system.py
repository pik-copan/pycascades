import numpy as np

"""
Here all global functions are stored - the functions are up to "choice": Here, linear functions are used
"""


class global_functions():
    """
    Linear feedback function to compute feedbacks. Maximal feedback is obtained from 2.0°C onwards.
    feedbacks for Arctic summer sea ice, mountain glaciers, GIS and WAIS are proven to be constant also for higher temperatures
    feedbacks for Amazon and feedbacks_steffen are computed for a temperature increase of 2.0°C until 2100, see paper
    """
    def feedback_function(GMT, fbmax):
        # fbmax = maximal feedback
        # only returns a value in case GMT is higher than lower boundary of the respective tipping element, otherwise return 0.0 (lower cap), N.B.: No upper cap
        if GMT <= 2.0:
            y = (fbmax / 2.0) * GMT
            return y
        elif GMT > 2.0:
            return fbmax
        else:
            raise Exception("GMT negativ: Feedbacks do not work for temperatures smaller 0!")

    # feedbacks of state dependent variables, linear increase of feedbacks between state -1 and +1 for GIS, WAIS, THC, NINO and AMAZ
    def state_feedback(state, fbmax):
        if state >= -1 and state <= 1:
            y = fbmax / 2 * (state + 1)
        elif state < -1:
            y = 0.
        elif state > +1:
            y = fbmax
        return y

    # c = c(GMT) where tipping occurs at sqrt(4/27) ~ 0.38
    # Linear function through two points maps GMT --> c, where x-values represent GMT and y-values represent CUSP-c values
    def CUSPc(x1, x2, x):
        # only returns a value in case GMT is higher than lower boundary of the respective tipping element, otherwise return 0.0 (lower cap), N.B.: No upper cap
        if x >= x1:
            y1 = 0.0
            y2 = np.sqrt(4 / 27)
            y = (y2 - y1) / (x2 - x1) * (x - x1) + y1
            return y
        else:
            return 0.0