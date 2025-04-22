import React from "react";

const Facelayout = ({
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

export default Facelayout;
