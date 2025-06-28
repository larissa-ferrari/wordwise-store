import React from 'react';
import Navbar from '../components/Navbar/Navbar';
import Banner from '../components/Banner/Banner';
import CategoryCarousel from '../components/CategoryCarousel/CategoryCarousel';
import BookHighlights from '../components/BookHighlights/BookHighlights';
import Newsletter from '../components/Newsletter/Newsletter';
import Footer from '../components/Footer/Footer';


function Home() {
  return (
    <div>
      <Navbar />
      <Banner />
      <CategoryCarousel />
      <BookHighlights />
      <Newsletter />
      <Footer />
    </div>
  );
}

export default Home;
