# -*- coding: utf-8 -*-

#
# General Includes

from fpylll.gmp.mpz cimport mpz_t
from fpylll.gmp.random cimport gmp_randstate_t
from libcpp.vector cimport vector
from libcpp.string cimport string

#
# Numbers

cdef extern from "fplll/nr/nr.h" namespace "fplll":

    ctypedef double enumf

    cdef cppclass Z_NR[T]:
        T& get_data() nogil
        void set "operator=" (T d) nogil
        double get_d() nogil
        long exponent() nogil
        void set_str(const char* s) nogil
        int cmp(const Z_NR[T]& m) nogil
        int sgn() nogil

        void operator=(const Z_NR[T]& z) nogil
        void operator=(const mpz_t& z) nogil
        void operator=(long i) nogil
        int operator<(const Z_NR[T]& a) nogil
        int operator<(long a) nogil
        int operator>(const Z_NR[T]& a) nogil
        int operator>(long a) nogil
        int operator<=(const Z_NR[T]& a) nogil
        int operator<=(long a) nogil
        int operator>=(const Z_NR[T]& a) nogil
        int operator>=(long a) nogil
        int operator==(const Z_NR[T]& a) nogil
        int operator==(long a) nogil
        int operator!=(const Z_NR[T]& a) nogil
        int operator!=(long a) nogil

        void add(const Z_NR[T]& a, const Z_NR[T]& b) nogil
        void add_ui(const Z_NR[T]& a, unsigned int b) nogil
        void sub(const Z_NR[T]& a, const Z_NR[T]& b) nogil
        void sub_ui(const Z_NR[T]& a, unsigned int b) nogil
        void neg(const Z_NR[T]& a) nogil
        void mul(const Z_NR[T]& a, const Z_NR[T]& b) nogil
        void mul_si(const Z_NR[T]& a, long b) nogil
        void mul_ui(const Z_NR[T]& a, unsigned long b) nogil
        void mul_2si(const Z_NR[T]& a, long b) nogil
        void div_2si(const Z_NR[T]& a, long b) nogil
        void addmul(const Z_NR[T]& a, const Z_NR[T]& b) nogil
        void addmul_ui(const Z_NR[T]& a, unsigned long b) nogil
        void addmul_si(const Z_NR[T]& a, long b) nogil
        void submul(const Z_NR[T]& a, const Z_NR[T]& b) nogil
        void submul_ui(const Z_NR[T]& a, unsigned long b) nogil
        void abs(const Z_NR[T]& a) nogil
        void swap(Z_NR[T]& a) nogil
        void randb(int bits) nogil
        void randb_si(int bits) nogil
        void randm(const Z_NR[T]& max) nogil
        void randm_si(const Z_NR[T]& max) nogil


    cdef cppclass FP_NR[T]:
        T& get_data() nogil
        double get_d() nogil
        inline void operator=(const FP_NR[T]& a) nogil
        inline void operator=(double a) nogil

        @staticmethod
        unsigned int get_prec() nogil

        @staticmethod
        unsigned int set_prec(unsigned int) nogil

cdef extern from "fplll/nr/nr.h":
    cdef struct dpe_struct:
        pass
    ctypedef dpe_struct *dpe_t


# Random Numbers


cdef extern from "fplll/nr/nr.h" namespace "fplll":

    cdef cppclass RandGen:
        @staticmethod
        void init()

        @staticmethod
        void init_with_seed(unsigned long seed)

        @staticmethod
        void init_with_time()

        @staticmethod
        void init_with_time2()

        @staticmethod
        int get_initialized()

        @staticmethod
        gmp_randstate_t& get_gmp_state()


# Definitions & Enums

