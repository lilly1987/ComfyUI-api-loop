import json
from urllib import request, parse
import random

#This is the ComfyUI api prompt format.

#If you want it for a specific workflow you can "enable dev mode options"
#in the settings of the UI (gear beside the "Queue Size: ") this will enable
#a button on the UI to save workflows in api format.

#keep in mind ComfyUI is pre alpha software so this format will change a bit.

#this is the one for the default workflow
prompt_text1 = """
{
    "3": {
        "class_type": "KSampler",
        "inputs": {
            "cfg": 8,
            "denoise": 1,
            "latent_image": [
                "5",
                0
            ],
            "model": [
                "4",
                0
            ],
            "negative": [
                "7",
                0
            ],
            "positive": [
                "6",
                0
            ],
            "sampler_name": "euler",
            "scheduler": "normal",
            "seed": 8566257,
            "steps": 20
        }
    },
    "4": {
        "class_type": "CheckpointLoaderSimple",
        "inputs": {
            "ckpt_name": "2d\\\\xFlareMixS2_anime.safetensors"
        }
    },
    "5": {
        "class_type": "EmptyLatentImage",
        "inputs": {
            "batch_size": 1,
            "height": 512,
            "width": 512
        }
    },
    "6": {
        "class_type": "CLIPTextEncode",
        "inputs": {
            "clip": [
                "4",
                1
            ],
            "text": "masterpiece best quality girl"
        }
    },
    "7": {
        "class_type": "CLIPTextEncode",
        "inputs": {
            "clip": [
                "4",
                1
            ],
            "text": "bad hands"
        }
    },
    "8": {
        "class_type": "VAEDecode",
        "inputs": {
            "samples": [
                "3",
                0
            ],
            "vae": [
                "4",
                2
            ]
        }
    },
    "9": {
        "class_type": "SaveImage",
        "inputs": {
            "filename_prefix": "ComfyUI",
            "images": [
                "8",
                0
            ]
        }
    }
}
"""

prompt_text="""
{
  "KSampler": {
    "inputs": {
      "seed": 890115323374972,
      "steps": 20,
      "cfg": 3,
      "sampler_name": "dpmpp_3m_sde",
      "scheduler": "karras",
      "denoise": 1,
      "model": [
        "CheckpointLoaderSimple",
        0
      ],
      "positive": [
        "ImpactWildcardEncode1",
        2
      ],
      "negative": [
        "ImpactWildcardEncode2",
        2
      ],
      "latent_image": [
        "5",
        0
      ]
    },
    "class_type": "KSampler",
    "_meta": {
      "title": "KSampler"
    }
  },
  "5": {
    "inputs": {
      "width": 384,
      "height": 768,
      "batch_size": 1
    },
    "class_type": "EmptyLatentImage",
    "_meta": {
      "title": "Empty Latent Image"
    }
  },
  "8": {
    "inputs": {
      "samples": [
        "KSampler",
        0
      ],
      "vae": [
        "VAELoader",
        0
      ]
    },
    "class_type": "VAEDecode",
    "_meta": {
      "title": "VAE Decode"
    }
  },
  "SaveImage1": {
    "inputs": {
      "filename_prefix": [
        "55",
        0
      ],
      "images": [
        "8",
        0
      ]
    },
    "class_type": "SaveImage",
    "_meta": {
      "title": "Save Image"
    }
  },
  "ImpactWildcardEncode1": {
    "inputs": {
      "wildcard_text": "",
      "populated_text": "",
      "mode": true,
      "Select to add LoRA": "Select the LoRA to add to the text",
      "Select to add Wildcard": "Select the Wildcard to add to the text",
      "seed": 387677219282618,
      "model": [
        "CheckpointLoaderSimple",
        0
      ],
      "clip": [
        "CheckpointLoaderSimple",
        1
      ]
    },
    "class_type": "ImpactWildcardEncode",
    "_meta": {
      "title": "ImpactWildcardEncode"
    }
  },
  "CheckpointLoaderSimple": {
    "inputs": {
      "ckpt_name": "2d\\\\xFlareMixS2_anime.safetensors"
    },
    "class_type": "CheckpointLoaderSimple",
    "_meta": {
      "title": "Load Checkpoint"
    }
  },
  "ImpactWildcardEncode2": {
    "inputs": {
      "wildcard_text": "",
      "populated_text": "",
      "mode": true,
      "Select to add LoRA": "Select the LoRA to add to the text",
      "Select to add Wildcard": "Select the Wildcard to add to the text",
      "seed": 757989997184339,
      "model": [
        "CheckpointLoaderSimple",
        0
      ],
      "clip": [
        "CheckpointLoaderSimple",
        1
      ]
    },
    "class_type": "ImpactWildcardEncode",
    "_meta": {
      "title": "ImpactWildcardEncode"
    }
  },
  "VAELoader": {
    "inputs": {
      "vae_name": "clearvae_v23.safetensors"
    },
    "class_type": "VAELoader",
    "_meta": {
      "title": "Load VAE"
    }
  },
  "DetailerForEachDebug": {
    "inputs": {
      "guide_size": 256,
      "guide_size_for": true,
      "max_size": 512,
      "seed": 647318466108458,
      "steps": 20,
      "cfg": 3,
      "sampler_name": "dpmpp_3m_sde",
      "scheduler": "karras",
      "denoise": 0.38,
      "feather": 5,
      "noise_mask": true,
      "force_inpaint": true,
      "wildcard": "",
      "cycle": 1,
      "inpaint_model": false,
      "noise_mask_feather": 0,
      "image": [
        "8",
        0
      ],
      "segs": [
        "49",
        0
      ],
      "model": [
        "CheckpointLoaderSimple",
        0
      ],
      "clip": [
        "CheckpointLoaderSimple",
        1
      ],
      "vae": [
        "VAELoader",
        0
      ],
      "positive": [
        "ImpactWildcardEncode1",
        2
      ],
      "negative": [
        "ImpactWildcardEncode2",
        2
      ]
    },
    "class_type": "DetailerForEachDebug",
    "_meta": {
      "title": "DetailerDebug (SEGS)"
    }
  },
  "49": {
    "inputs": {
      "threshold": 0.38,
      "dilation": 10,
      "crop_factor": 3,
      "drop_size": 10,
      "labels": "",
      "bbox_detector": [
        "61",
        0
      ],
      "image": [
        "8",
        0
      ]
    },
    "class_type": "BboxDetectorSEGS",
    "_meta": {
      "title": "BBOX Detector (SEGS)"
    }
  },
  "SaveImage2": {
    "inputs": {
      "filename_prefix": [
        "55",
        0
      ],
      "images": [
        "DetailerForEachDebug",
        0
      ]
    },
    "class_type": "SaveImage",
    "_meta": {
      "title": "Save Image"
    }
  },
  "55": {
    "inputs": {
      "action": "append",
      "tidy_tags": "yes",
      "text_a": "xFlareMix_semireal",
      "text_b": "",
      "text_c": "",
      "result": "xFlareMix_semireal"
    },
    "class_type": "StringFunction|pysssss",
    "_meta": {
      "title": "String Function 🐍"
    }
  },
  "61": {
    "inputs": {
      "model_name": "bbox/face_yolov8m.pt"
    },
    "class_type": "UltralyticsDetectorProvider",
    "_meta": {
      "title": "UltralyticsDetectorProvider"
    }
  },
  "PreviewImage1": {
    "inputs": {
      "images": [
        "DetailerForEachDebug",
        1
      ]
    },
    "class_type": "PreviewImage",
    "_meta": {
      "title": "Preview Image"
    }
  },
  "PreviewImage2": {
    "inputs": {
      "images": [
        "DetailerForEachDebug",
        2
      ]
    },
    "class_type": "PreviewImage",
    "_meta": {
      "title": "Preview Image"
    }
  },
  "PreviewImage3": {
    "inputs": {
      "images": [
        "DetailerForEachDebug",
        3
      ]
    },
    "class_type": "PreviewImage",
    "_meta": {
      "title": "Preview Image"
    }
  },
  "PreviewImage4": {
    "inputs": {
      "images": [
        "DetailerForEachDebug",
        4
      ]
    },
    "class_type": "PreviewImage",
    "_meta": {
      "title": "Preview Image"
    }
  }
}
"""

