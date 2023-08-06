""" vector field traversals (incl. multi-threading and halo-filling logic) """
import numba

from .enumerations import (
    INNER,
    INVALID_INDEX,
    MID3D,
    ONE_FOR_STAGGERED_GRID,
    OUTER,
    RNG_START,
    RNG_STOP,
    SIGN_LEFT,
    SIGN_RIGHT,
)
from .meta import META_HALO_VALID
from .traversals_common import _make_common


def _make_apply_vector(
    *,
    indexers,
    jit_flags,
    halo,
    n_dims,
    n_threads,
    spanner,
    chunker,
    boundary_cond_vector,
    boundary_cond_scalar
):
    set_value = indexers[n_dims].set
    common = _make_common(jit_flags, spanner, chunker)
    halos = ((halo - 1, halo, halo), (halo, halo - 1, halo), (halo, halo, halo - 1))

    @numba.njit(**jit_flags)
    # pylint: disable=too-many-arguments,too-many-locals
    def apply_vector_impl(
        thread_id,
        out_meta,
        fun_outer,
        fun_mid3d,
        fun_inner,
        out_outer,
        out_mid3d,
        out_inner,
        scal_arg1,
        vec_arg2_outer,
        vec_arg2_mid3d,
        vec_arg2_inner,
        scal_arg3,
    ):
        span, rng_outer, last_thread, _ = common(out_meta, thread_id)
        rng_mid3d = (0, span[MID3D])
        rng_inner = (0, span[INNER])
        arg2 = (vec_arg2_outer, vec_arg2_mid3d, vec_arg2_inner)

        for i in (
            range(
                rng_outer[RNG_START] + halos[OUTER][OUTER],
                rng_outer[RNG_STOP]
                + halos[OUTER][OUTER]
                + (ONE_FOR_STAGGERED_GRID if last_thread else 0),
            )
            if n_dims > 1
            else (INVALID_INDEX,)
        ):
            for j in (
                range(
                    rng_mid3d[RNG_START] + halos[MID3D][MID3D],
                    rng_mid3d[RNG_STOP] + ONE_FOR_STAGGERED_GRID + halos[MID3D][MID3D],
                )
                if n_dims > 2
                else (INVALID_INDEX,)
            ):
                for k in range(
                    rng_inner[RNG_START] + halos[INNER][INNER],
                    rng_inner[RNG_STOP] + ONE_FOR_STAGGERED_GRID + halos[INNER][INNER],
                ):
                    focus = (i, j, k)
                    if n_dims > 1:
                        set_value(
                            out_outer,
                            i,
                            j,
                            k,
                            fun_outer(
                                (focus, scal_arg1), (focus, arg2), (focus, scal_arg3)
                            ),
                        )
                        if n_dims > 2:
                            set_value(
                                out_mid3d,
                                i,
                                j,
                                k,
                                fun_mid3d(
                                    (focus, scal_arg1),
                                    (focus, arg2),
                                    (focus, scal_arg3),
                                ),
                            )
                    set_value(
                        out_inner,
                        i,
                        j,
                        k,
                        fun_inner(
                            (focus, scal_arg1), (focus, arg2), (focus, scal_arg3)
                        ),
                    )

    @numba.njit(**{**jit_flags, **{"parallel": n_threads > 1}})
    # pylint: disable=too-many-arguments,too-many-locals
    def apply_vector(
        fun_outer,
        fun_mid3d,
        fun_inner,
        out_meta,
        out_outer,
        out_mid3d,
        out_inner,
        arg1s_meta,
        arg1s_data,
        arg1s_bc_o,
        arg1s_bc_m,
        arg1s_bc_i,
        arg2v_meta,
        arg2v_data_o,
        arg2v_data_m,
        arg2v_data_i,
        arg2v_bc_o,
        arg2v_bc_m,
        arg2v_bc_i,
        arg3s_meta,
        arg3s_data,
        arg3s_bc_o,
        arg3s_bc_m,
        arg3s_bc_i,
    ):
        for thread_id in range(1) if n_threads == 1 else numba.prange(n_threads):
            boundary_cond_scalar(
                thread_id, arg1s_meta, arg1s_data, arg1s_bc_o, arg1s_bc_m, arg1s_bc_i
            )
            boundary_cond_vector(
                thread_id,
                arg2v_meta,
                arg2v_data_o,
                arg2v_data_m,
                arg2v_data_i,
                arg2v_bc_o,
                arg2v_bc_m,
                arg2v_bc_i,
            )
            boundary_cond_scalar(
                thread_id, arg3s_meta, arg3s_data, arg3s_bc_o, arg3s_bc_m, arg3s_bc_i
            )
        if not arg1s_meta[META_HALO_VALID]:
            arg1s_meta[META_HALO_VALID] = True
        if not arg2v_meta[META_HALO_VALID]:
            arg2v_meta[META_HALO_VALID] = True
        if not arg3s_meta[META_HALO_VALID]:
            arg3s_meta[META_HALO_VALID] = True

        for thread_id in range(1) if n_threads == 1 else numba.prange(n_threads):
            # pylint: disable=duplicate-code
            apply_vector_impl(
                thread_id,
                out_meta,
                fun_outer,
                fun_mid3d,
                fun_inner,
                out_outer,
                out_mid3d,
                out_inner,
                arg1s_data,
                arg2v_data_o,
                arg2v_data_m,
                arg2v_data_i,
                arg3s_data,
            )
        out_meta[META_HALO_VALID] = False

    return apply_vector


