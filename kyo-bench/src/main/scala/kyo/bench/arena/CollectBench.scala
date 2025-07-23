package kyo.bench.arena

class CollectBench extends ArenaBench.SyncAndFork(Seq.fill(1000)(1)):

    val count = 1000

    val kyoTasks   = List.fill(count)(kyo.Sync.defer(1))
    val catsTasks  = List.fill(count)(cats.effect.IO(1))
    val zioTasks   = List.fill(count)(zio.ZIO.succeed(1))
    val oxTasks    = List.fill(count)(1)
    val pekkoTasks = List.fill(count)(scala.concurrent.Future.successful(1))

    def kyoBench() =
        import kyo.*

        Kyo.collectAll(kyoTasks)
    end kyoBench

    def catsBench() =
        import cats.effect.*
        import cats.implicits.*

        catsTasks.sequence
    end catsBench

    def zioBench() =
        import zio.*

        ZIO.collectAll(zioTasks)
    end zioBench

    override def oxBench() =
        import ox.*

        oxTasks
    end oxBench

    override def pekkoBench() =
        import scala.concurrent.ExecutionContext.Implicits.global
        import scala.concurrent.Future

        Future.sequence(pekkoTasks)
    end pekkoBench
end CollectBench
