import torch
from torchvision import transforms
from face_alignment import align
from backbones import get_model
from torch.nn.functional import normalize, cosine_similarity

# load model
model_name="edgeface_xs_gamma_06" # or edgeface_xs_gamma_06
model=get_model(model_name)
checkpoint_path=f'checkpoints/{model_name}.pt'
#model.load_state_dict(torch.load(checkpoint_path, map_location='cpu')).eval()
state_dict = torch.load(checkpoint_path, map_location='cpu')
model.load_state_dict(state_dict)
model.eval()

transform = transforms.Compose([
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.5, 0.5, 0.5], std=[0.5, 0.5, 0.5]),
            ])

def get_feature(path):
    aligned = align.get_aligned_face(path) # align face
    if aligned is None:
        print("顔が検出できませんでした")
    else:
        print("顔検出成功。aligned.jpg に保存しました")
    transformed_input = transform(aligned) # preprocessing
    transformed_input = transformed_input.unsqueeze(0)  # [1, 3, 112, 112]

    with torch.no_grad():
        embedding = normalize(model(transformed_input))  # L2正規化

    # extract embedding
    #embedding = model(transformed_input)

    return embedding

path1 = './face1.jpg'
path2 = './face2.jpg'

# res = get_feature(path1)
# print(res)

sim = cosine_similarity(get_feature(path1), get_feature(path2)).item()
print(f"Similarity: {sim:.4f}")