# pylint: disable=too-many-statements,too-many-locals
def _make_fill_halos_vector(*, indexers, jit_flags, halo, n_dims, chunker, spanner):
    set_value = indexers[n_dims].set
    common = _make_common(jit_flags, spanner, chunker)
    halos = ((halo - 1, halo, halo), (halo, halo - 1, halo), (halo, halo, halo - 1))

    @numba.njit(**jit_flags)
    def outer_outer(span, comp, fun, first_thread, last_thread):
        if first_thread:
            for i in range(
                halos[OUTER][OUTER] - 1, -1, -1
            ):  # note: non-reverse order assumed in Extrapolated
                for j in (
                    range(0, span[MID3D] + 2 * halo) if n_dims > 2 else (INVALID_INDEX,)
                ):
                    for k in range(0, span[INNER] + 2 * halos[OUTER][INNER]):
                        focus = (i, j, k)
                        set_value(
                            comp,
                            i,
                            j,
                            k,
                            fun((focus, comp), span[OUTER] + 1, SIGN_LEFT),
                        )
        if last_thread:
            for i in range(
                span[OUTER] + ONE_FOR_STAGGERED_GRID + halos[OUTER][OUTER],
                span[OUTER] + ONE_FOR_STAGGERED_GRID + 2 * halos[OUTER][OUTER],
            ):  # note: non-reverse order assumed in Extrapolated
                for j in (
                    range(0, span[MID3D] + 2 * halo) if n_dims > 2 else (INVALID_INDEX,)
                ):
                    for k in range(0, span[INNER] + 2 * halos[OUTER][INNER]):
                        focus = (i, j, k)
                        set_value(
                            comp,
                            i,
                            j,
                            k,
                            fun((focus, comp), span[OUTER] + 1, SIGN_RIGHT),
                        )

    @numba.njit(**jit_flags)
    def outer_mid3d(span, comp, fun, rng_outer, last_thread):
        for i in range(
            rng_outer[RNG_START],
            rng_outer[RNG_STOP]
            + (
                (ONE_FOR_STAGGERED_GRID + 2 * halos[OUTER][OUTER]) if last_thread else 0
            ),
        ):
            for j in range(0, halos[OUTER][MID3D]):
                for k in range(0, span[INNER] + 2 * halo):
                    focus = (i, j, k)
                    set_value(comp, i, j, k, fun((focus, comp), span[MID3D], SIGN_LEFT))
            for j in range(
                span[MID3D] + halos[OUTER][MID3D], span[MID3D] + 2 * halos[OUTER][MID3D]
            ):
                for k in range(0, span[INNER] + 2 * halo):
                    focus = (i, j, k)
                    set_value(
                        comp, i, j, k, fun((focus, comp), span[MID3D], SIGN_RIGHT)
                    )

    @numba.njit(**jit_flags)
    def outer_inner(span, comp, fun, rng_outer, last_thread):
        for i in range(
            rng_outer[RNG_START],
            rng_outer[RNG_STOP]
            + (
                (ONE_FOR_STAGGERED_GRID + 2 * halos[OUTER][OUTER]) if last_thread else 0
            ),
        ):
            for j in (
                range(0, span[MID3D] + 2 * halo) if n_dims > 2 else (INVALID_INDEX,)
            ):
                for k in range(0, halos[OUTER][INNER]):
                    focus = (i, j, k)
                    set_value(comp, i, j, k, fun((focus, comp), span[INNER], SIGN_LEFT))
                for k in range(
                    span[INNER] + halos[OUTER][INNER],
                    span[INNER] + 2 * halos[OUTER][INNER],
                ):
                    focus = (i, j, k)
                    set_value(
                        comp, i, j, k, fun((focus, comp), span[INNER], SIGN_RIGHT)
                    )

    @numba.njit(**jit_flags)
    def mid3d_outer(span, comp, fun, first_thread, last_thread):
        if first_thread:
            for i in range(0, halos[MID3D][OUTER]):
                for j in range(
                    0, span[MID3D] + ONE_FOR_STAGGERED_GRID + 2 * halos[MID3D][MID3D]
                ):
                    for k in range(0, span[INNER] + 2 * halo):
                        focus = (i, j, k)
                        set_value(
                            comp, i, j, k, fun((focus, comp), span[OUTER], SIGN_LEFT)
                        )
        if last_thread:
            for i in range(
                span[OUTER] + halos[MID3D][OUTER], span[OUTER] + 2 * halos[MID3D][OUTER]
            ):
                for j in range(
                    0, span[MID3D] + ONE_FOR_STAGGERED_GRID + 2 * halos[MID3D][MID3D]
                ):
                    for k in range(0, span[INNER] + 2 * halo):
                        focus = (i, j, k)
                        set_value(
                            comp, i, j, k, fun((focus, comp), span[OUTER], SIGN_RIGHT)
                        )

    @numba.njit(**jit_flags)
    def mid3d_mid3d(span, comp, fun, rng_outer, last_thread):
        for i in range(
            rng_outer[RNG_START],
            rng_outer[RNG_STOP] + (2 * halos[MID3D][OUTER] if last_thread else 0),
        ):
            for j in range(0, halos[MID3D][MID3D]):
                for k in range(0, span[INNER] + 2 * halo):
                    focus = (i, j, k)
                    set_value(
                        comp,
                        i,
                        j,
                        k,
                        fun(
                            (focus, comp),
                            span[MID3D] + ONE_FOR_STAGGERED_GRID,
                            SIGN_LEFT,
                        ),
                    )
            for j in range(
                span[MID3D] + 1 + halos[MID3D][MID3D],
                span[MID3D] + ONE_FOR_STAGGERED_GRID + 2 * halos[MID3D][MID3D],
            ):
                for k in range(0, span[INNER] + 2 * halo):
                    focus = (i, j, k)
                    set_value(
                        comp,
                        i,
                        j,
                        k,
                        fun(
                            (focus, comp),
                            span[MID3D] + ONE_FOR_STAGGERED_GRID,
                            SIGN_RIGHT,
                        ),
                    )

    @numba.njit(**jit_flags)
    def mid3d_inner(span, comp, fun, rng_outer, last_thread):
        for i in range(
            rng_outer[RNG_START],
            rng_outer[RNG_STOP] + (2 * halos[MID3D][OUTER] if last_thread else 0),
        ):
            for j in range(
                0, span[MID3D] + ONE_FOR_STAGGERED_GRID + 2 * halos[MID3D][MID3D]
            ):
                for k in range(0, halos[MID3D][INNER]):
                    focus = (i, j, k)
                    set_value(comp, i, j, k, fun((focus, comp), span[INNER], SIGN_LEFT))
                for k in range(
                    span[INNER] + halos[MID3D][INNER],
                    span[INNER] + 2 * halos[MID3D][INNER],
                ):
                    focus = (i, j, k)
                    set_value(
                        comp, i, j, k, fun((focus, comp), span[INNER], SIGN_RIGHT)
                    )

    @numba.njit(**jit_flags)
    def inner_outer(span, comp, fun, first_thread, last_thread):
        if first_thread:
            for i in range(0, halos[INNER][OUTER]):
                for j in (
                    range(0, span[MID3D] + 2 * halo) if n_dims > 2 else (INVALID_INDEX,)
                ):
                    for k in range(
                        0,
                        span[INNER] + ONE_FOR_STAGGERED_GRID + 2 * halos[INNER][INNER],
                    ):
                        focus = (i, j, k)
                        set_value(
                            comp, i, j, k, fun((focus, comp), span[OUTER], SIGN_LEFT)
                        )
        if last_thread:
            for i in range(
                span[OUTER] + halos[INNER][OUTER], span[OUTER] + 2 * halos[INNER][OUTER]
            ):
                for j in (
                    range(0, span[MID3D] + 2 * halo) if n_dims > 2 else (INVALID_INDEX,)
                ):
                    for k in range(
                        0,
                        span[INNER] + ONE_FOR_STAGGERED_GRID + 2 * halos[INNER][INNER],
                    ):
                        focus = (i, j, k)
                        set_value(
                            comp, i, j, k, fun((focus, comp), span[OUTER], SIGN_RIGHT)
                        )

    @numba.njit(**jit_flags)
    def inner_inner(span, comp, fun, last_thread, rng_outer):
        for i in (
            range(
                rng_outer[RNG_START],
                rng_outer[RNG_STOP] + (2 * halos[INNER][OUTER] if last_thread else 0),
            )
            if n_dims > 1
            else (INVALID_INDEX,)
        ):
            for j in (
                range(0, span[MID3D] + 2 * halo) if n_dims > 2 else (INVALID_INDEX,)
            ):
                for k in range(0, halos[INNER][INNER]):
                    focus = (i, j, k)
                    set_value(
                        comp,
                        i,
                        j,
                        k,
                        fun(
                            (focus, comp),
                            span[INNER] + ONE_FOR_STAGGERED_GRID,
                            SIGN_LEFT,
                        ),
                    )
                for k in range(
                    span[INNER] + 1 + halos[INNER][INNER],
                    span[INNER] + ONE_FOR_STAGGERED_GRID + 2 * halos[INNER][INNER],
                ):
                    focus = (i, j, k)
                    set_value(
                        comp,
                        i,
                        j,
                        k,
                        fun(
                            (focus, comp),
                            span[INNER] + ONE_FOR_STAGGERED_GRID,
                            SIGN_RIGHT,
                        ),
                    )

    @numba.njit(**jit_flags)
    def inner_mid3d(span, comp, fun, rng_outer, last_thread):
        for i in range(
            rng_outer[RNG_START],
            rng_outer[RNG_STOP] + (2 * halos[INNER][OUTER] if last_thread else 0),
        ):
            for j in range(0, halos[INNER][MID3D]):
                for k in range(
                    0, span[INNER] + ONE_FOR_STAGGERED_GRID + 2 * halos[INNER][INNER]
                ):
                    focus = (i, j, k)
                    set_value(comp, i, j, k, fun((focus, comp), span[MID3D], SIGN_LEFT))
            for j in range(
                span[MID3D] + halos[INNER][MID3D], span[MID3D] + 2 * halos[INNER][MID3D]
            ):
                for k in range(
                    0, span[INNER] + ONE_FOR_STAGGERED_GRID + 2 * halos[INNER][INNER]
                ):
                    focus = (i, j, k)
                    set_value(
                        comp, i, j, k, fun((focus, comp), span[MID3D], SIGN_RIGHT)
                    )

    @numba.njit(**jit_flags)
    # pylint: disable=too-many-arguments
    def boundary_cond_vector(
        thread_id,
        meta,
        comp_outer,
        comp_mid3d,
        comp_inner,
        fun_outer,
        fun_mid3d,
        fun_inner,
    ):
        if meta[META_HALO_VALID]:
            return
        span, rng_outer, last_thread, first_thread = common(meta, thread_id)

        if n_dims > 1:
            outer_outer(span, comp_outer, fun_outer, first_thread, last_thread)
            if n_dims > 2:
                outer_mid3d(span, comp_outer, fun_mid3d, rng_outer, last_thread)
            outer_inner(span, comp_outer, fun_inner, rng_outer, last_thread)

        if n_dims > 2:
            mid3d_outer(span, comp_mid3d, fun_outer, first_thread, last_thread)
            mid3d_mid3d(span, comp_mid3d, fun_mid3d, rng_outer, last_thread)
            mid3d_inner(span, comp_mid3d, fun_inner, rng_outer, last_thread)

        if n_dims > 1:
            inner_outer(span, comp_inner, fun_outer, first_thread, last_thread)
            if n_dims > 2:
                inner_mid3d(span, comp_inner, fun_mid3d, rng_outer, last_thread)
        inner_inner(span, comp_inner, fun_inner, last_thread, rng_outer)

    return boundary_cond_vector
