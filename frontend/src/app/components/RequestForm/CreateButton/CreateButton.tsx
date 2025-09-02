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
          申請用に加工
        </button>
      </div>
    </div>
  );
};

export default CreateButton;
