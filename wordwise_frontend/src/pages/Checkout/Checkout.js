import React, { useEffect, useState } from "react";
import { listarTransportes } from "../../api/transportApi"; // Você cria essa função para chamar a API de transporte
import { listarMetodosPagamento } from "../../api/paymentApi"; // Similar para pagamento
import { criarPedido } from "../../api/orderApi"; // Função para criar pedido
import "./Checkout.css";

function Checkout() {
    const [transportes, setTransportes] = useState([]);
    const [metodosPagamento, setMetodosPagamento] = useState([]);
    const [form, setForm] = useState({
        transporte_id: "",
        metodo_pagamento_id: "",
        endereco_entrega: "",
        observacoes: "",
    });
    const [error, setError] = useState(null);
    const [sucesso, setSucesso] = useState(false);

    useEffect(() => {
        async function fetchDados() {
            try {
                const transportesData = await listarTransportes();
                setTransportes(transportesData);

                const pagamentosData = await listarMetodosPagamento();
                setMetodosPagamento(pagamentosData);
            } catch (err) {
                setError("Erro ao carregar opções de transporte ou pagamento");
            }
        }
        fetchDados();
    }, []);

    function handleChange(e) {
        setForm({
            ...form,
            [e.target.name]: e.target.value,
        });
    }

    async function handleSubmit(e) {
        e.preventDefault();
        setError(null);

        try {
            await criarPedido(form);
            setSucesso(true);
        } catch (err) {
            setError(err?.message || "Erro ao finalizar pedido");
        }
    }

    if (sucesso) {
        return <p className="success-message">Pedido finalizado com sucesso!</p>;
    }

    return (
        <div className="checkout-container">
            <h2>Finalizar Pedido</h2>
            {error && <p className="error-message">{error}</p>}

            <form onSubmit={handleSubmit}>
                <div className="checkout-section">
                    <label htmlFor="transporte_id">Transporte</label>
                    <select
                        name="transporte_id"
                        value={form.transporte_id}
                        onChange={handleChange}
                        required
                    >
                        <option value="">Selecione o transporte</option>
                        {transportes.map((t) => (
                            <option key={t.id} value={t.id}>
                                {t.nome} - R$ {t.preco}
                            </option>
                        ))}
                    </select>
                </div>

                <div className="checkout-section">
                    <label htmlFor="metodo_pagamento_id">Método de Pagamento</label>
                    <select
                        name="metodo_pagamento_id"
                        value={form.metodo_pagamento_id}
                        onChange={handleChange}
                        required
                    >
                        <option value="">Selecione o método de pagamento</option>
                        {metodosPagamento.map((m) => (
                            <option key={m.id} value={m.id}>
                                {m.nome}
                            </option>
                        ))}
                    </select>
                </div>

                <div className="checkout-section">
                    <label htmlFor="endereco_entrega">Endereço de Entrega</label>
                    <textarea
                        name="endereco_entrega"
                        value={form.endereco_entrega}
                        onChange={handleChange}
                        placeholder="Digite seu endereço completo"
                        required
                    />
                </div>

                <div className="checkout-section">
                    <label htmlFor="observacoes">Observações</label>
                    <textarea
                        name="observacoes"
                        value={form.observacoes}
                        onChange={handleChange}
                        placeholder="Alguma observação extra?"
                    />
                </div>

                <div className="checkout-actions">
                    <button type="submit">Finalizar Pedido</button>
                </div>
            </form>
        </div>
    );
}

export default Checkout;
