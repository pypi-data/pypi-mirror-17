from hashlib import sha1
from rask.base import Base
from rask.parser.utcode import UTCode
from rask.rmq import ack,BasicProperties
from uuid import uuid4

__all__ = ['MP']

class MP(Base):
    options = {
        'code':{
            'checkout_add_item':{
                'ok':'430f27c966064cfc871930514775b8cc'
            },
            'checkout_get':{
                'ok':'4c4cd268521c4ca48b7e66769b79de89'
            },
            'checkout_remove_item':{
                'ok':'9fc18880436d41e38afdbf2e05b081c4'
            },
            'checkout_update_item':{
                'ok':'642862d4715047f0b3545b4926d05f83'
            },
            'customer_create':{
                'address_invalid':'d88251a8f60548ad8f771a79b7430e0d',
                'customer_exists':'1fd743a09d3343b68ea2c70be2bb6db1',
                'customer_invalid':'4aeb4808e53b49629ad203eac499fe46',
                'mercadopago_error':'71f6709cd9f240b8ae114cf1b4beba2d',
                'ok':'4063c693a8b540759439e03fbf415a52'
            },
            'customer_get':{
                'kuid_invalid':'fad0a77804854fe19bf01dcb8fda1165',
                'mercadopago_error':'a3de94f15a414e578f04952274fa322a',
                'ok':'127185366fd5497bb54ca7b1e8b5ce98'
            },
            'customer_kuid':{
                'not_found':'0dd44f2179cb4e3f8604950b0388ec20',
                'ok':'144cabe531a142558e2e8638f08b845d',
                'password_invalid':'fdbef8d44f0a4e869eff9cdc318f5a62'
            },
            'payment_create':{
                'ok':'8602177cab9b42dd80b154e71cae5038'
            }
        },
        'rmq':{
            'exchange':{
                'headers':'mercadopago_headers',
                'topic':'mercadopago'
            },
            'rk':{
                'customer_create':'mercadopago.customer.create',
                'customer_get':'mercadopago.customer.get',
                'customer_kuid':'mercadopago.customer.kuid'
            }
        }
    }

    def __init__(self,rmq):
        self.options['rmq']['queue'] = self.etag
        self.rmq = rmq
        self.utcode = UTCode()
        self.ioengine.loop.add_callback(self.__services__)

    @property
    def __channel__(self):
        try:
            assert self.__channel
        except (AssertionError,AttributeError):
            self.__channel = {}
        except:
            raise
        return self.__channel

    @property
    def __request__(self):
        try:
            assert self.__request
        except (AssertionError,AttributeError):
            self.__request = {}
        except:
            raise
        return self.__request

    @property
    def active(self):
        try:
            assert self.__active
        except (AssertionError,AttributeError):
            self.__active = False
        except:
            raise
        return self.__active

    @active.setter
    def active(self,_):
        try:
            assert _
            assert 'consumer' in self.__channel__
            assert 'pusher' in self.__channel__
        except AssertionError:
            self.__active = False
        except:
            raise
        else:
            self.__active = True
            self.ioengine.loop.add_callback(self.__promise_consume__)

    @property
    def etag(self):
        return sha1('mp:%s:%s' % (self.uuid,uuid4().hex)).hexdigest()

    def __queue_declare__(self):
        def on_declare(*args):
            self.__channel__['consumer'].basic_consume(
                consumer_callback=self.on_msg,
                queue=self.options['rmq']['queue']
            )
            self.active = True
            return True
        
        self.__channel__['consumer'].queue_declare(
            callback=on_declare,
            queue=self.options['rmq']['queue'],
            durable=False,
            exclusive=True
        )
        return True

    def __push__(self,payload,rk,future):
        etag = self.etag
        def on_encode(_):
            self.__channel__['pusher'].basic_publish(
                body=_.result(),
                exchange=self.options['rmq']['exchange']['topic'],
                properties=BasicProperties(headers={'etag':etag}),
                routing_key=rk
            )
            return True
        
        def on_response(_):
            future.set_result(_.result())
            self.__channel__['consumer'].queue_unbind(
                callback=None,
                queue=self.options['rmq']['queue'],
                exchange=self.options['rmq']['exchange']['headers'],
                arguments={
                    'etag':etag,
                    'mercadopago-response':True,
                    'x-match':'all'
                }
            )
            return True

        self.__request__[etag] = self.ioengine.future(on_response)
        self.__channel__['consumer'].queue_bind(
            callback=None,
            queue=self.options['rmq']['queue'],
            exchange=self.options['rmq']['exchange']['headers'],
            arguments={
                'etag':etag,
                'mercadopago-response':True,
                'x-match':'all'
            }
        )
        self.utcode.encode(payload,future=self.ioengine.future(on_encode))
        return True

    def __services__(self):
        def on_consumer(_):
            self.log.info('channel consumer')
            self.__channel__['consumer'] = _.result().channel
            self.ioengine.loop.add_callback(self.__queue_declare__)
            return True
        
        def on_pusher(_):
            self.log.info('channel pusher')
            self.__channel__['pusher'] = _.result().channel
            return True
        
        self.rmq.channel('mp_consumer_%s' % self.uuid,self.ioengine.future(on_consumer))
        self.rmq.channel('mp_pusher_%s' % self.uuid,self.ioengine.future(on_pusher))
        return True

    def customer_create(self,payload,future):
        try:
            assert self.active
        except AssertionError:
            def on_active(_):
                self.ioengine.loop.add_callback(
                    self.customer_create,
                    payload=payload,
                    future=future
                )
                return True

            self.promises.append(self.ioengine.future(on_active))
        except:
            raise
        else:
            def on_response(_):
                try:
                    assert _.result()['header']['code'] in self.options['code']['customer_create'].values()
                except AssertionError:
                    future.set_result(False)
                except:
                    raise
                else:
                    future.set_result(_.result())
                return True

            self.ioengine.loop.add_callback(
                self.__push__,
                payload=payload,
                rk=self.options['rmq']['rk']['customer_create'],
                future=self.ioengine.future(on_response)
            )
            self.log.info('creating customer')
        return True
    
    def customer_get(self,kuid,future):
        try:
            assert self.active
        except AssertionError:
            def on_active(_):
                self.ioengine.loop.add_callback(
                    self.customer_get,
                    kuid=kuid,
                    future=future
                )
                return True

            self.promises.append(self.ioengine.future(on_active))
        except:
            raise
        else:
            def on_response(_):
                try:
                    assert _.result()['header']['code'] in self.options['code']['customer_get'].values()
                except AssertionError:
                    future.set_result(False)
                except:
                    raise
                else:
                    future.set_result(_.result())
                return True

            self.ioengine.loop.add_callback(
                self.__push__,
                payload={'kuid':kuid},
                rk=self.options['rmq']['rk']['customer_get'],
                future=self.ioengine.future(on_response)
            )
            self.log.info('fetching customer')
        return True

    def customer_kuid(self,cred,future):
        try:
            assert self.active
        except AssertionError:
            def on_active(_):
                self.ioengine.loop.add_callback(
                    self.customer_kuid,
                    cred=cred,
                    future=future
                )
                return True
            
            self.promises.append(self.ioengine.future(on_active))
        except:
            raise
        else:
            def on_response(_):
                try:
                    assert _.result()['header']['code'] in self.options['code']['customer_kuid'].values()
                except AssertionError:
                    future.set_result(False)
                except:
                    raise
                else:
                    future.set_result(_.result())
                return True

            self.ioengine.loop.add_callback(
                self.__push__,
                payload=cred,
                rk=self.options['rmq']['rk']['customer_kuid'],
                future=self.ioengine.future(on_response)
            )
            self.log.info('authenticating customer')
        return True

    def on_msg(self,channel,method,properties,body):
        try:
            assert properties.headers['etag'] in self.__request__
        except AssertionError:
            channel.basic_publish(
                body=body,
                exchange=self.options['rmq']['exchange']['topic'],
                routing_key='',
                properties=properties
            )
        except KeyError:
            pass
        except:
            raise
        else:
            def on_decode(_):
                self.__request__[properties.headers['etag']].set_result({'header':properties.headers,'body':_.result()})
                del self.__request__[properties.headers['etag']]
                return True

            self.utcode.decode(body,future=self.ioengine.future(on_decode))

        ack(channel,method)(True)
        return True
