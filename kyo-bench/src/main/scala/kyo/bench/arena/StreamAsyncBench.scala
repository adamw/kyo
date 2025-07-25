package kyo.bench.arena

class StreamAsyncBench extends ArenaBench.ForkOnly(()):
    val seq = (0 until 10000).toVector

    def catsBench() =
        import cats.effect.*
        import fs2.*
        Stream.emits(seq)
            .parEvalMap(6)(v => IO(v + 1))
            .compile
            .drain
    end catsBench

    override def kyoBenchFiber() =
        import kyo.*
        Stream.init(seq)
            .mapPar(6)(v => Sync.defer(v + 1))
            .discard
    end kyoBenchFiber

    def zioBench() =
        import zio.*
        import zio.stream.*
        ZStream.fromIterable(seq)
            .mapZIOPar(6)(v => ZIO.succeed(v + 1))
            .runDrain
            .unit
    end zioBench

    override def oxBench() =
        import ox.flow.*

        Flow.fromIterable(seq)
            .mapPar(6)(v => v + 1)
            .runDrain()
    end oxBench

    import org.apache.pekko.actor.ActorSystem
    given system: ActorSystem = ActorSystem("StreamAsyncBench")
    override def pekkoBench() =
        import org.apache.pekko.stream.scaladsl.Source
        import scala.concurrent.Future
        import system.dispatcher

        Source(seq)
            .mapAsync(6)(v => Future(v + 1))
            .run()
            .map(_ => ())
    end pekkoBench

end StreamAsyncBench
