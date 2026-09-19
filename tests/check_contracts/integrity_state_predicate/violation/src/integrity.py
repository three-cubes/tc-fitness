QUERY = "SELECT p.id FROM parents p LEFT JOIN child_records c ON c.parent_id = p.id WHERE c.parent_id IS NULL"
