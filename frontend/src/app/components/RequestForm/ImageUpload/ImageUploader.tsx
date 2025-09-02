import { useState, useRef } from "react";
import Image from "next/image";

interface ImageUploaderProps {
  allowedTypes: string[];
  maxSize: number;
  onImageUpload: (src: string, file: File) => void; // Fileを追加
  onError: (message: string) => void;
}

const ImageUploader: React.FC<ImageUploaderProps> = ({
  allowedTypes,
  maxSize,
  onImageUpload,
  onError,
}) => {
  const [isUploadButtonVisible, setIsUploadButtonVisible] = useState(true);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleButtonClick = () => {
    fileInputRef.current?.click();
  };

  const handleFileChange = (input: HTMLInputElement) => {
    if (input.files && input.files[0]) {
      const file = input.files[0];
      const fileType = file.type;
      const fileSize = file.size;

      // 拡張子確認
      if (!allowedTypes.includes(fileType)) {
        onError(
          `画像ファイルは、${allowedTypes.join(
            ", "
          )}形式のいずれかで選択してください。`
        );
        return;
      }

      // サイズチェック
      if (fileSize > maxSize) {
        onError("10MB以下の画像ファイルを選択してください。");
        return;
      }

      // ファイル読み込み
      const fileData = new FileReader();
      fileData.onload = (e) => {
        const result = e.target?.result as string | null;
        if (!result) {
          onError("ファイルの読み込みに失敗しました。");
          return;
        }

        const img = new globalThis.Image();
        img.onload = () => {
          // アップロード成功
          onImageUpload(result, file); // ファイルも渡す
          setIsUploadButtonVisible(false); // ボタンを非表示にする
        };
        img.src = result;
      };
      fileData.readAsDataURL(file);
    }
  };

  return (
    <>
      {isUploadButtonVisible && (
        <>
          <button
            type="button"
            className="uploadAreaBtn"
            onClick={handleButtonClick}
          >
            画像を選択
          </button>
          <input
            type="file"
            id="upfile"
            ref={fileInputRef}
            style={{ display: "none" }}
            onChange={(e) => handleFileChange(e.target as HTMLInputElement)}
          />
        </>
      )}
    </>
  );
};

export default ImageUploader;
