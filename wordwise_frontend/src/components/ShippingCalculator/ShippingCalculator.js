import React, { useState } from "react";
import "./ShippingCalculator.css";

function ShippingCalculator() {
  const [showForm, setShowForm] = useState(false);
  const [cep, setCep] = useState("");
  const [shipping, setShipping] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleCalculate = () => {
    setLoading(true);
    setShipping(null);
    setError("");

    setTimeout(() => {
      if (!cep || cep.length < 8) {
        setError("Por favor, insira um CEP válido.");
        setLoading(false);
        return;
      }
      setShipping({
        price: "R$ 19,90",
        estimated: "5-8 dias úteis",
      });
      setLoading(false);
    }, 1000);
  };

  return (
    <div className="shipping-container">
      {!showForm && (
        <button
          className="show-form-button"
          onClick={() => setShowForm(true)}
        >
          Calcular Frete
        </button>
      )}

      {showForm && (
        <>
          <div className="shipping-form">
            <input
              type="text"
              placeholder="Digite seu CEP"
              value={cep}
              onChange={(e) => setCep(e.target.value)}
            />
            <button onClick={handleCalculate}>
              {loading ? "Calculando..." : "Calcular"}
            </button>
          </div>
          {error && <p className="shipping-error">{error}</p>}
          {shipping && (
            <div className="shipping-result">
              <p><strong>Valor:</strong> {shipping.price}</p>
              <p><strong>Prazo:</strong> {shipping.estimated}</p>
            </div>
          )}
        </>
      )}
    </div>
  );
}

export default ShippingCalculator;
