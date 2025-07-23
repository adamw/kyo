package kyo.bench.arena

class DeepBindBench extends ArenaBench.SyncAndFork(()):

    val depth = 10000

    def kyoBench() =
        import kyo.*

        def loop(i: Int): Unit < Sync =
            Kyo.unit.flatMap { _ =>
                if i > depth then
                    ()
                else
                    loop(i + 1)
            }
        loop(0)
    end kyoBench

    def catsBench() =
        import cats.effect.*
        def loop(i: Int): IO[Unit] =
            IO.unit.flatMap { _ =>
                if i > depth then
                    IO.unit
                else
                    loop(i + 1)
            }
        loop(0)
    end catsBench

    def zioBench() =
        import zio.*
        def loop(i: Int): UIO[Unit] =
            ZIO.unit.flatMap { _ =>
                if i > depth then
                    ZIO.unit
                else
                    loop(i + 1)
            }
        loop(0)
    end zioBench

    override def oxBench() =
        def loop(i: Int): Unit = if i > depth then () else loop(i + 1)
        loop(0)
    end oxBench

    override def pekkoBench() =
        import scala.concurrent.ExecutionContext.Implicits.global
        import scala.concurrent.Future

        def loop(i: Int): Future[Unit] =
            Future.unit.flatMap { _ =>
                if i > depth then Future.unit else loop(i + 1)
            }
        loop(0)
    end pekkoBench
end DeepBindBench
