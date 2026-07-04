import pytest

from channels.testing import WebsocketCommunicator

from chatproject.asgi import application


@pytest.mark.asyncio
@pytest.mark.django_db(transaction=True)
async def test_websocket_connect():
    communicator = WebsocketCommunicator(
        application,
        "/websocket/1",
    )

    connected, _ = await communicator.connect()

    assert connected

    await communicator.disconnect()