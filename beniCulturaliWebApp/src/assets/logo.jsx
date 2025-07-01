import React from "react";

export default function Logo({logo, testoLogo}) {
    return <>
     <p>{testoLogo}</p>
     <img src={logo} alt="logo" />
    </>
}