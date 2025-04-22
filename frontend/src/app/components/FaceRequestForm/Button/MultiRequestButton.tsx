import { useState } from "react";

interface CreateButtonProps {
  type: "submit"; // ボタンのtype属性の型
}

const MultiRequestButton: React.FC<CreateButtonProps> = ({ type }) => {
  return (
    <div className="buttonArea">
      <div className="inputBtn" id="uploadBtn">
        <button id="uploadBtnInput" type={type} className="btnBlue">
          画像アップロード
        </button>
      </div>
    </div>
  );
};

export default MultiRequestButton;
