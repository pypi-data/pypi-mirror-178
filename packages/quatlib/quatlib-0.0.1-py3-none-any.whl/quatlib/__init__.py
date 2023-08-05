from numpy import *
from scipy.spatial.transform import Rotation

"""
print('================================================================================')
print('Datatype\n')
print("Angles:\t\tRadian(float)\nQuaternion:\tarray[qw,qx,qy,qz]\nAxis:\t\tarray[x,y,z]\n")
print('\t\t\t\t\t\tR11\tR12\tR13\nRotation Matrix:In (3x3) matrix/array form like\tR21\tR22\tR23\t\n\t\t\t\t\t\tR31\tR32\tR33')
print('================================================================================')
"""

"""
###########################################################################
Datatype

Angles:		Radian(float)
Quaternion:	array[qw,qx,qy,qz]
Axis:		array[x,y,z]

						R11	R12	R13
Rotation Matrix:In (3x3) matrix/array form like	R21	R22	R23	
						R31	R32	R33
###########################################################################
"""

def axisAngle2quatern(axis, angle):
    '''
    axis as array([x,y,z]), angle in radian 
    '''
    axis = axis/linalg.norm(axis)
    q0 = float(cos(divide(angle,2)))
    q1 = -float(axis[0]*sin(angle/2.0))
    q2 = -float(axis[1]*sin(angle/2.0))
    q3 = -float(axis.item[2]*sin(angle/2.0))
    q = array([q0, q1, q2, q3])
    return q

def axisAngle2rotMat(axis, angle):
    '''
    axis as array([x,y,z]), angle in radian 
    '''
    axis = axis/linalg.norm(axis)
    kx = axis[0]
    ky = axis[1]
    kz = axis[2]
    cT = cos(angle)
    sT = sin(angle)
    vT = 1 - cos(angle)

    R11 = kx*kx*vT + cT
    R12 = kx*ky*vT - kz*sT
    R13 = kx*kz*vT + ky*sT

    R21 = kx*ky*vT + kz*sT
    R22 = ky*ky*vT + cT
    R23 = ky*kz*vT - kx*sT

    R31 = kx*kz*vT - ky*sT
    R32 = ky*kz*vT + kx*sT
    R33 = kz*kz*vT + cT

    R = array([[R11,R12,R13],[R21,R22,R23],[R31,R32,R33]])
    return R

def euler2rotMat(phi, theta, psi):
    '''
    phi, theta, psi in radian
    '''
    R11 = cos(psi)*cos(theta)
    R12 = -sin(psi)*cos(phi) + cos(psi)*sin(theta)*sin(phi)
    R13 = sin(psi)*sin(phi) + cos(psi)*sin(theta)*cos(phi)

    R21 = sin(psi)*cos(theta)
    R22 = cos(psi)*cos(phi) + sin(psi)*sin(theta)*sin(phi)
    R23 = -cos(psi)*sin(phi) + sin(psi)*sin(theta)*cos(phi)

    R31 = -sin(theta)
    R32 = cos(theta)*sin(phi)
    R33 = cos(theta)*cos(phi)

    R = array([[R11,R12,R13],[R21,R22,R23],[R31,R32,R33]])
    return R

def quatern2euler(q):
    '''
    Quaternion, q = array[qw,qx,qy,qz]
    '''
    q=q/linalg.norm(q)
    q0 = q[0]
    q1 = q[1]
    q2 = q[2]
    q3 = q[3]
    
    R11 = 2*(q0**2)-1+2*(q1**2)
    R21 = 2*(q1*q2-q0*q3)
    R31 = 2*(q1*q3+q0*q2)
    R32 = 2*(q2*q3-q0*q1)
    R33 = 2*(q0**2)-1+2*(q3**2)

    phi = arctan2(R32, R33 )
    theta = -arctan(R31 / sqrt(1-(R31**2)) )
    psi = arctan2(R21, R11 )

    euler = array([phi, theta, psi])
    return euler

def quatern2rotMat(q):
    '''
    Quaternion, q = array[qw,qx,qy,qz]
    '''
    q=q/linalg.norm(q)
    q0 = q[0]
    q1 = q[1]
    q2 = q[2]
    q3 = q[3]
    
    R11 = 2*(q0**2)-1+2*(q1**2)
    R12 = 2*(q1*q2+q0*q3)
    R13 = 2*(q1*q3-q0*q2)
    R21 = 2*(q1*q2-q0*q3)
    R22 = 2*(q0**2)-1+2*(q2**2)
    R23 = 2*(q2*q3+q0*q1)
    R31 = 2*(q1*q3+q0*q2)
    R32 = 2*(q2*q3-q0*q1)
    R33 = 2*(q0**2)-1+2*(q3**2)

    R = array([[R11,R12,R13],[R21,R22,R23],[R31,R32,R33]])
    return R

def quaternConj(q):
    '''
    Quaternion, q = array[qw,qx,qy,qz]
    '''
    q=q/linalg.norm(q)
    qConj= array([q[0],-q[1],-q[2],-q[3]])
    return qConj

def quaternProd(a, b):
    '''
    a & b are quaternions array of form q = array[qw,qx,qy,qz]
    '''
    a=a/linalg.norm(a)
    b=b/linalg.norm(b)
    ab1 = a[0]*b[0]-a[1]*b[1]-a[2]*b[2]-a[3]*b[3]
    ab2 = a[0]*b[1]+a[1]*b[0]+a[2]*b[3]-a[3]*b[2]
    ab3 = a[0]*b[2]-a[1]*b[3]+a[2]*b[0]+a[3]*b[1]
    ab4 = a[0]*b[3]+a[1]*b[2]-a[2]*b[1]+a[3]*b[0]
    ab = array([ab1,ab2,ab3,ab4])
    return ab

def rotMat2euler(R):
    '''
    R is Rotation Matrix in (3x3) matrix/array form
    '''
    phi = arctan2(R.item(2,1), R.item(2,2) )
    theta = -arctan(R.item(2,0) / sqrt(1-R.item(2,0)**2) )
    psi = arctan2(R.item(1,0), R.item(0,0) )

    euler = array([phi, theta, psi])
    return euler
def rotMat2quatern(R):
    '''
    R is Rotation Matrix in (3x3) matrix/array form
    '''
    q = array([Rotation.from_matrix(R).as_quat()[3], Rotation.from_matrix(R).as_quat()[0], Rotation.from_matrix(R).as_quat()[1], Rotation.from_matrix(R).as_quat()[2]])
    return q
