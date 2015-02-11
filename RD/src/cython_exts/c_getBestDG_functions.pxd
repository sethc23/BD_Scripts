
cdef extern from "update_order_results.c":
    long[:,::1] c_update_order_results(long[:, ::1], long[:, ::1], long)