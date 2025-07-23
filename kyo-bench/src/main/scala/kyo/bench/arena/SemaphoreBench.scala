package kyo.bench.arena

class SemaphoreBench extends ArenaBench.ForkOnly(()):

    val depth = 10000

    def catsBench() =
        import cats.effect.*
        import cats.effect.std.*

        def loop(s: Semaphore[IO], i: Int): IO[Unit] =
            if i >= depth then
                IO.unit
            else
                s.acquire.flatMap(_ => s.release).flatMap(_ => loop(s, i + 1))

        Semaphore[IO](1).flatMap(loop(_, 0))
    end catsBench

    override def kyoBenchFiber() =
        import kyo.*

        def loop(s: Meter, i: Int): Unit < (Async & Abort[Closed]) =
            if i >= depth then
                Kyo.unit
            else
                s.run(()).flatMap(_ => loop(s, i + 1))

        Meter.initSemaphoreUnscoped(1).flatMap(loop(_, 0))
    end kyoBenchFiber

    def zioBench() =
        import zio.*

        def loop(s: Semaphore, i: Int): ZIO[Any, Nothing, Unit] =
            if i >= depth then
                ZIO.unit
            else
                s.withPermit(ZIO.succeed(())).flatMap(_ => loop(s, i + 1))

        Semaphore.make(1).flatMap(loop(_, 0))
    end zioBench

    override def oxBench() =
        import ox.*
        import java.util.concurrent.Semaphore

        def loop(s: Semaphore, i: Int): Unit =
            if i >= depth then ()
            else
                s.acquire()
                s.release()
                loop(s, i + 1)

        loop(new Semaphore(1), 0)
    end oxBench

    override def pekkoBench() =
        import scala.concurrent.ExecutionContext.Implicits.global
        import scala.concurrent.{blocking, Future}
        import java.util.concurrent.Semaphore

        def loop(s: Semaphore, i: Int): Future[Unit] =
            if i >= depth then
                Future.unit
            else
                Future(blocking(s.acquire())).flatMap(_ => Future(blocking(s.release()))).flatMap(_ => loop(s, i + 1))

        loop(new Semaphore(1), 0)
    end pekkoBench

end SemaphoreBench
