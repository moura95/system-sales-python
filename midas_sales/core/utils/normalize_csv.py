def normalize_product_to_schema(product):
    return {
        "name": product.get("nome"),
        "code": product.get("codigo"),
        "bar_code": product.get("codigo_de_barra"),
        "price": product.get("preco"),
        "valor": product.get("valor"),
        "cost_value": product.get("valor_de_custo"),
        "unit": product.get("unidade"),
        "current_stock": product.get("estoque_inicial"),
    }