cdef extern from "fplll/defs.h" namespace "fplll":

    cdef enum RedStatus:
        RED_SUCCESS
        RED_GSO_FAILURE
        RED_BABAI_FAILURE
        RED_LLL_FAILURE
        RED_ENUM_FAILURE
        RED_BKZ_FAILURE
        RED_BKZ_TIME_LIMIT
        RED_BKZ_LOOPS_LIMIT
        RED_STATUS_MAX

    cdef enum LLLFlags:
        LLL_VERBOSE
        LLL_EARLY_RED
        LLL_SIEGEL
        LLL_DEFAULT

    cdef enum BKZFlags:
        BKZ_DEFAULT
        BKZ_VERBOSE
        BKZ_NO_LLL
        BKZ_MAX_LOOPS
        BKZ_MAX_TIME
        BKZ_BOUNDED_LLL
        BKZ_AUTO_ABORT
        BKZ_DUMP_GSO
        BKZ_GH_BND

    cdef enum LLLMethod:
        LM_WRAPPER
        LM_PROVED
        LM_HEURISTIC
        LM_FAST

    cdef enum SVPMethod:
        SVPM_FAST
        SVPM_PROVED

    cdef enum SVPFlags:
        SVP_DEFAULT
        SVP_VERBOSE
        SVP_OVERRIDE_BND

    cdef enum CVPFlags:
        CVP_DEFAULT
        CVP_VERBOSE

    cdef enum IntType:
        ZT_MPZ
        ZT_LONG
        ZT_DOUBLE

    cdef enum FloatType:
        FT_DEFAULT
        FT_DOUBLE
        FT_LONG_DOUBLE
        FT_DD
        FT_QD
        FT_DPE
        FT_MPFR

    cdef enum SVPMethod:
        SVPM_FAST
        SVPM_PROVED

    cdef double LLL_DEF_DELTA
    cdef double LLL_DEF_ETA


    const double BKZ_DEF_AUTO_ABORT_SCALE
    const int BKZ_DEF_AUTO_ABORT_MAX_NO_DEC
    const double BKZ_DEF_GH_FACTOR
    const double BKZ_DEF_MIN_SUCCESS_PROBABILITY
    const int BKZ_DEF_RERANDOMIZATION_DENSITY


# Matrices over the Integers

cdef extern from "fplll/nr/matrix.h" namespace "fplll":
    cdef cppclass MatrixRow[T]:
        T& operator[](int i) nogil
        int size() nogil
        int is_zero() nogil
        int is_zero(int frm) nogil
        int size_nz() nogil
        void fill(long value) nogil
        void add(const MatrixRow[T] v) nogil
        void add(const MatrixRow[T] v, int n) nogil
        void sub(const MatrixRow[T] v) nogil
        void sub(const MatrixRow[T] v, int n) nogil
        void addmul_2exp(const MatrixRow[T]& v, const T& x, long expo, T& tmp) nogil
        void addmul_2exp(const MatrixRow[T]& v, const T& x, long expo, int n, T& tmp) nogil
        void addmul_si(const MatrixRow[T]& v, long x) nogil
        void addmul_si(const MatrixRow[T]& v, long x, int n) nogil
        void addmul_si_2exp(const MatrixRow[T]& v, long x, long expo, T& tmp) nogil
        void addmul_si_2exp(const MatrixRow[T]& v, long x, long expo, int n, T& tmp) nogil

    void dot_product[T](T& result, const MatrixRow[T]& v1, const MatrixRow[T]& v2, int n) nogil
    void dot_product[T](T& result, const MatrixRow[T]& v1, const MatrixRow[T]& v2) nogil

    cdef cppclass Matrix[T]:
        Matrix()
        Matrix(int r, int c)

        int get_rows()
        int get_cols()

        T& operator()(int i, int j)
        MatrixRow[T] operator[](int i)

        void clear()
        int empty()
        void resize(int rows, int cols) nogil
        void set_rows(int rows) nogil
        void set_cols(int cols) nogil
        void swap(Matrix[T]& m) nogil

        void swap_rows(int r1, int r2) nogil
        void rotate_left(int first, int last) nogil
        void rotate_right(int first, int last) nogil
        void rotate(int first, int middle, int last) nogil
        void rotate_gram_left(int first, int last, int nValidRows) nogil
        void rotate_gram_right(int first, int last, int nValidRows) nogil
        void transpose() nogil
        long get_max_exp() nogil

    cdef cppclass ZZ_mat[T]:

        ZZ_mat()
        ZZ_mat(int r, int c)

        int get_rows() nogil
        int get_cols() nogil
        void set_rows(int rows) nogil
        void set_cols(int cols) nogil

        Z_NR[T]& operator()(int i, int j) nogil
        MatrixRow[Z_NR[T]] operator[](int i) nogil

        void gen_identity(int nrows) nogil
        void gen_intrel(int bits) nogil
        void gen_simdioph(int bits, int bits2) nogil
        void gen_uniform(int bits) nogil
        void gen_ntrulike(int bits) nogil
        void gen_ntrulike_withq(int q) nogil
        void gen_ntrulike2(int bits) nogil
        void gen_ntrulike2_withq(int q) nogil
        void gen_qary_withq(int k, int q) nogil
        void gen_qary_prime(int k, int bits) nogil
        void gen_trg(double alpha) nogil



