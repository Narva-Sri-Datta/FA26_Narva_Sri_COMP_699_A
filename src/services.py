from database import connect

def matching_providers(path, category, area=""):
    with connect(path) as db:
        rows=db.execute("""SELECT u.id,u.name,u.phone,p.business_name,p.service_area,p.bio,p.availability,
          GROUP_CONCAT(c.name, ', ') AS categories,
          ROUND(AVG(f.rating),1) AS rating
          FROM providers p JOIN users u ON u.id=p.user_id
          JOIN provider_categories pc ON pc.provider_id=p.user_id JOIN categories c ON c.id=pc.category_id
          LEFT JOIN service_requests sr ON sr.provider_id=u.id LEFT JOIN feedback f ON f.request_id=sr.id
          WHERE u.active=1 AND p.approved=1 AND p.availability='Available' AND c.name=?
          AND (?='' OR lower(p.service_area) LIKE '%' || lower(?) || '%')
          GROUP BY u.id ORDER BY rating DESC, p.business_name""",(category,area,area)).fetchall()
        return [dict(r) for r in rows]
