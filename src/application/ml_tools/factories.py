from detectron2.config import get_cfg
from detectron2.data import MetadataCatalog
from detectron2.engine import DefaultPredictor
from detectron2.model_zoo import model_zoo

import application.settings
from application.ml_tools.constants import (
    DETECTRON_MODEL_CONFIG_FILE_PATH_MAP,
    ImageAnalysisMLTool,
)
from application.ml_tools.ml_models import Detectron2MLModel


class Detectron2ToolFactory:

    def build_model(
        self,
        analysis_type,
        threshold=application.settings.DETECTRON2_MODEL_ANALYSIS_THRESHOLD,
        processing_device=application.settings.DETECTRON2_PROCESSING_DEVICE,
    ):
        config = get_cfg()

        # Load model config and pretrained model
        config.merge_from_file(
            model_zoo.get_config_file(
                DETECTRON_MODEL_CONFIG_FILE_PATH_MAP[analysis_type]
            )
        )
        config.MODEL.WEIGHTS = model_zoo.get_checkpoint_url(
            DETECTRON_MODEL_CONFIG_FILE_PATH_MAP[analysis_type]
        )

        config.MODEL.ROI_HEADS.SCORE_THRESH_TEST = threshold
        config.MODEL.DEVICE = processing_device

        predictor = DefaultPredictor(config)
        metadata = MetadataCatalog.get(config.DATASETS.TRAIN[0])

        return Detectron2MLModel(predictor, metadata)


ml_model_factory_map = {
    ImageAnalysisMLTool.DETECTRON_2.value: Detectron2ToolFactory,
}
