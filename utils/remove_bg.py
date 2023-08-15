import os
import cv2
import numpy as np
from detectron2.config import get_cfg
from detectron2.engine import DefaultPredictor
from detectron2.utils.visualizer import Visualizer
from detectron2.data import MetadataCatalog

def remove_background(image_path, output_path):
    # Load a pre-trained Mask R-CNN model
    cfg = get_cfg()
    cfg.merge_from_file("COCO-InstanceSegmentation/mask_rcnn_R_50_FPN_3x.yaml")
    cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = 0.5
    cfg.MODEL.WEIGHTS = "mask_rcnn_R_50_FPN_3x.pth"
    predictor = DefaultPredictor(cfg)

    # Load the image
    image = cv2.imread(image_path)
    outputs = predictor(image)

    # Visualize the predictions (optional)
    v = Visualizer(image[:, :, ::-1], MetadataCatalog.get(cfg.DATASETS.TRAIN[0]), scale=1.2)
    v = v.draw_instance_predictions(outputs["instances"].to("cpu"))
    cv2.imshow("Predictions", v.get_image()[:, :, ::-1])
    cv2.waitKey(0)

    # Extract the mask of the sunglasses
    masks = outputs["instances"].pred_masks.cpu().numpy()
    sunglasses_mask = masks[0]

    # Create a transparent overlay of the sunglasses
    overlay = np.zeros_like(image)
    overlay[sunglasses_mask] = image[sunglasses_mask]

    # Save the overlay image
    cv2.imwrite(output_path, overlay)

if __name__ == "__main__":
    input_image_path = "path_to_input_image.jpg"
    output_image_path = "output_overlay.png"
    
    remove_background(input_image_path, output_image_path)
