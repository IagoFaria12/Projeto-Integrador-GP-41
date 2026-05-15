def filter_year_month(sql, categories, current_year, first_month, last_month):

    filters = []
    params = []

    if categories:
        params.extend(categories)
        placeholders = ",".join("?" for _ in categories)
        filters.append(f"p.category_id IN ({placeholders})")

    if current_year and first_month and last_month:
        params.append(f"{current_year}-{first_month}")
        params.append(f"{current_year}-{last_month}")
        filters.append("s.date BETWEEN ? AND ?")
        
    if current_year and first_month and not last_month:
        params.append(f"{current_year}-{first_month}")
        filters.append("s.date = ?")
    
    if current_year and not first_month and not last_month:
        params.append(f"{current_year}%")   
        filters.append("s.date LIKE ?")

    if filters:
        sql += "WHERE " + " AND ".join(filters)
    
    return params, sql