def filter_year_month(sql, current_year, first_month, last_month):

    filters = []
    params = []

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
        sql += "WHERE " + "".join(filters)
    
    return params, sql

    