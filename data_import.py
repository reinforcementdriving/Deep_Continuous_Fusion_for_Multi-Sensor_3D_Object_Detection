import numpy as np
import torch
from PIL import Image, ImageDraw

def getRect(x, y, width, height, angle):
    rect = np.array([(-width/2, -height/2), (width/2, -height/2),
                    (width/2, height/2), (-width/2, height/2),
                     (-width/2, -height/2)])
    theta = angle
    R = np.array([[np.cos(theta), -np.sin(theta)],
                  [np.sin(theta), np.cos(theta)]])
    offset = np.array([x, y])
    transformed_rect = np.dot(rect, R) + offset
    return transformed_rect

def putBoundingBox(lidar_image, reference_bboxes, color=1):
    lidar_image_with_bbox = lidar_image.cpu().clone().numpy()
    # lidar_image_with_bbox = np.tile(lidar_image, (1, 1, 3))
    # print(lidar_image_with_bbox.shape)
    img = Image.fromarray((255*lidar_image_with_bbox).astype(np.uint8))
    draw = ImageDraw.Draw(img)
    for bbox in reference_bboxes:
        x = int(bbox[1]*10+350)
        y = int(bbox[0]*10)
        width = bbox[3]*10
        height = bbox[4]*10
        angle = bbox[6] - 1.57
        rect = getRect(x=x, y=y, width=width, height=height, angle=angle)
        draw.polygon([tuple(p) for p in rect], fill=color)
    lidar_image_with_bbox = np.asarray(img)
    return torch.tensor(lidar_image_with_bbox)
