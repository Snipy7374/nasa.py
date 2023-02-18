.. currentmodule:: nasa

Clients
-------

.. toctree::
    :hidden:

    sync_client
    async_client

Introduction to clients
=======================

The nasa.py library provides two different clients:
    - :class:`NasaSyncClient`
    - :class:`NasaAsyncClient`

:class:`NasaSyncClient`, as the name suggests, is a synchronous client. This means that every request made to the NASA Api will block the thread where your python program is running, for most general usecases this is fine.

Instead :class:`NasaAsyncClient` is an asynchronous client. Every request made to tha NASA Api won't block the python execution thread and you'll be able to concurrently run coroutines/tasks.

.. seealso::
    | :py:mod:`Asyncio <asyncio>` - write concurrent code using the async/await syntax.
    | `Asyncio Walkthrough <https://realpython.com/async-io-python/>`_ - a basic guide to use and understand asyncio.

If you're in an asynchronous context (e.g a discord bot) you should use :class:`NasaAsyncClient` to not block your application and to execute concurrently coroutines/task, etc... Viceversa if you're not in an asynchronous context it's recommended to use :class:`NasaSyncClient`.


Examples
========
.. note::
    Typehints in the examples don't influence runtime performances
    or results, they're there to tell to the static type checker
    what's the type of something. You can omit them in your code.


.. _NasaSyncClient-example-reference:

NasaSyncClient
~~~~~~~~~~~~~~

.. tab:: Normal NasaSyncClient instantiation

    .. code-block:: python3

        from typing import TYPE_CHECKING
        from nasa import NasaSyncClient

        if TYPE_CHECKING:
            from nasa import AstronomyPicuture

        client = NasaSyncClient(token="TOKEN")
        apod: AstronomyPicuture = client.get_astronomy_picture()
        print(apod.title, apod.explanation)

.. tab:: Using NasaSyncClient with a context manager

    .. code-block:: python3

        from typing import TYPE_CHECKING
        from nasa import NasaSyncClient

        if TYPE_CHECKING:
            from nasa import AstronomyPicuture
        
        with NasaSyncClient(token="TOKEN") as client:
            apod: AstronomyPicuture = client.get_astronomy_picture()
        print(apod.title, apod.explanation)


.. _NasaAsyncClient-example-reference:

NasaAsyncClient
~~~~~~~~~~~~~~~

.. tab:: Normal NasaAsyncClient instantiation

    .. code-block:: python3

        from typing import TYPE_CHECKING
        from nasa import NasaAsyncClient

        if TYPE_CHECKING:
            from nasa import AstronomyPicuture
        
        client = NasaAsyncClient(token="TOKEN")

        async def main():
            apod: AstronomyPicuture = await client.get_astronomy_picture()
            print(apod.title, apod.explanation)

.. tab:: Using NasaAsyncClient with a context manager

    .. code-block:: python3

        from typing import TYPE_CHECKING
        from nasa import NasaAsyncClient

        if TYPE_CHECKING:
            from nasa import AstronomyPicuture
        
        async def main():
            async with NasaAsyncClient(token="TOKEN") as client:
                apod: AstronomyPicuture = await client.get_astronomy_picture()
            print(apod.title, apod.explanation)

