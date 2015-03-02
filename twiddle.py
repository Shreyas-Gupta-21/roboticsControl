#!/usr/bin/env python


class Twiddle:
    """
    Twiddler class
    """

    def __init__(self, params=[0, 0, 0], deltas=[2, 1, 1], tolerance=10**-6):
        self.params = params
        self.deltas = deltas
        self.tolerance = tolerance
        self.error_min = float("inf")

    def tune(self, error_function):
        """
        Calculate the tuned parameters
        """
        # Initialize a buffered vector for the best parameters found for
        # cleaner keyboard interrupt handling
        self.best_params = [-1 for p in self.params]
        # Catch ctrl-Cs here since the interesting data (best params) are here
        try:
            # Coordinate descent -> tolerance will be on the param deltas
            #while self.error_min > self.tolerance:
            while sum(map(abs, self.deltas)) > self.tolerance:
                for i in range(len(self.params)):
                    self.params[i] += self.deltas[i]
                    error = error_function(self.params)
                    if error < self.error_min:
                        # New best result
                        self.error_min = error
                        self.best_params = self.params
                        self.deltas[i] *= 1.1
                    else:
                        # Was not better, try other way around
                        self.params[i] -= 2*self.deltas[i]
                        error = error_function(self.params)
                        if error < self.error_min:
                            # Was best when going the other way
                            self.error_min = error
                            self.best_params = self.params
                            self.deltas[i] *= 1.1
                        else:
                            # Didn't get better results using previous delta.
                            # Thus, make it smaller and try again
                            self.params[i] += self.deltas[i]
                            self.deltas[i] *= 0.9
        except KeyboardInterrupt:
            print "ctrl-C!"  # Do nothing and then pass the params
        return self.best_params
