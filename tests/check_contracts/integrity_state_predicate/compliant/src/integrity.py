QUERY = "SELECT p.id FROM parents p LEFT JOIN child_records c ON c.parent_id = p.id AND c.completed_at IS NOT NULL WHERE c.parent_id IS NULL"
