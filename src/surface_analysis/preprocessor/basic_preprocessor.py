import numpy as np
import typing

from surface_analysis.preprocessor.preprocessor import Preprocessor
from surface_analysis.fitter.fitter import NonLinearFitter
from surface_analysis.objective.linear_objective_function import LinearObjectiveFunction

# NOTE: this isn't a linear function but using the existing class structure as it does what we need
class XYPlaneOrientationObjectiveFunction(LinearObjectiveFunction):
    def __init__(self,
                x: np.ndarray,
                y: np.ndarray,
                z: np.ndarray
                ) -> None:
        self.x = x
        self.y = y
        self.z = z
        
    def rotate_points(
            self,
            theta_x: float,
            theta_y: float            
        ) -> typing.Tuple[np.ndarray, np.ndarray, np.ndarray]:
        points = np.hstack((self.x, self.y, self.z)).T
        # FIXME: put matrix creation in a separate module
        Mx = np.array(
                [[1,             0,              0],
                 [0, np.cos(theta_x), -np.sin(theta_x)],
                 [0, np.sin(theta_x),  np.cos(theta_x)]],
                dtype=np.float64
            )
        My = np.array(
                [[ np.cos(theta_y), 0, np.sin(theta_y)],
                 [               0, 1,               0],
                 [-np.sin(theta_y), 0, np.cos(theta_y)]],
                dtype=np.float64
            )
        M = Mx @ My
        rotated_points = M @ points

        #raise RuntimeError()
        return rotated_points[0,:].reshape(-1, 1),rotated_points[1,:].reshape(-1, 1),rotated_points[2,:].reshape(-1, 1)
        
    def evaluate(self, coeffs: np.ndarray, grad) -> float:
        theta_x = coeffs[0]
        theta_y = coeffs[1]
        x,y,z = self.rotate_points(theta_x,theta_y)
        f = abs(z).sum()
        return f


class BasicPreprocessor(Preprocessor):
    def preprocess_points(
        self,
        raw_x: np.ndarray,
        raw_y: np.ndarray,
        raw_z: np.ndarray,
    ) -> typing.Tuple[np.ndarray, np.ndarray, np.ndarray]:
        x,y,z = self.centre_points_centroid(raw_x, raw_y, raw_z)
        x,y,z = self.rotate_points_xy_plane(x, y, z)
        #x,y,z = self.centre_points_basin(x, y, z)
        return x,y,z

    def centre_points_centroid(
        self,
        raw_x: np.ndarray,
        raw_y: np.ndarray,
        raw_z: np.ndarray,
    ) -> typing.Tuple[np.ndarray, np.ndarray, np.ndarray]:
               
        x = raw_x - raw_x.mean()
        y = raw_y - raw_y.mean()
        z = raw_z - raw_z.mean()
        
        return x, y, z
       
    def rotate_points_xy_plane(
        self,
        raw_x: np.ndarray,
        raw_y: np.ndarray,
        raw_z: np.ndarray,
    ) -> typing.Tuple[np.ndarray, np.ndarray, np.ndarray]:
        func_class = XYPlaneOrientationObjectiveFunction(raw_x,raw_y,raw_z)
        fitter = NonLinearFitter(2,func_class,[-np.pi/2,-np.pi/2],[np.pi/2,np.pi/2],[0.,0.])
        params = fitter.fit()
        x,y,z = func_class.rotate_points(params[0][0],params[1][0])
        
        # detect if upside-down via z sign of point nearest to origin
        l = np.sqrt(x**2+y**2+z**2)
        i = l.argmin()
        isUpsideDown = (z[i]>0)
        
        # ensure +ve z is upwards     
        if isUpsideDown:
            x,y,z = func_class.rotate_points(params[0][0]+np.pi,params[1][0])
        
        return x,y,z
       
    def centre_points_basin(
        self,
        raw_x: np.ndarray,
        raw_y: np.ndarray,
        raw_z: np.ndarray,
    ) -> typing.Tuple[np.ndarray, np.ndarray, np.ndarray]:
        
        i = raw_z.argmin()
                       
        x = raw_x - raw_x[i]
        y = raw_y - raw_y[i]
        z = raw_z - raw_z[i]
        
        return x, y, z
