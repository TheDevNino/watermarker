import cv2 as cv


def drawCross(img, pos_xy, size, text):
    size = size // 2
    color = (150, 50, 255)
    lw = 2
    for r in [size * .8, size * .5]:
        cv.circle(img, pos_xy, int(r), color, thickness=lw)
    cv.line(img, pt1=(pos_xy[0], pos_xy[1] - size),
            pt2=(pos_xy[0], pos_xy[1] + size),
            color=color, thickness=lw)
    cv.line(img, pt1=(pos_xy[0] - size, pos_xy[1]),
            pt2=(pos_xy[0] + size, pos_xy[1]),
            color=color, thickness=lw)
    cv.rectangle(img, pt1=(pos_xy[0] - size, pos_xy[1] - size),
                 pt2=(pos_xy[0] + size, pos_xy[1] + size),
                 color=color, thickness=lw)

    font = cv.FONT_HERSHEY_DUPLEX
    cv.putText(img, text=text,
               org=(pos_xy[0] - size, pos_xy[1] - size - 10),
               fontFace=font, fontScale=.8,
               color=color, thickness=2,
               lineType=cv.LINE_AA)


img = cv.imread('opencv_data/messi5.jpg')
drawCross(img, pos_xy=(365, 310), size=60, text="Hier ist der Ball")

cv.imshow('img', img)
cv.waitKey(0)
