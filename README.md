1. Primeros debemos de crear un contenedor de rabbitmq
	`docker run -d --hostname my--rabbit --name some-rabbit -p 15672:15672 -p 5672:5672 rabbitmq:3-management`
	Una vez creado para entrar nos dirimos a la ip que nos proporciona docker 
	IP-DOCKER:15672 podemos usar un usuario por defaul guest cuyo contraseña tambien es guest
2. habilitar por comando nameko 
	`nameko run src.amp_service --broker amp:\\guest:guest@IP-DOCKER`
3. Consumimos en endoint de points que es el que tiene la tarea para que nos de una respuesta provisional en lo que se termina de insertar el recorrido en la BD
