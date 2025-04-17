import { useState } from "react";

interface ReloadButtonProps {
  isHidden: boolean;
}

const ReloadButton: React.FC<ReloadButtonProps> = ({ isHidden }) => {
  // ページリロード
  const handleReload = () => {
    window.location.reload();
  };

  return (
    <div className="buttonArea">
      <div id="reloadBtn" style={{ display: isHidden ? "none" : "block" }}>
        <button className="btnLightblue" onClick={handleReload}>
          やり直し
        </button>
      </div>
    </div>
  );
};

export default ReloadButton;
