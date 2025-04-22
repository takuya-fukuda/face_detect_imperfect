import React from "react";
import Header from "../components/Header/Header";
import Footer from "../components/Footer/Footer";

const Mainlayout = ({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) => {
  return (
    <div>
      <Header />
      <main>{children}</main>
      <Footer />
    </div>
  );
};

export default Mainlayout;
