class dao:
	def __init__(self):
		query = ""

	def get_consulta_parqueo_total(self, year, month, documento):
		query = """
			SELECT fe.fecha, COUNT(fe.fecha) FROM
			(
				SELECT en.fecha as fecha
				FROM carro as car inner join 
				(
					SELECT consecutivo, id_carro, DATE_FORMAT(fecha_entrada, '%Y %M %D') as fecha
					FROM entrada
					WHERE
					YEAR(fecha_entrada) = {0} AND MONTH(fecha_entrada) = {1}
				) en
				ON(en.id_carro = car.id_carro) 
				WHERE en.id_carro IS NOT NULL and car.us_documento = {2}
				GROUP BY en.fecha
				UNION ALL
				SELECT en.fecha as fecha
				FROM moto as mo inner join 
				(
					SELECT consecutivo, id_moto, DATE_FORMAT(fecha_entrada, '%Y %M %D') as fecha
					FROM entrada
					WHERE
					YEAR(fecha_entrada) = {0} AND MONTH(fecha_entrada) = {1}
				) en
				ON(en.id_moto = mo.id_moto) 
				WHERE en.id_moto IS NOT NULL and mo.us_documento = {2}
				GROUP BY en.fecha
				UNION ALL
				SELECT en.fecha as fecha
				FROM bicicleta as bic inner join 
				(
					SELECT consecutivo, id_bicicleta, DATE_FORMAT(fecha_entrada, '%Y %M %D') as fecha
					FROM entrada
					WHERE
					YEAR(fecha_entrada) = {0} AND MONTH(fecha_entrada) = {1}
				) en
				ON(en.id_bicicleta = bic.id_bicicleta) 
				WHERE en.id_bicicleta IS NOT NULL and bic.us_documento = {2}
				GROUP BY en.fecha
			) as fe
			GROUP BY fe.fecha
			""".format(year, month, documento)
		return query

	def get_consulta_parqueo_carro(self, year, month, documento):
		query = """
			SELECT en.fecha, COUNT(en.fecha)
			FROM carro as car inner join 
			(
				SELECT consecutivo, id_carro, DATE_FORMAT(fecha_entrada, '%Y %M %D') as fecha
				FROM entrada
				WHERE
				YEAR(fecha_entrada) = {} AND MONTH(fecha_entrada) = {}
			) en
			ON(en.id_carro = car.id_carro) 
			WHERE en.id_carro IS NOT NULL and car.us_documento = {}
			GROUP BY en.fecha
			""".format(year, month, documento)
		return query

	def get_consulta_parqueo_moto(self, year, month, documento):
		query = """
			SELECT en.fecha, COUNT(en.fecha)
			FROM moto as mo inner join 
			(
				SELECT consecutivo, id_moto, DATE_FORMAT(fecha_entrada, '%Y %M %D') as fecha
				FROM entrada
				WHERE
				YEAR(fecha_entrada) = {} AND MONTH(fecha_entrada) = {}
			) en
			ON(en.id_moto = mo.id_moto) 
			WHERE en.id_moto IS NOT NULL and mo.us_documento = {}
			GROUP BY en.fecha
			""".format(year, month, documento)
		return query

	def get_consulta_parqueo_bicicleta(self, year, month, documento):
		query = """
			SELECT en.fecha, COUNT(en.fecha)
			FROM bicicleta as bic inner join 
			(
				SELECT consecutivo, id_bicicleta, DATE_FORMAT(fecha_entrada, '%Y %M %D') as fecha
				FROM entrada
				WHERE
				YEAR(fecha_entrada) = {} AND MONTH(fecha_entrada) = {}
			) en
			ON(en.id_bicicleta = bic.id_bicicleta) 
			WHERE en.id_bicicleta IS NOT NULL and bic.us_documento = {}
			GROUP BY en.fecha
			""".format(year, month, documento)
		return query