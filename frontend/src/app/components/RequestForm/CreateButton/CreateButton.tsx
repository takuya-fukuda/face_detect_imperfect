import { useState } from "react";

interface CreateButtonProps {
  createButtonVisible: boolean;
  type: "submit"; // ボタンのtype属性の型
}

const CreateButton: React.FC<CreateButtonProps> = ({
  createButtonVisible,
  type,
}) => {
  return (
    <div className="buttonArea">
      <div
        className="inputBtn"
        id="uploadBtn"
        style={{ display: createButtonVisible ? "none" : "block" }}
      >
        <button id="uploadBtnInput" type={type} className="btnBlue">
          申込用顔写真を作成する
        </button>
      </div>
    </div>
  );
};

export default CreateButton;
