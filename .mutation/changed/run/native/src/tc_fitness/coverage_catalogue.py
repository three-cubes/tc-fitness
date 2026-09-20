"""The repository's coverage admission rows; thresholds live in its config."""

from tc_fitness.catalogue import RuleEntry

ENTRIES = tuple(
    RuleEntry(id=name, gate=name, check="core:" + name, staged_class="always-run")
    for name in ("coverage_includes_branches", "coverage_floor", "new_code_coverage")
)


from mutmut.mutation.trampoline import wrap_in_trampoline as _mutmut_mutated, MutantDict
