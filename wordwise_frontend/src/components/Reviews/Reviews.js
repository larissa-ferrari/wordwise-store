import React from "react";
import "./Reviews.css";

const mockReviews = [
  {
    id: 1,
    user: "Ana",
    comment: "Livro maravilhoso! Entrega rápida e bem embalado.",
    rating: 5,
  },
  {
    id: 2,
    user: "Carlos",
    comment: "Gostei muito da qualidade da edição.",
    rating: 4,
  },
];

function Reviews() {
  return (
    <div className="reviews-container">
      <h3>Feedback dos Clientes</h3>
      {mockReviews.map((review) => (
        <div key={review.id} className="review">
          <div className="review-header">
            <strong>{review.user}</strong>
            <span className="rating">
              {"★".repeat(review.rating)}{"☆".repeat(5 - review.rating)}
            </span>
          </div>
          <p>{review.comment}</p>
        </div>
      ))}
    </div>
  );
}

export default Reviews;
