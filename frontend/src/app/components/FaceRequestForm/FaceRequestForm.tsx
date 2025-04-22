"use client";

import React, { useState } from "react";
import MultiImageUploader from "./MultiImageUpload/MultiImageUpload";
import Image from "next/image";
import MultiRequestButton from "./Button/MultiRequestButton";

const FaceRequestForm = () => {
  const allowedTypes = ["image/jpg", "image/jpeg", "image/png"];
  const maxSize = 10 * 1024 * 1024; // 10MB
  const [previewSrcs, setPreviewSrcs] = useState<string[]>([]);
  const [uploadedFiles, setUploadedFiles] = useState<File[]>([]);
  const [uperrorMessage, setUpErrorMessage] = useState("");
  const [responseData, setResponseData] = useState<string | undefined>();
  const [loading, setLoading] = useState(false);

  //画像アップロード
  const handleImageUpload = (images: { src: string; file: File }[]) => {
    setPreviewSrcs(images.map((img) => img.src));
    setUploadedFiles(images.map((img) => img.file));
    setUpErrorMessage("");
    // setCreateButtonVisible(false);
  };

  const handleError = (message: string) => {
    setUpErrorMessage(message);
  };

  //APIリクエスト
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault(); // ←これ必須！

    if (uploadedFiles.length < 2) {
      setUpErrorMessage("2枚の画像をアップロードしてください。");
      return;
    }

    const formData = new FormData();
    formData.append("file1", uploadedFiles[0]);
    formData.append("file2", uploadedFiles[1]);

    try {
      const response = await fetch("http://localhost:5000/face", {
        method: "POST",
        body: formData,
      });

      if (!response.ok) {
        throw new Error("画像の送信に失敗しました。");
      }

      const data = await response.json();
      console.log("APIの返却値:", data);
      setResponseData(data.message);

      // 必要に応じて画像結果やメッセージをUIへ表示
      // setPreviewSrcs([data.result1, data.result2]) なども可
    } catch (error) {
      console.error("送信中にエラー:", error);
      setUpErrorMessage("APIリクエスト中にエラーが発生しました。");
    }
  };

  return (
    <div>
      <main id="main" className="main">
        <form onSubmit={handleSubmit}>
          <div className="uploadArea">
            <MultiImageUploader
              allowedTypes={allowedTypes}
              maxSize={maxSize}
              onImageUpload={handleImageUpload}
              onError={handleError}
            />
            <div id="flow" className="uploadAreaFlow">
              <div className="uploadAreaFlow_inner" style={{ display: "flex" }}>
                <div className="uploadAreaFlow_col">
                  <p className="uploadAreaFlow_ttl">選択画像</p>
                  <div className="uploadAreaFlow_img">
                    {previewSrcs[0] && (
                      <Image
                        id="preview"
                        src={previewSrcs[0]}
                        alt="プレビュー画像"
                        width={150}
                        height={150}
                        unoptimized
                      />
                    )}
                  </div>
                </div>
                <div className="uploadAreaFlow_arrow"></div>
                <div className="uploadAreaFlow_col">
                  <p className="uploadAreaFlow_ttl">選択画像２</p>
                  <div className="uploadAreaFlow_img">
                    <div id="loading" className="uploadAreaLoading">
                      {previewSrcs[1] && (
                        <Image
                          id="loadingImage"
                          src={previewSrcs[1]}
                          alt=""
                          width={150}
                          height={150}
                        />
                      )}
                    </div>
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
              <pre>判定結果 {responseData}</pre>
            )}
          </div>

          {/* 申込画像作成ボタン */}
          <MultiRequestButton type="submit" />
        </form>
      </main>
    </div>
  );
};

export default FaceRequestForm;
