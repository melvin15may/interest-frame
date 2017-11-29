import cv2
import numpy as np,sys

def pyramid_blend(A,B,axis):
    #A = cv2.imread(image1)
    #B = cv2.imread(image)

    # generate Gaussian pyramid for A
    #A = cv2.copyMakeBorder(A, 27,26,16,16, cv2.BORDER_CONSTANT)

    G = A.copy()
    gpA = [G]
    for i in range(2):
        G = cv2.pyrDown(G)
        gpA.append(G)

    # generate Gaussian pyramid for B
    #B = cv2.copyMakeBorder(B, 27,26,16,16, cv2.BORDER_CONSTANT)
    G = B.copy()
    gpB = [G]
    for i in range(2):
        G = cv2.pyrDown(G)
        gpB.append(G)

    # generate Laplacian Pyramid for A
    lpA = [gpA[1]]
    for i in range(1,0,-1):
        GE = cv2.pyrUp(gpA[i])
        L = cv2.subtract(gpA[i-1],GE)
        lpA.append(L)

    # generate Laplacian Pyramid for B
    lpB = [gpB[1]]
    for i in range(1,0,-1):
        GE = cv2.pyrUp(gpB[i])
        L = cv2.subtract(gpB[i-1],GE)
        lpB.append(L)

    # Now add left and right halves of images in each level
    LS = []
    for la,lb in zip(lpA,lpB):
        rows,cols,dpt = la.shape
        #print(la.shape)
        if axis==1:
            ls = np.hstack((la, lb))
        else:
            ls = np.vstack((la, lb))
        #ls = np.vstack((la, lb))
        LS.append(ls)

    # now reconstruct
    ls_ = LS[0]
    for i in range(1,2):
        ls_ = cv2.pyrUp(ls_)
        ls_ = cv2.add(ls_, LS[i])

    # image with direct connecting each half
    # real = np.hstack((A[:,:int(cols/2)],B[:,int(cols/2):]))
    return ls_