# Gram Schmidt Orthogonalization

cdef extern from "fplll/gso.h" namespace "fplll":

    cdef enum MatGSOFlags:
        GSO_DEFAULT
        GSO_INT_GRAM
        GSO_ROW_EXPO
        GSO_OP_FORCE_LONG

    cdef cppclass MatGSO[ZT, FT]:
        MatGSO(Matrix[ZT] B, Matrix[ZT] U, Matrix[ZT] UinvT, int flags)

        int d
        Matrix[ZT]& b
        vector[long] row_expo
        void row_op_begin(int first, int last)
        void row_op_end(int first, int last)
        FT& get_gram(FT& f, int i, int j)

        const Matrix[FT]& get_mu_matrix() nogil
        const FT& get_mu_exp(int i, int j, long& expo) nogil
        const FT& get_mu_exp(int i, int j) nogil
        FT& get_mu(FT& f, int i, int j) nogil

        const Matrix[FT]& get_rmatrix() nogil
        const FT& get_r_exp(int i, int j, long& expo) nogil
        const FT& get_r_exp(int i, int j) nogil
        FT& get_r(FT& f, int i, int j) nogil

        long get_max_mu_exp(int i, int nColumns) nogil

        int update_gso_row(int i, int lastJ) nogil
        int update_gso_row(int i) nogil
        int update_gso() nogil

        void discover_all_rows() nogil
        void set_r(int i, int j, FT& f) nogil
        void move_row(int oldR, int newR) nogil
        void swap_rows(int row1, int row2)

        void row_addmul(int i, int j, const FT& x) nogil
        void row_addmul_we(int i, int j, const FT& x, long expoAdd) nogil

        void lock_cols() nogil
        void unlock_cols() nogil

        void create_row() nogil
        void create_rows(int nNewRows) nogil

        void remove_last_row() nogil
        void remove_last_rows(int nRemovedRows) nogil

        void apply_transform(const Matrix[FT]& transform, int srcBase, int targetBase) nogil
        void apply_transform(const Matrix[FT]& transform, int srcBase) nogil

        void dump_mu_d(double* mu, int offset, int block_size) nogil
        void dump_mu_d(vector[double] mu, int offset, int block_size) nogil

        void dump_r_d(double* r, int offset, int block_size) nogil
        void dump_r_d(vector[double] r, int offset, int block_size) nogil

        double get_current_slope(int start_row, int stop_row) nogil
        FT get_root_det(int start_row, int stop_row) nogil
        FT get_log_det(int start_row, int stop_row) nogil
        FT get_slide_potential(int start_row, int stop_row, int block_size) nogil

        const int enable_int_gram
        const int enable_row_expo
        const int enable_transform

        const int enable_inverse_transform
        const int row_op_force_long



# LLL

cdef extern from "fplll/lll.h" namespace "fplll":

    cdef cppclass LLLReduction[ZT,FT]:
        LLLReduction(MatGSO[ZT, FT]& m, double delta, double eta, int flags)

        int lll() nogil
        int lll(int kappaMin) nogil
        int lll(int kappaMin, int kappaStart) nogil
        int lll(int kappaMin, int kappaStart, int kappaEnd) nogil
        int size_reduction() nogil
        int size_reduction(int kappaMin) nogil
        int size_reduction(int kappaMin, int kappaEnd) nogil

        int status
        int final_kappa
        int last_early_red
        int zeros
        int n_swaps

    int is_lll_reduced[ZT, FT](MatGSO[ZT, FT]& m, double delta, double eta) nogil


# LLL Wrapper

cdef extern from "fplll/wrapper.h" namespace "fplll":

    cdef cppclass Wrapper:
        Wrapper(ZZ_mat[mpz_t]& b, ZZ_mat[mpz_t]& u, ZZ_mat[mpz_t]& uInv,
                double delta, double eta, int flags)
        int lll() nogil
        int status



# Evaluator

