import { useState } from "react";

interface ApiRequestResult {
  responseData: string | undefined;
  resultImageSrc: string;
  resultNormalArea: boolean;
  resultAbnormalityArea: boolean;
  error: boolean;
  errorMessage: string;
  handleApiRequest: (uploadedFile: File | null) => Promise<void>;
}

export const useApiRequest = (): ApiRequestResult => {
  const [responseData, setResponseData] = useState<string | undefined>();
  const [resultImageSrc, setResultImageSrc] = useState(
    "https://placehold.jp/x150.png"
  );
  const [resultNormalArea, setResultNormalArea] = useState(true);
  const [resultAbnormalityArea, setResultAbnormalityArea] = useState(true);

  const [error, setError] = useState(false);
  const [errorMessage, setErrorMessage] = useState("");

  const handleApiRequest = async (uploadedFile: File | null) => {
    if (!uploadedFile) {
      setErrorMessage("画像を選択してください");
      return;
    }

    const formData = new FormData();
    formData.append("file", uploadedFile);

    setError(false);
    setErrorMessage("");

    try {
      const response = await fetch("http://localhost:5000/image", {
        method: "POST",
        body: formData,
      });

      if (!response.ok) {
        throw new Error("画像のアップロードに失敗しました");
      }

      const data = await response.json();
      const base64Image = `data:image/jpeg;base64,${data.image}`;
      setResultImageSrc(base64Image);
      const mask: string = data.mask;
      const face: string = data.face_count;

      setResponseData(mask + ",  " + face);
      setResultNormalArea(false);
    } catch (error) {
      console.error("Error during POST request:", error);
      setError(true);
      if (error instanceof Error) {
        setErrorMessage(error.message);
      } else {
        setErrorMessage("APIのリクエストに失敗しました");
      }
      setResultAbnormalityArea(false);
    }
  };

  return {
    responseData,
    resultImageSrc,
    resultNormalArea,
    resultAbnormalityArea,
    error,
    errorMessage,
    handleApiRequest,
  };
};
