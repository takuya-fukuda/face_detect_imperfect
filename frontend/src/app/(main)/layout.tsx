import React from "react";

const Mainlayout = ({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) => {
  return (
    <div>
      <main>{children}</main>
    </div>
  );
};

export default Mainlayout;
