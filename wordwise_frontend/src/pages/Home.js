import React from 'react';
import Navbar from '../components/Navbar';
import Banner from '../components/Banner';
import CategoryCarousel from '../components/CategoryCarousel';
import BookHighlights from '../components/BookHighlights';
import Newsletter from '../components/Newsletter';
import Footer from '../components/Footer';


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
