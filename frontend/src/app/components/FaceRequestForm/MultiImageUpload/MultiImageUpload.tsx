import { useRef, useState } from "react";
import Image from "next/image";

interface ImageUploaderProps {
  allowedTypes: string[];
  maxSize: number;
  onImageUpload: (images: { src: string; file: File }[]) => void;
  onError: (message: string) => void;
}

const MultiImageUploader: React.FC<ImageUploaderProps> = ({
  allowedTypes,
  maxSize,
  onImageUpload,
  onError,
}) => {
  const [isUploadButtonVisible, setIsUploadButtonVisible] = useState(true);

  const handleFileChange = (input: HTMLInputElement) => {
    const files = input.files;
    if (!files || files.length === 0) {
      onError("画像を選択してください。");
      return;
    }

    const selectedFiles = Array.from(files).slice(0, 2); // 最大2枚まで
    const loadedImages: { src: string; file: File }[] = [];

    selectedFiles.forEach((file) => {
      if (!allowedTypes.includes(file.type)) {
        onError(`画像は${allowedTypes.join(", ")}のいずれかにしてください`);
        return;
      }

      if (file.size > maxSize) {
        onError("10MB以下の画像ファイルを選択してください。");
        return;
      }

      const reader = new FileReader();
      reader.onload = (e) => {
        const result = e.target?.result as string | null;
        if (!result) {
          onError("画像の読み込みに失敗しました");
          return;
        }

        const img = new globalThis.Image();
        img.onload = () => {
          loadedImages.push({ src: result, file });
          if (loadedImages.length === selectedFiles.length) {
            onImageUpload(loadedImages);
            setIsUploadButtonVisible(false);
          }
        };
        img.src = result;
      };
      reader.readAsDataURL(file);
    });
  };

  const inputRef = useRef<HTMLInputElement | null>(null);
  const handleClick = () => {
    inputRef.current?.click(); // ← これがポイント！
  };

  return (
    <>
      {isUploadButtonVisible && (
        <div>
          <button
            type="button"
            onClick={handleClick}
            style={{
              padding: "10px 20px",
              backgroundColor: "blue",
              color: "white",
              border: "none",
              borderRadius: "5px",
            }}
          >
            画像を選択（最大2枚）
          </button>
          <input
            ref={inputRef}
            type="file"
            id="upfile"
            multiple
            accept={allowedTypes.join(",")}
            onChange={(e) => handleFileChange(e.target)}
            style={{ display: "none" }} // ← 重要：非表示
          />
        </div>
      )}
    </>
  );
};

export default MultiImageUploader;