cdef extern from "fplll/enum/evaluator.h" namespace "fplll":

    cdef cppclass Evaluator[FT]:
        Evaluator()

        void eval_sol(const vector[FT]& newSolCoord,
                      const enumf& newPartialDist, enumf& maxDist, long normExp)

        vector[FT] sol_coord
        int new_sol_flag


    cdef cppclass FastEvaluator[FT]:
        FastEvaluator()

        void eval_sol(const vector[FT]& newSolCoord,
                      const enumf& newPartialDist, enumf& maxDist, long normExp)

        vector[FT] sol_coord
        int new_sol_flag



# Enumeration

cdef extern from "fplll/enum/enumerate.h" namespace "fplll":
    cdef cppclass Enumeration[FT]:
        Enumeration(MatGSO[Z_NR[mpz_t], FT]& gso, FastEvaluator[FT]& evaluator)

        void enumerate(int first, int last, FT& fMaxDist, long maxDistExpo,
                       const vector[FT]& targetCoord,
                       const vector[double]& subTree,
                       const vector[double]& pruning,
                       int dual)

        long get_nodes()



# SVP

cdef extern from "fplll/svpcvp.h" namespace "fplll":
    int shortest_vector(ZZ_mat[mpz_t]& b,
                        vector[Z_NR[mpz_t]] &sol_coord,
                        SVPMethod method, int flags) nogil

    int shortest_vector_pruning(ZZ_mat[mpz_t]& b, vector[Z_NR[mpz_t]]& sol_coord,
                                const vector[double]& pruning, int flags) nogil

    # Experimental. Do not use.
    int closest_vector(ZZ_mat[mpz_t] b, vector[Z_NR[mpz_t]] &intTarget,
                       vector[Z_NR[mpz_t]]& sol_coord, int flags) nogil



# BKZ

cdef extern from "fplll/bkz_param.h" namespace "fplll":

    cdef cppclass Pruning:
        double radius_factor
        vector[double] coefficients
        double probability

        Pruning()

        @staticmethod
        Pruning LinearPruning(int block_size, int level)

    cdef cppclass Strategy:
        size_t block_size
        vector[Pruning] pruning_parameters
        vector[size_t] preprocessing_block_sizes

        @staticmethod
        Strategy EmptyStrategy()

        Pruning get_pruning(double radius, double gh)

    cdef cppclass BKZParam:
        BKZParam() nogil
        BKZParam(int block_size) nogil
        BKZParam(int block_size, vector[Strategy] strategies, double delta) nogil
        BKZParam(int block_size, vector[Strategy] strategies, double delta, int flags, int max_loops, int max_time,
                 double auto_abort_scale, int auto_abort_max_no_dec) nogil
        BKZParam(int block_size, vector[Strategy] strategies, double delta, int flags, int max_loops, int max_time,
                 double auto_abort_scale, int auto_abort_max_no_dec, double gh_factor) nogil
        int block_size
        double delta
        int flags
        int max_loops
        double max_time

        double auto_abort_scale
        int auto_abort_max_no_dec

        vector[Strategy] strategies

        double gh_factor

        double min_success_probability

        int rerandomization_density

        string dump_gso_filename

    vector[Strategy] load_strategies_json(const string &filename) nogil
    const string default_strategy_path() nogil
    const string default_strategy() nogil
    const string strategy_full_path(const string &strategy_path) nogil


