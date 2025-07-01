import React, { createContext, useContext, useState, useEffect } from "react";
import { obterCarrinho } from "../api/cartApi";
import { isAuthenticated } from "../utils/auth";

const CarrinhoContext = createContext();

export const CarrinhoProvider = ({ children }) => {
    const [quantidadeCarrinho, setQuantidadeCarrinho] = useState(0);

    const atualizarCarrinho = async () => {
        try {
            const data = await obterCarrinho();
            const total = data.itens?.reduce((acc, item) => acc + item.quantidade, 0);
            setQuantidadeCarrinho(total || 0);
        } catch (err) {
            console.error("Erro ao atualizar carrinho:", err);
        }
    };

    useEffect(() => {
        atualizarCarrinho();
    }, [isAuthenticated()]);

    return (
        <CarrinhoContext.Provider value={{ quantidadeCarrinho, atualizarCarrinho }}>
            {children}
        </CarrinhoContext.Provider>
    );
};

export const useCarrinho = () => useContext(CarrinhoContext);