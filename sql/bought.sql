select id , session as "номер сессии", cost as "стоимость", place as "место"
from bilet
where avail = 0