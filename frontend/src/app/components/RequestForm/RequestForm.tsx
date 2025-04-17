import { useApiRequest } from "@/app/hooks/useApiRequest";
import React, { useState } from "react";
import ImageUploader from "./ImageUpload/ImageUploader";
import Image from "next/image";
import CreateButton from "./CreateButton/CreateButton";
import ReloadButton from "./ReloadButton/ReloadButton";

import "./RequestForm.css";

const RequestForm = () => {
  const allowedTypes = ["image/jpg", "image/jpeg", "image/png"];
  const maxSize = 10 * 1024 * 1024; // 10MB
  const [isHidden, setIsHidden] = useState(true);
  const [isUploadButtonVisible, setIsUploadButtonVisible] = useState(true);
  const [createButtonVisible, setCreateButtonVisible] = useState(true);
  const [reflectButtonVisible, setReflectButtonVisible] = useState(true);
  const [previewSrc, setPreviewSrc] = useState("https://placehold.jp/x150.png");
  const [uploadedFile, setUploadedFile] = useState<File | null>(null);
  const [uperrorMessage, setUpErrorMessage] = useState("");
  const [loading, setLoading] = useState(false);

  // APIへPOSTするFetch処理
  const {
    responseData,
    resultImageSrc,
    resultNormalArea,
    resultAbnormalityArea,
    error,
    errorMessage,
    handleApiRequest,
  } = useApiRequest();

  //画像アップロード
  const handleImageUpload = (src: string, file: File) => {
    setPreviewSrc(src);
    setUploadedFile(file);
    setUpErrorMessage("");
    setIsHidden(false);
    setCreateButtonVisible(false);
  };

  const handleError = (message: string) => {
    setUpErrorMessage(message);
  };

  // フォーム送信処理
  const handleSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    setLoading(true); // Loading 開始
    await handleApiRequest(uploadedFile);
    setLoading(false); // Loading 終了
    setCreateButtonVisible(true);
    setReflectButtonVisible(false);
  };

  return (
    <div>
      <main id="main" className="main">
        <form onSubmit={handleSubmit}>
          <div className="uploadArea">
            {isUploadButtonVisible && (
              <ImageUploader
                allowedTypes={allowedTypes}
                maxSize={maxSize}
                onImageUpload={handleImageUpload}
                onError={handleError}
              />
            )}

            <div
              id="flow"
              className="uploadAreaFlow"
              style={{ display: isHidden ? "none" : "block" }}
            >
              <div className="uploadAreaFlow_inner">
                <div className="uploadAreaFlow_col">
                  <p className="uploadAreaFlow_ttl">選択画像</p>
                  <div className="uploadAreaFlow_img">
                    <Image
                      id="preview"
                      src={previewSrc}
                      alt="プレビュー画像"
                      width={150}
                      height={150}
                      unoptimized
                    />
                  </div>
                </div>
                <div className="uploadAreaFlow_arrow"></div>
                <div className="uploadAreaFlow_col">
                  <p className="uploadAreaFlow_ttl">検出顔写真</p>
                  <div className="uploadAreaFlow_img">
                    {/* ローディング処理 */}
                    {loading ? (
                      <div id="loading" className="uploadAreaLoading">
                        <Image
                          id="loadingImage"
                          src="/img/loading.png"
                          alt=""
                          width={150}
                          height={150}
                        />
                      </div>
                    ) : (
                      <Image
                        id="resultImage"
                        src={resultImageSrc}
                        alt="結果画像"
                        width={150}
                        height={150}
                        style={{ display: isHidden ? "none" : "block" }}
                        unoptimized
                      />
                    )}
                  </div>
                </div>
              </div>
            </div>
          </div>
          {/* 判定結果 */}
          <div className="messageloading">
            {loading ? (
              <pre>画像アップロード中...</pre>
            ) : (
              <div
                id="clearMessage"
                className="resultArea -clear"
                style={{ display: resultNormalArea ? "none" : "block" }}
              >
                {<pre>判定結果 {responseData}</pre>}
              </div>
            )}
          </div>
          <div
            id="errorMessage"
            className="resultArea -error"
            style={{ display: resultAbnormalityArea ? "none" : "block" }}
          >
            {error ? (
              <pre
                style={{
                  color: "red",
                }}
              >
                想定外のエラーです。メッセージ内容：&nbsp;
                {errorMessage}
              </pre>
            ) : (
              <pre>{responseData}</pre>
            )}
          </div>

          {/* 申込画像作成ボタン */}
          <CreateButton
            createButtonVisible={createButtonVisible}
            type="submit"
          />
        </form>

        {/* <ReflectButton reflectButtonVisible={reflectButtonVisible} /> */}
        {/* やり直しボタン */}
        <ReloadButton isHidden={isHidden} />
      </main>
    </div>
  );
};

export default RequestForm;