def queue_prompt(prompt):
    p = {"prompt": prompt}
    data = json.dumps(p).encode('utf-8')
    req =  request.Request("http://127.0.0.1:8288/prompt", data=data)
    request.urlopen(req)


prompt = json.loads(prompt_text)
#set the text prompt for our positive CLIPTextEncode
#prompt["6"]["inputs"]["text"] = "masterpiece best quality man"

#set the seed for our KSampler node
#prompt["3"]["inputs"]["seed"] = 5

prompt["CheckpointLoaderSimple"]["inputs"]["ckpt_name"]= "2d/xFlareMixS2_anime.safetensors"
prompt["ImpactWildcardEncode1"]["inputs"]["wildcard_text"]= "masterpiece , best quality , detailed_face, cowboy shot, {from side,|9::} looking at viewer,1girl,  __char__,__chest__ , __exposure__,  thin waist,sex, large insertion, dildo riding , dildo, object insertion,{arms behind back, bound arms, bound bdsm, bdsm, |}{(open_dress:1.0), (Undressing:1.1), Nipples, (Pussy:1.1), (navel:1.0),|2::}__shoulder__,{See Through,|}__concept__,__insertion__, {<lora:microwaistV05:{0.75|0.875|1.0}:1.0>,|3::} , "
prompt["ImpactWildcardEncode2"]["inputs"]["wildcard_text"]= "lowres, worst quality, low quality,cropped, (multiple views), (multiple viewer), (cropped), face only, facial, lower body, from torso down,{-$$embedding:FastNegativeV2.pt|embedding:NGH.safetensors|embedding:bad_prompt_version2-neg.pt|embedding:negative_hand-neg|embedding:nncursedV0-neg.pt|embedding:badquality.pt|embedding:bad-picture-chill-75v.pt|embedding:neg_grapefruit.pt|embedding:ParaNegative.safetensors|embedding:easynegative.safetensors|embedding:EasyNegativeV2.safetensors},(monochrome:1.1), "


queue_prompt(prompt)


