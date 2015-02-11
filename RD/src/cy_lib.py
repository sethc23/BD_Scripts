import pyximport#,pp
pyximport.install(build_in_temp=False,inplace=True)
import Cython.Compiler.Options
Cython.Compiler.Options.annotate = True
import cython_exts as cy
from cy.getBestDG import c_getBestDG

# from cython_exts.order_by_min import c_order_by_min
# from cython_exts.get_combo_start_info import c_get_combo_start_info
# from cython_exts.update_order_results import c_update_order_results
# from cython_exts.eval_single_order import c_eval_single_order
# from cython_exts.bestED import c_bestED
# from cython_exts.getBestDG import c_getBestDG
