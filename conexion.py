import pymysql
#import script_consulta_horarios
try:
	conexion = pymysql.connect(host='192.168.1.175',
                             user='authen',
                             password='D3s@rr0ll02022',
                             db='pruebaChecador')
	print("Conexión exitosa a la base de datos.")
	try:
		with conexion.cursor() as cursor:
	#		
			consulta = "SELECT * FROM checador"
			cursor.execute(consulta)
			resultados = cursor.fetchall()
			for fila in resultados:
				print(fila)

	#		cursor.execute(script_consulta_horarios.consulta)
 
			# Con fetchall traemos todas las filas
	#		prueba = cursor.fetchall()
 
			# Recorrer e imprimir
	#		for nombres in prueba:
	#			print(nombres)
	finally:
		conexion.close()
	
except (pymysql.err.OperationalError, pymysql.err.InternalError) as e:
	print("Ocurrió un error al conectar: ", e)