cdef extern from "fplll/bkz.h" namespace "fplll":

    cdef cppclass BKZReduction[FT]:

        BKZReduction(MatGSO[Z_NR[mpz_t], FT] &m, LLLReduction[Z_NR[mpz_t], FT] &lll_obj, const BKZParam &param) nogil

        int svp_preprocessing(int kappa, int block_size, const BKZParam &param) nogil
        int svp_postprocessing(int kappa, int block_size, const vector[FT] &solution) nogil
        int dsvp_postprocessing(int kappa, int block_size, const vector[FT] &solution) nogil

        int svp_reduction(int kappa, int block_size, const BKZParam &param, int dual) nogil except +

        int tour(const int loop, int &kappa_max, const BKZParam &param, int min_row, int max_row) nogil except +
        int sd_tour(const int loop, const BKZParam &param, int min_row, int max_row) nogil except +
        int slide_tour(const int loop, const BKZParam &param, int min_row, int max_row) nogil except +

        int hkz(int &kappaMax, const BKZParam &param, int min_row, int max_row) nogil except +

        int bkz()

        void rerandomize_block(int min_row, int max_row, int density) nogil except +

        void dump_gso(const string filename, const string prefix, int append) nogil except +

        int status

        long nodes


    cdef cppclass BKZAutoAbort[FT]:
        BKZAutoAbort(MatGSO[Z_NR[mpz_t], FT]& m, int num_rows) nogil
        BKZAutoAbort(MatGSO[Z_NR[mpz_t], FT]& m, int num_rows, int start_row) nogil

        int test_abort() nogil
        int test_abort(double scale) nogil
        int test_abort(double scale, int max_no_dec) nogil

    void gaussian_heuristic[FT](FT& max_dist, long max_dist_expo,
                                        int block_size, FT& root_det_mpfr, double gh_factor) nogil

    FT get_root_det[FT](MatGSO[Z_NR[mpz_t], FT]& m, int start, int end)
    FT get_log_det[FT](MatGSO[Z_NR[mpz_t], FT]& m, int start, int end)
    FT get_sld_potential[FT](MatGSO[Z_NR[mpz_t], FT]& m, int start, int end, int block_size)

    double get_current_slope[FT](MatGSO[Z_NR[mpz_t], FT]& m, int startRow, int stopRow) nogil


# Utility

cdef extern from "fplll/util.h" namespace "fplll":
    void vector_matrix_product(vector[Z_NR[mpz_t]] &result,
                               vector[Z_NR[mpz_t]] &x,
                               const ZZ_mat[mpz_t] &m) nogil

    void sqr_norm[T](T& result, const MatrixRow[T]& v, int n) nogil



# Pruner

cdef extern from "fplll/pruner.h" namespace "fplll":

    cdef cppclass Pruner[FT]:

        FT preproc_cost
        FT target_probability
        FT enumeration_radius;

        Pruner()
        Pruner(double enumeration_radius, double preproc_cost, double target_probability, int descent_method)
        Pruner(FT enumeration_radius, FT preproc_cost, FT target_probability)
        Pruner(FT enumeration_radius, FT preproc_cost, FT target_probability, size_t n, size_t d)

        void load_basis_shape[GSO_ZT, GSO_FT](MatGSO[GSO_ZT, GSO_FT] &gso, int start_row, int end_row, int reset_renorm)
        void load_basis_shape(const vector[double] &gso_sq_norms, int reset_renorm)

        void load_basis_shapes[GSO_ZT, GSO_FT](vector[MatGSO[GSO_ZT, GSO_FT]] &gsos, int start_row, int end_row)
        void load_basis_shapes(const vector[vector[double]] &gso_sq_norms_vec)

        void optimize_coefficients(vector[double] &pr, const int reset)

        double single_enum_cost(const vector[double] &pr)
        double repeated_enum_cost(const vector[double] &pr)
        double svp_probability(const vector[double] &pr)

    double svp_probability[FT](const vector[double] &pr)

    Pruning prune[FT, GSO_ZT, GSO_FT](const double enumeration_radius, const double preproc_cost,
                                      const double target_probability, vector[MatGSO[GSO_ZT, GSO_FT]] &m,
                                      const int descent_method, int start_row, int end_row)

    cdef enum PRUNER_METHOD:
        PRUNER_METHOD_GRADIENT
        PRUNER_METHOD_NM
        PRUNER_METHOD_HYBRID


# Highlevel Functions

cdef extern from "fplll/fplll.h" namespace "fplll":

    int lll_reduction(ZZ_mat[mpz_t] b, double delta, double eta,
                      LLLMethod method, FloatType float_type,
                      int precision, int flags) nogil
    int lll_reduction(ZZ_mat[mpz_t] b, ZZ_mat[mpz_t] u,
                      double delta, double eta,
                      LLLMethod method, FloatType float_type,
                      int precision, int flags) nogil

    int bkz_reduction(ZZ_mat[mpz_t] *b, ZZ_mat[mpz_t] *u,
                      BKZParam &param, FloatType float_type, int precision) nogil
    int bkz_reduction(ZZ_mat[mpz_t] *b, int block_size, int flags, FloatType float_type, int precision) nogil

    int hkz_reduction(ZZ_mat[mpz_t] b) nogil

    const char* get_red_status_str(int status) nogil
