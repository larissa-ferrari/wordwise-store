import React from 'react';
import './Banner.css';
import bannerImage from '../assets/banner.png'; // substitua com seu arquivo real

function Banner() {
  return (
    <div className="banner">
      <img src={bannerImage} alt="Banner Book Club" className="banner-img" />
    </div>
  );
}

export default Banner;
