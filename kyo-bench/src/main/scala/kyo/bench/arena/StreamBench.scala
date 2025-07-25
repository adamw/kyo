package kyo.bench.arena

class StreamBench extends ArenaBench.SyncAndFork(25000000):

    val seq = (0 until 10000).toVector

    def catsBench() =
        import cats.effect.*
        import fs2.*
        Stream.emits(seq)
            .filter(_ % 2 == 0)
            .map(_ + 1)
            .covary[IO]
            .compile
            .fold(0)(_ + _)
    end catsBench

    def kyoBench() =
        import kyo.*
        Stream.init(seq)
            .filterPure(_ % 2 == 0)
            .mapPure(_ + 1)
            .foldPure(0)(_ + _)
    end kyoBench

    def zioBench() =
        import zio.*
        import zio.stream.*
        ZStream.fromIterable(seq)
            .filter(_ % 2 == 0)
            .map(_ + 1)
            .runSum
    end zioBench

    override def oxBench() =
        import ox.flow.*

        Flow.fromIterable(seq)
            .filter(_ % 2 == 0)
            .map(_ + 1)
            .runFold(0)(_ + _)
    end oxBench

    import org.apache.pekko.actor.ActorSystem
    given system: ActorSystem = ActorSystem("StreamBench")
    override def pekkoBench() =
        import org.apache.pekko.stream.scaladsl.Source

        Source.fromIterator(() => seq.iterator)
            .filter(_ % 2 == 0)
            .map(_ + 1)
            .runFold(0)(_ + _)
    end pekkoBench

end StreamBench
