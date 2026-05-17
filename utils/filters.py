def filter_year_month(sql, categories, current_year, first_month, last_month):
    filters = []
    params = []

    if categories:
        params.extend(categories)
        placeholders = ",".join("?" for _ in categories)
        filters.append(f"p.category_id IN ({placeholders})")

    def safe_int_str(val):
        try:
            if val is not None and str(val).strip().isdigit():
                return f"{int(val):02d}"
        except (ValueError, TypeError):
            pass
        return None

    f_month_str = safe_int_str(first_month)
    l_month_str = safe_int_str(last_month)

    if current_year:
        if f_month_str and l_month_str:
            params.append(f"{current_year}-{f_month_str}-01")
            params.append(f"{current_year}-{l_month_str}-31")
            filters.append("s.date BETWEEN ? AND ?")
        elif f_month_str:
            params.append(f"{current_year}-{f_month_str}%")
            filters.append("s.date LIKE ?")
        else:
            params.append(f"{current_year}%")
            filters.append("s.date LIKE ?")

    if filters:
        if "WHERE" in sql.upper():
            sql += " AND " + " AND ".join(filters)
        else:
            sql += " WHERE " + " AND ".join(filters)

    return params, sql