from pydantic import BaseSettings, BaseModel, Field
from typing import Set, List


class BaseEntity(BaseModel):
    # Workaround for serializing properties with pydantic until
    # https://github.com/samuelcolvin/pydantic/issues/935
    # is solved
    @classmethod
    def get_properties(cls):
        return [prop for prop in dir(cls) if isinstance(getattr(cls, prop), property)]

    def dict(self, *args, **kwargs):
        self.__dict__.update(
            {prop: getattr(self, prop) for prop in self.get_properties()}
        )
        return super().dict(*args, **kwargs)

    def json(
        self,
        *args,
        **kwargs,
    ) -> str:
        self.__dict__.update(
            {prop: getattr(self, prop) for prop in self.get_properties()}
        )

        return super().json(*args, **kwargs)


class Group(BaseEntity):
    id: str
    alias: str

    def __hash__(self):
        return self.id.__hash__()


class Session(BaseEntity):
    schema_id: str = ''
    active: bool = False
    hostname: str
    type: str = 'local'
    alias: str
    remote_address: str = '127.0.0.1'
    remote_port: int = 0
    local_address: str = '127.0.0.1'
    local_port: int = 0
    link: str = None
    auto_start: bool = True

    @property
    def tmux_id(self) -> str:
        fields = [
            'pfm_session',
            '{schema_id}',
            '{hostname}',
            '{remote_address}',
            '{remote_port}',
            '{local_address}',
            '{local_port}',
            '{type}'
        ]

        data = {
            'schema_id': self.schema_id,
            'hostname': self.hostname,
            'remote_address': self.remote_address,
            'remote_port': self.remote_port,
            'local_address': self.local_address,
            'local_port': self.local_port,
            'type': self.type
        }

        return '|'.join(fields).format(**data).replace('.', '_')

    @property
    def url(self):
        if self.link:
            data = {
                'schema_id': self.schema_id,
                'hostname': self.hostname,
                'remote_address': self.remote_address,
                'remote_port': self.remote_port,
                'local_address': self.local_address,
                'local_port': self.local_port,
                'type': self.type
            }

            return self.link.format(**data)
        else:
            return ''


class Schema(BaseEntity):
    id: str
    active: bool = False
    group: str
    alias: str
    hosts: Set[str] = []
    sessions: List[Session]

    def __hash__(self):
        return hash((type(self),) + (self.id, self.group))

    def get_session(self, hostname: str, remote_port: int):
        for session in self.sessions:
            # print(session.dict())
            # print(hostname, remote_port)
            if session.hostname == hostname and session.remote_port == remote_port:
                return session

        raise Exception(f"Session {hostname} and {remote_port} not found on {self.id}")


class Settings(BaseEntity):
    schemas: List[Schema]
    groups: List[Group]
    ports_active: List = []
    show_schema_link: bool = False
    show_table_border: bool = True
    wait_after_start: float = 0.5
    wait_after_stop: float = 0.5

        
