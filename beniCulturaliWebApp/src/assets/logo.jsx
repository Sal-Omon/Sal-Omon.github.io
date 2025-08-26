import React from "react";

export default function Logo({logo, testoLogo}) {
    return <>
     <img src={logo} alt="logo" />
     <p>{testoLogo}</p>
    </>
}