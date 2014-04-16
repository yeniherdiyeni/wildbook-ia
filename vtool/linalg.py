from __future__ import absolute_import, division, print_function
# Science
import cv2
import numpy as np
import numpy.linalg as npl
from numpy import (array, sin, cos)
import utool
(print, print_, printDBG, rrr, profile) = utool.inject(
    __name__, '[linalg]', DEBUG=False)

np.tau = 2 * np.pi  # tauday.com

TRANSFORM_DTYPE = np.float64


# Function which multiplies many matrices at once
from numpy.core.umath_tests import matrix_multiply  # NOQA


def svd(M):
    # V is actually Vt
    flags = cv2.SVD_FULL_UV
    S, U, Vt = cv2.SVDecomp(M, flags=flags)
    s = S.flatten()
    return U, s, Vt


def OLD_pdf_norm2d(x_, y_):
    # DEPRICATED
    import math
    x = np.array([x_, y_])
    sigma = np.eye(2)
    mu = np.array([0, 0])
    size = len(x)
    if size == len(mu) and (size, size) == sigma.shape:
        det = np.linalg.det(sigma)
        if det == 0:
            raise NameError('The covariance matrix cant be singular')
    np.tau = 2 * np.pi
    norm_const = 1.0 / ( math.pow(np.tau, float(size) / 2) * math.pow(det, 1.0 / 2))
    x_mu = np.matrix(x - mu)
    inv = np.linalg.inv(sigma)
    result = math.pow(math.e, -0.5 * (x_mu * inv * x_mu.T))
    return norm_const * result


def gauss2d_pdf(x_, y_, sigma=None, mu=None):
    '''
    Input: x and y coordinate of a 2D gaussian
           sigma, mu - covariance and mean vector
    Output: The probability density at that point
    '''
    if sigma is None:
        sigma = np.eye(2)
    if mu is None:
        mu = np.array([0, 0])
    x = array([x_, y_])
    size = len(x)
    if size == len(mu) and (size, size) == sigma.shape:
        det = npl.det(sigma)
        if det == 0:
            raise NameError('The covariance matrix cant be singular')
    denom1 = np.tau ** (size / 2.0)
    denom2 = np.sqrt(det)
    norm_const = 1.0 / (denom1 * denom2)
    x_mu = x - mu  # deviation from mean
    invSigma = npl.inv(sigma)  # inverse covariance
    exponent = -0.5 * (x_mu.dot(invSigma).dot(x_mu.T))
    result = norm_const * np.exp(exponent)
    return result


def rotation_mat3x3(radians):
    sin_ = sin(radians)
    cos_ = cos(radians)
    R = array(((cos_, -sin_,  0),
               (sin_,  cos_,  0),
               (   0,     0,  1),))
    return R


def rotation_mat2x2(theta):
    sin_ = sin(theta)
    cos_ = cos(theta)
    rot_ = array(((cos_, -sin_),
                  (sin_,  cos_),))
    return rot_


def rotation_around_mat3x3(theta, x, y):
    sin_ = sin(theta)
    cos_ = cos(theta)
    tr1_ = array([[1, 0, -x],
                  [0, 1, -y],
                  [0, 0, 1]])
    rot_ = array([[cos_, -sin_, 0],
                  [sin_, cos_,  0],
                  [   0,    0,  1]])
    tr2_ = array([[1, 0, x],
                  [0, 1, y],
                  [0, 0, 1]])
    rot = tr2_.dot(rot_).dot(tr1_)
    return rot


def translation_mat3x3(x, y, dtype=TRANSFORM_DTYPE):
    T = array([[1, 0,  x],
               [0, 1,  y],
               [0, 0,  1]], dtype=dtype)
    return T


def scale_mat3x3(sx, sy=None, dtype=TRANSFORM_DTYPE):
    sy = sx if sy is None else sy
    S = array([[sx, 0, 0],
               [0, sy, 0],
               [0,  0, 1]], dtype=dtype)
    return S


def scaleedoffset_mat3x3(offset, scale_factor):
    sfy = sfx = scale_factor
    T = translation_mat3x3(*offset)
    S = scale_mat3x3(sfx, sfy)
    M = T.dot(S)
    return M


# Ensure that a feature doesn't have multiple assignments
# --------------------------------
# Linear algebra functions on lower triangular matrices


#PYX DEFINE
def det_ltri(ltri):
    #cdef det_ltri(FLOAT_2D ltri):
    'Lower triangular determinant'
    #PYX CDEF FLOAT_1D det
    det = ltri[0] * ltri[2]
    return det


#PYX DEFINE
def inv_ltri(ltri, det):
    #cdef inv_ltri(FLOAT_2D ltri, FLOAT_1D det):
    'Lower triangular inverse'
    # PYX CDEF FLOAT_2D inv_ltri
    inv_ltri = array((ltri[2], -ltri[1], ltri[0]), dtype=ltri.dtype) / det
    return inv_ltri


