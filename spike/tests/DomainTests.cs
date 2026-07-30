// SPIKE — CÓDIGO DE INVESTIGACIÓN TÉCNICA (EXENCIÓN-SPIKE-01). No es código de producción.
// Unit tests del dominio puro: máquina de estados OT (Doc 14) y HLC (SY-6).
using SpikeBackend.Domain;
using Xunit;

namespace SpikeBackend.Tests;

public class StateMachineTests
{
    [Theory]
    [InlineData(WoState.Asignada, WoState.EnProgreso, true)]
    [InlineData(WoState.Asignada, WoState.Completada, false)]  // saltarse estados: prohibido
    [InlineData(WoState.EnProgreso, WoState.Completada, true)]
    [InlineData(WoState.Completada, WoState.Verificada, true)]
    [InlineData(WoState.Verificada, WoState.Cerrada, true)]
    [InlineData(WoState.Cerrada, WoState.EnProgreso, false)]   // terminal
    [InlineData(WoState.Cancelada, WoState.Asignada, false)]   // terminal
    [InlineData(WoState.Asignada, WoState.Cancelada, true)]
    public void Transitions_follow_canonical_matrix(WoState from, WoState to, bool expected) =>
        Assert.Equal(expected, WorkOrderStateMachine.CanTransition(from, to));

    [Fact]
    public void Server_is_authoritative_on_conflict()
    {
        // Cliente intentó completar, pero el servidor canceló → REJECT (nunca LWW silencioso)
        Assert.Equal(Verdict.Reject,
            WorkOrderStateMachine.RevalidateTransition(WoState.Cancelada, WoState.Completada));
    }

    [Fact]
    public void Same_transition_is_idempotent_duplicate()
    {
        Assert.Equal(Verdict.AcceptDuplicate,
            WorkOrderStateMachine.RevalidateTransition(WoState.Completada, WoState.Completada));
    }

    [Fact]
    public void Valid_transition_from_current_state_accepts()
    {
        Assert.Equal(Verdict.Accept,
            WorkOrderStateMachine.RevalidateTransition(WoState.EnProgreso, WoState.Completada));
    }
}

public class HlcTests
{
    [Fact]
    public void Tick_advances_with_physical_clock()
    {
        var h = new Hlc(100, 0).Tick(200);
        Assert.Equal(new Hlc(200, 0), h);
    }

    [Fact]
    public void Tick_increments_logical_when_clock_stalls_or_goes_backwards()
    {
        // Reloj del dispositivo atrasado (caso normativo del Doc 27)
        var h = new Hlc(100, 0).Tick(50);
        Assert.Equal(new Hlc(100, 1), h);
    }

    [Fact]
    public void Merge_preserves_causality()
    {
        var a = new Hlc(100, 5);
        var b = new Hlc(100, 3);
        var m = a.Merge(b, 100);
        Assert.True(Hlc.Compare(m, a) > 0);
        Assert.True(Hlc.Compare(m, b) > 0);
    }

    [Fact]
    public void Compare_orders_causally()
    {
        Assert.True(Hlc.Compare(new Hlc(1, 0), new Hlc(1, 1)) < 0);
        Assert.True(Hlc.Compare(new Hlc(2, 0), new Hlc(1, 99)) > 0);
    }
}
