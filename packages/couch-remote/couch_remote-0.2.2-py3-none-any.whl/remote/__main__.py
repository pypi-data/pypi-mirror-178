import uvicorn

from remote import config


def main():
    uvicorn.run('remote:app', host=config.host, port=config.port, log_level='info', reload=True)