#PYX BEGIN
def dot_ltri(ltri1, ltri2):
    #cdef dot_ltri(FLOAT_2D ltri1, FLOAT_2D ltri2):
    'Lower triangular dot product'
    # PYX FLOAT_1D m11, m21, m22
    # PYX FLOAT_1D n11, n21, n22
    # PYX FLOAT_1D o11, o21, o22
    # PYX FLOAT_2D ltri3
    # use m, n, and o as temporary matrixes
    m11, m21, m22 = ltri1
    n11, n21, n22 = ltri2
    o11 = (m11 * n11)
    o21 = (m21 * n11) + (m22 * n21)
    o22 = (m22 * n22)
    ltri3 = array((o11, o21, o22), dtype=ltri1.dtype)
    return ltri3
# PYX END CDEF


def nearest_point(x, y, pts, mode='random'):
    """ finds the nearest point(s) in pts to (x, y) """
    dists = (pts.T[0] - x) ** 2 + (pts.T[1] - y) ** 2
    fx = dists.argmin()
    mindist = dists[fx]
    other_fx = np.where(mindist == dists)[0]
    if len(other_fx) > 0:
        if mode == 'random':
            np.random.shuffle(other_fx)
            fx = other_fx[0]
        if mode == 'all':
            fx = other_fx
        if mode == 'first':
            fx = fx
    return fx, mindist


def and_lists(*args):
    """ Like np.logical_and, but can take more than 2 arguments """
    # TODO: Cython
    flags =  reduce(np.logical_and, args)
    #assert len(args) >= 1
    #flags_ = args[0]
    #for arg in args[1:]:
        #flags_ = np.logical_and(flags_, arg)
    #try:
        #print('fixme')
        #assert np.all(flags_ == flags), 'reduce has problems'
    #except Exception as ex:
        #utool.print_exception(ex)
        #print(flags_)
        #print(flags)
        #raise
    return flags


def ori_distance(ori1, ori2):
    """ Returns how far off determinants are from one another """
    # TODO: Cython
    ori_dist = np.abs(ori1 - ori2) % np.tau
    ori_dist = np.minimum(ori_dist, np.tau - ori_dist)
    return ori_dist


def det_distance(det1, det2):
    """ Returns how far off determinants are from one another """
    # TODO: Cython
    det_dist = det1 / det2
    # Flip ratios that are less than 1
    _flip_flag = det_dist < 1
    det_dist[_flip_flag] = (1.0 / det_dist[_flip_flag])
    return det_dist


def L1(hist1, hist2):
    """ returns L1 (aka manhatten or grid) distance between two histograms """
    return (np.abs(hist1 - hist2)).sum(-1)


def L2_sqrd(hist1, hist2):
    """ returns the squared L2 distance
    seealso L2
    """
    # TODO: Cython
    return (np.abs(hist1 - hist2) ** 2).sum(-1)


def L2(hist1, hist2):
    """ returns L2 (aka euclidean or standard) distance between two histograms """
    return np.sqrt((np.abs(hist1 - hist2) ** 2).sum(-1))


def hist_isect(hist1, hist2):
    """ returns histogram intersection distance between two histograms """
    numer = (np.dstack([hist1, hist2])).min(-1).sum(-1)
    denom = hist2.sum(-1)
    hisect_dist = 1 - (numer / denom)
    if len(hisect_dist) == 1:
        hisect_dist = hisect_dist[0]
    return hisect_dist


def whiten_xy_points(xy_m):
    """
    whitens points to mean=0, stddev=1 and returns transformation
    """
    mu_xy  = xy_m.mean(1)  # center of mass
    std_xy = xy_m.std(1)
    std_xy[std_xy == 0] = 1  # prevent divide by zero
    tx, ty = -mu_xy / std_xy
    sx, sy = 1 / std_xy
    T = np.array([(sx, 0, tx),
                  (0, sy, ty),
                  (0,  0,  1)])
    xy_norm = ((xy_m.T - mu_xy) / std_xy).T
    return xy_norm, T


def homogonize(_xyzs):
    """ normalizes 3d homogonous coordinates into 2d coordinates """
    _xs, _ys, _zs = _xyzs
    _xys = np.vstack((_xs / _zs, _ys / _zs))
    return _xys


def rowwise_operation(arr1, arr2, op):
    """
    performs an operation between an
    (N x A x B ... x Z) array with an
    (N x 1) array
    """
    # FIXME: not sure this is the correct terminology
    assert arr1.shape[0] == arr2.shape[0]
    broadcast_dimensions = arr1.shape[1:]
    tileshape = tuple(list(broadcast_dimensions) + [1])
    arr2_ = np.rollaxis(np.tile(arr2, tileshape), -1)
    return op(arr1, arr2_)


def rowwise_division(arr1, arr2):
    return rowwise_operation(arr1, arr2, np.divide)


def compare_matrix_columns(matrix, columns):
    # FIXME: Generalize
    #row_matrix = matrix.T
    #row_list   = columns.T
    return compare_matrix_to_rows(matrix.T, columns.T).T


def compare_matrix_to_rows(row_matrix, row_list, comp_op=np.equal, logic_op=np.logical_or):
    # FIXME: Generalize
    '''
    Compares each row in row_list to each row in row matrix using comp_op
    Both must have the same number of columns.
    Performs logic_op on the results of each individual row

    compop   = np.equal
    logic_op = np.logical_or
    '''
    row_result_list = [array([comp_op(matrow, row) for matrow in row_matrix])
                       for row in row_list]
    output = row_result_list[0]
    for row_result in row_result_list[1:]:
        output = logic_op(output, row_result)
    return output
