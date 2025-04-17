import { useState } from "react";
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
          // if (img.width < 413 || img.height < 531) {
          //   onError(
          //     "写真の解像度が低いです。画像の横幅が最低413px、縦幅が最低531px必要です。"
          //   );
          //   return;
          // }

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
        <label htmlFor="upfile" className="uploadAreaBtn">
          <Image
            src="/img/ic_photo.svg"
            width={21}
            height={20}
            className="icon-photo"
            alt=""
          />
          画像を選択
          <input
            type="file"
            id="upfile"
            onChange={(e) => handleFileChange(e.target as HTMLInputElement)}
          />
        </label>
      )}
    </>
  );
};

export default ImageUploader;
