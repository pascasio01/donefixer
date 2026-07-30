// SPIKE — CÓDIGO DE INVESTIGACIÓN TÉCNICA (EXENCIÓN-SPIKE-01). No es código de producción.
// Dominio puro: máquina de estados de OT conforme a Doc 14 (sin infraestructura).
namespace SpikeBackend.Domain;

public enum WoState { Asignada, EnProgreso, Completada, Verificada, Cerrada, Cancelada }

public static class WorkOrderStateMachine
{
    // Matriz de transiciones canónica (subset J-2 de la máquina del Doc 14)
    private static readonly Dictionary<WoState, WoState[]> Allowed = new()
    {
        [WoState.Asignada]   = new[] { WoState.EnProgreso, WoState.Cancelada },
        [WoState.EnProgreso] = new[] { WoState.Completada, WoState.Cancelada },
        [WoState.Completada] = new[] { WoState.Verificada },
        [WoState.Verificada] = new[] { WoState.Cerrada },
        [WoState.Cerrada]    = Array.Empty<WoState>(),
        [WoState.Cancelada]  = Array.Empty<WoState>(),
    };

    public static bool CanTransition(WoState from, WoState to) =>
        Allowed.TryGetValue(from, out var next) && next.Contains(to);

    /// <summary>
    /// Re-validación de autoridad en servidor (ADR-011 v1.1).
    /// Devuelve el veredicto del intento de transición llegado desde un cliente offline.
    /// </summary>
    public static Verdict RevalidateTransition(WoState serverState, WoState attempted)
    {
        if (serverState == attempted) return Verdict.AcceptDuplicate; // idempotencia: mismo resultado
        if (CanTransition(serverState, attempted)) return Verdict.Accept;
        // Servidor autoritativo en estado OT (Doc 14 §matriz de conflictos)
        return Verdict.Reject;
    }
}

public enum Verdict { Accept, AcceptDuplicate, Adjust, Reject }

/// <summary>HLC — Hybrid Logical Clock (SY-6): orden causal sin relojes confiables.</summary>
public readonly record struct Hlc(long PhysicalMs, long Logical)
{
    public Hlc Tick(long nowMs) =>
        new(Math.Max(nowMs, PhysicalMs), nowMs > PhysicalMs ? 0 : Logical + 1);

    public Hlc Merge(Hlc other, long nowMs)
    {
        var maxPhys = Math.Max(Math.Max(PhysicalMs, other.PhysicalMs), nowMs);
        var logical = maxPhys == PhysicalMs && maxPhys == other.PhysicalMs
            ? Math.Max(Logical, other.Logical) + 1
            : maxPhys == PhysicalMs ? Logical + 1
            : maxPhys == other.PhysicalMs ? other.Logical + 1
            : 0;
        return new Hlc(maxPhys, logical);
    }

    public static int Compare(Hlc a, Hlc b) =>
        a.PhysicalMs != b.PhysicalMs
            ? a.PhysicalMs.CompareTo(b.PhysicalMs)
            : a.Logical.CompareTo(b.Logical);
}
