def filter_year_month(sql, categories, current_year, first_month, last_month):
    filters = []
    params = []

    # 1. Filtro de Categorias
    if categories:
        params.extend(categories)
        placeholders = ",".join("?" for _ in categories)
        filters.append(f"p.category_id IN ({placeholders})")

    # Função auxiliar para validar e formatar os meses com zero à esquerda
    def safe_int_str(val):
        try:
            if val is not None and str(val).strip().isdigit():
                return f"{int(val):02d}"
        except (ValueError, TypeError):
            pass
        return None

    f_month_str = safe_int_str(first_month)
    l_month_str = safe_int_str(last_month)

    # 2. Filtro de Tempo (Ajustado cirurgicamente para o formato AAAA-MM do banco)
    if current_year:
        if f_month_str and f_month_str != "" and l_month_str and l_month_str != "":
            # Se tem os dois meses, faz o BETWEEN com texto exato (ex: '2022-03' AND '2022-04')
            params.append(f"{current_year}-{f_month_str}")
            params.append(f"{current_year}-{l_month_str}")
            filters.append("s.date BETWEEN ? AND ?")
        elif f_month_str and f_month_str != "":
            # "Apenas este mês": faz correspondência exata do texto (ex: '2022-03')
            params.append(f"{current_year}-{f_month_str}")
            filters.append("s.date = ?")
        else:
            # "Todos os meses": pega tudo que começa com o ano escolhido (ex: '2022%')
            params.append(f"{current_year}%")
            filters.append("s.date LIKE ?")

    # 3. Injeção Inteligente de Filtros (Evita quebrar queries com GROUP BY / ORDER BY)
    if filters:
        clausula_filtro = " AND ".join(filters)
        sql_upper = sql.upper()

        ponto_corte = len(sql)
        for palavra in ["GROUP BY", "ORDER BY"]:
            idx = sql_upper.rfind(palavra)
            if idx != -1 and idx < ponto_corte:
                ponto_corte = idx

        parte_principal = sql[:ponto_corte]
        parte_final = sql[ponto_corte:]

        if "WHERE" in parte_principal.upper():
            parte_principal += " AND " + clausula_filtro
        else:
            parte_principal += " WHERE " + clausula_filtro

        sql = parte_principal + " " + parte_final

    return params, sql