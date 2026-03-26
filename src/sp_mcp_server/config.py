import os
from dataclasses import dataclass
from typing import Optional

@dataclass
class ServerConfig:
    server_address: Optional[str]
    server_port: str
    admin_id: Optional[str]
    admin_password: Optional[str]
    dsmserv_path: Optional[str] = None
    server_instance_dir: Optional[str] = None
    servermon_path: Optional[str] = None
    servermon_xml_dir: Optional[str] = None
    instance_user: Optional[str] = None

    def validate(self) -> bool:
        return all([
            self.admin_id,
            self.admin_password
        ])

def load_config() -> ServerConfig:
    """Load configuration from environment variables."""
    # Check for both standard and TSM-style env vars
    address = os.environ.get("TCPSERVERADDRESS")
    port = os.environ.get("SP_SERVER_PORT") or os.environ.get("TCPPORT") or "1500"
    admin = os.environ.get("SP_ADMIN_ID")
    password = os.environ.get("SP_ADMIN_PASSWORD")
    dsmserv = os.environ.get("SP_DSMSERV_PATH")
    instance_dir = os.environ.get("SP_SERVER_INSTANCE_DIR")
    servermon = os.environ.get("SP_SERVERMON_PATH")
    servermon_xml = os.environ.get("SP_SERVERMON_XML_DIR")
    instance_user = os.environ.get("SP_INSTANCE_USER")

    return ServerConfig(
        server_address=address,
        server_port=port,
        admin_id=admin,
        admin_password=password,
        dsmserv_path=dsmserv,
        server_instance_dir=instance_dir,
        servermon_path=servermon,
        servermon_xml_dir=servermon_xml,
        instance_user=instance_user
    )
