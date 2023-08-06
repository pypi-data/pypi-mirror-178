import enum
import logging
import secrets
import time

import docker


class Flavors(enum.Enum):
    POSTGRES = "postgres"


class PostgreContainer:
    """Postgres flavored container"""

    def __init__(
        self,
        image="postgres",
        tag="latest",
        port=5432,
        password=None,
        wait_for_ready=True,
    ):
        self.container = None

        self.db_image = image + ":" + tag
        self.db_port = port
        self.db_password = password or self._gen_password()

        self._init_db_container()
        if wait_for_ready:
            self._wait_for_db_ready()

    @property
    def connection_string(self):
        connection_string = f"postgresql://postgres:{self.db_password}@localhost:{self.db_port}/postgres?sslmode=disable"
        return connection_string

    def _wait_for_db_ready(self):
        ready_string = "database system is ready to accept connections"
        logging.debug("Waiting for the DB to be initialize...")
        for log in self.container.logs(stream=True):
            if ready_string in log.decode("ascii"):
                logging.debug("DB is ready with note: '%s'", ready_string)
                time.sleep(0.25)  # TODO: Invesitgate ready failure without this
                return

    def _gen_password(self):
        return secrets.token_urlsafe(8)

    def _init_db_container(self):
        container_name_hash = secrets.token_urlsafe(4).lower()
        container_name = f"dev-postgres-{container_name_hash}"
        logging.debug("Initializing DB container with name: '%s'", container_name)

        client = docker.from_env()
        self.container = client.containers.run(
            self.db_image,
            name=container_name,
            environment=[f"POSTGRES_PASSWORD={self.db_password}"],
            ports={"5432/tcp": self.db_port},
            detach=True,
        )
        logging.debug("Initializing DB container: %s", self.container)
