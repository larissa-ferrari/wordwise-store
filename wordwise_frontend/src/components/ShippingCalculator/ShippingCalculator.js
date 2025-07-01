import React, { useState } from "react";
import "./ShippingCalculator.css";

function ShippingCalculator() {
  const [showForm, setShowForm] = useState(false);
  const [cep, setCep] = useState("");
  const [shipping, setShipping] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [address, setAddress] = useState(null);

  const handleCalculate = async () => {
    setLoading(true);
    setShipping(null);
    setError("");
    setAddress(null);

    if (!cep || cep.length < 8) {
      setError("Por favor, insira um CEP válido.");
      setLoading(false);
      return;
    }

    try {
      const response = await fetch(`https://viacep.com.br/ws/${cep}/json/`);
      const data = await response.json();

      if (data.erro) {
        setError("CEP não encontrado.");
        setLoading(false);
        return;
      }

      setAddress({
        logradouro: data.logradouro,
        bairro: data.bairro,
        localidade: data.localidade,
        uf: data.uf,
      });

      setShipping({
        price: "R$ 19,90",
        estimated: "5-8 dias úteis",
      });
    } catch (err) {
      setError("Erro ao buscar o CEP. Tente novamente.");
    }

    setLoading(false);
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
            <button onClick={handleCalculate} disabled={loading}>
              {loading ? "Calculando..." : "Calcular"}
            </button>
          </div>

          {error && <p className="shipping-error">{error}</p>}

          {shipping && (
            <div className="shipping-result">
              <p><strong>Valor:</strong> {shipping.price}</p>
              <p><strong>Prazo:</strong> {shipping.estimated}</p>

              {address && (
                <>
                  <hr />
                  <p>
                    <strong>Endereço:</strong>{" "}
                    {`${address.logradouro}, ${address.bairro}, ${address.localidade} - ${address.uf}`}
                  </p>
                </>
              )}
            </div>
          )}
        </>
      )}
    </div>
  );
}

export default ShippingCalculator;
