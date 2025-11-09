DELETE  from medical.ag_edge where "end" not in (select id from medical.ag_vertex);
DELETE  from medical.ag_edge where "start" not in (select id from medical.ag_vertex);