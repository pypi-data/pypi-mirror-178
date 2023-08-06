from dataclasses import dataclass
from typing import List, Optional

CocoBbox = List[float]
"""x, y, w, h"""

COCO_PERMANENT_ANNOTATIONS = [
    "id_",
    "image_id",
    "category_id",
    "segmentation",
    "area",
    "bbox",
    "iscrowd",
    "keypoints",
    "num_keypoints",
]


class SuperClass:
    def asdict(self) -> dict:
        pass


@dataclass
class CocoAnnotation(SuperClass):
    #  DENIS: does this depend on the format? Can this be extended?
    area: float
    bbox: CocoBbox
    category_id: int
    id_: int  # DENIS: how is this translated to the json. => maybe a wrapper around asdict
    image_id: int
    iscrowd: int
    segmentation: List  # DENIS: this is actually some union
    keypoints: Optional[List[int]] = None
    num_keypoints: Optional[int] = None
    track_id: Optional[int] = None
    encord_track_uuid: Optional[str] = None
    rotation: Optional[float] = None


@dataclass
class EncordCocoMetadata:
    image_id: int
    image_url: str
    image_path: str
    image_title: str
    label_hash: str
    data_hash: str


def to_attributes_field(res: dict, include_null_annotations: bool = False) -> dict:
    res_tmp = {}
    for key, value in res.items():
        if value is None and not include_null_annotations:
            continue

        if key in COCO_PERMANENT_ANNOTATIONS:
            if key == "id_":
                res_tmp["id"] = value
            else:
                res_tmp[key] = value
        else:
            attr = res_tmp.setdefault("attributes", {})
            attr[key] = value
    return res_tmp
