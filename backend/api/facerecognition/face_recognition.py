import torch
from torchvision import transforms
from face_alignment import align
from backbones import get_model
from torch.nn.functional import normalize, cosine_similarity

'''
face_alignmentとbackbonesはライブラリとして使用しているようなので、
Flaskで扱う場合は、ファルダごと、venvのLib/site-packagesの中に入れてください。
'''

#クラス化
class FaceRecognizer:
    def __init__(self, model_name="edgeface_xs_gamma_06"):
        self.model = get_model(model_name)
        checkpoint_path = f'./api/facerecognition/checkpoints/{model_name}.pt'
        state_dict = torch.load(checkpoint_path, map_location='cpu')
        self.model.load_state_dict(state_dict)
        self.model.eval()
        self.transform = transforms.Compose([
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.5]*3, std=[0.5]*3)
        ])

    def get_feature(self, image_path):
        aligned = align.get_aligned_face(image_path)
        if aligned is None:
            raise ValueError("顔が検出できませんでした")
        tensor = self.transform(aligned).unsqueeze(0)
        with torch.no_grad():
            return normalize(self.model(tensor))

    def similarity(self, path1, path2):
        emb1 = self.get_feature(path1)
        emb2 = self.get_feature(path2)
        sim = cosine_similarity(emb1, emb2).item()
        return f"Similarity: {sim:.4f}"