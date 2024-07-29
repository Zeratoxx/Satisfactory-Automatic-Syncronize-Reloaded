.RECIPEPREFIX = >

serve:
> @echo "Starting Penpot containers using docker compose..."
> @docker compose -p penpot -f docker-compose-local-penpot.yaml up -d
> @echo " "
> @echo "Server URL:"
> @echo " "
> @echo "        http://localhost:9001"
> @echo " "

stop:
> @echo "Stopping Penpot containers..."
> @docker compose -p penpot -f docker-compose-local-penpot.yaml down
