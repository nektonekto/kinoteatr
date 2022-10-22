select count(id_bilet) as Количество
from bilet_in_orders
where id_session = '$num_session'