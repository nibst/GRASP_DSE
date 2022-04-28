#include "sha_transform.h"
#include "AESL_pkg.h"

using namespace std;

namespace ap_rtl {

void sha_transform::thread_ap_clk_no_reset_() {
    if ( ap_rst.read() == ap_const_logic_1) {
        ap_CS_fsm = ap_ST_fsm_state1;
    } else {
        ap_CS_fsm = ap_NS_fsm.read();
    }
    if (esl_seteq<1,1,1>(ap_const_logic_1, ap_CS_fsm_state5.read())) {
        A_reg_8717 = sha_info_digest_q0.read();
        B_reg_8724 = sha_info_digest_q1.read();
        lshr_ln117_1_reg_8746 = sha_info_digest_q1.read().range(31, 2);
        lshr_ln117_20_reg_8756 = sha_info_digest_q0.read().range(31, 2);
        lshr_ln_reg_8736 = sha_info_digest_q0.read().range(31, 27);
        sha_info_data_load_6_reg_8701 = sha_info_data_q0.read();
        sha_info_data_load_7_reg_8709 = sha_info_data_q1.read();
        trunc_ln117_1_reg_8741 = trunc_ln117_1_fu_949_p1.read();
        trunc_ln117_3_reg_8751 = trunc_ln117_3_fu_963_p1.read();
        trunc_ln117_reg_8731 = trunc_ln117_fu_935_p1.read();
    }
    if (esl_seteq<1,1,1>(ap_const_logic_1, ap_CS_fsm_state6.read())) {
        C_reg_8779 = sha_info_digest_q0.read();
        D_reg_8787 = sha_info_digest_q1.read();
        sha_info_data_load_8_reg_8761 = sha_info_data_q0.read();
        sha_info_data_load_9_reg_8770 = sha_info_data_q1.read();
    }
    if (esl_seteq<1,1,1>(ap_const_logic_1, ap_CS_fsm_state7.read())) {
        E_reg_8812 = sha_info_digest_q0.read();
        add_ln117_15_reg_8822 = add_ln117_15_fu_1258_p2.read();
        add_ln117_18_reg_8844 = add_ln117_18_fu_1330_p2.read();
        lshr_ln117_23_reg_8854 = add_ln117_11_fu_1167_p2.read().range(31, 2);
        lshr_ln117_24_reg_8864 = add_ln117_15_fu_1258_p2.read().range(31, 2);
        lshr_ln117_4_reg_8839 = add_ln117_15_fu_1258_p2.read().range(31, 27);
        or_ln117_23_reg_8817 = or_ln117_23_fu_1187_p3.read();
        or_ln117_25_reg_8828 = or_ln117_25_fu_1278_p3.read();
        sha_info_data_load_10_reg_8794 = sha_info_data_q0.read();
        sha_info_data_load_11_reg_8803 = sha_info_data_q1.read();
        trunc_ln117_11_reg_8859 = trunc_ln117_11_fu_1350_p1.read();
        trunc_ln117_8_reg_8834 = trunc_ln117_8_fu_1286_p1.read();
        trunc_ln117_9_reg_8849 = trunc_ln117_9_fu_1336_p1.read();
    }
    if (esl_seteq<1,1,1>(ap_const_logic_1, ap_CS_fsm_state14.read())) {
        W_load_1_reg_9820 = W_q1.read();
        W_load_reg_9815 = W_q0.read();
        add_ln125_43_reg_9753 = add_ln125_43_fu_6269_p2.read();
        add_ln125_47_reg_9765 = add_ln125_47_fu_6360_p2.read();
        add_ln125_50_reg_9790 = add_ln125_50_fu_6399_p2.read();
        lshr_ln125_12_reg_9785 = add_ln125_47_fu_6360_p2.read().range(31, 27);
        lshr_ln125_30_reg_9775 = add_ln125_39_fu_6178_p2.read().range(31, 2);
        lshr_ln125_31_reg_9800 = add_ln125_43_fu_6269_p2.read().range(31, 2);
        lshr_ln125_32_reg_9810 = add_ln125_47_fu_6360_p2.read().range(31, 2);
        or_ln125_50_reg_9758 = or_ln125_50_fu_6289_p3.read();
        trunc_ln125_23_reg_9770 = trunc_ln125_23_fu_6366_p1.read();
        trunc_ln125_24_reg_9780 = trunc_ln125_24_fu_6380_p1.read();
        trunc_ln125_25_reg_9795 = trunc_ln125_25_fu_6405_p1.read();
        trunc_ln125_27_reg_9805 = trunc_ln125_27_fu_6419_p1.read();
    }
    if (esl_seteq<1,1,1>(ap_const_logic_1, ap_CS_fsm_state15.read())) {
        W_load_2_reg_9887 = W_q0.read();
        W_load_3_reg_9892 = W_q1.read();
        add_ln125_71_reg_9825 = add_ln125_71_fu_6892_p2.read();
        add_ln125_75_reg_9837 = add_ln125_75_fu_6983_p2.read();
        add_ln125_78_reg_9862 = add_ln125_78_fu_7022_p2.read();
        lshr_ln125_19_reg_9857 = add_ln125_75_fu_6983_p2.read().range(31, 27);
        lshr_ln125_37_reg_9847 = add_ln125_67_fu_6801_p2.read().range(31, 2);
        lshr_ln125_38_reg_9872 = add_ln125_71_fu_6892_p2.read().range(31, 2);
        lshr_ln129_1_reg_9882 = add_ln125_75_fu_6983_p2.read().range(31, 2);
        or_ln125_71_reg_9830 = or_ln125_71_fu_6912_p3.read();
        trunc_ln125_37_reg_9842 = trunc_ln125_37_fu_6989_p1.read();
        trunc_ln125_38_reg_9852 = trunc_ln125_38_fu_7003_p1.read();
        trunc_ln125_39_reg_9867 = trunc_ln125_39_fu_7028_p1.read();
        trunc_ln129_1_reg_9877 = trunc_ln129_1_fu_7042_p1.read();
    }
    if (esl_seteq<1,1,1>(ap_const_logic_1, ap_CS_fsm_state16.read())) {
        W_load_4_reg_9958 = W_q0.read();
        W_load_5_reg_9963 = W_q1.read();
        add_ln129_19_reg_9897 = add_ln129_19_fu_7455_p2.read();
        add_ln129_23_reg_9908 = add_ln129_23_fu_7534_p2.read();
        add_ln129_26_reg_9933 = add_ln129_26_fu_7573_p2.read();
        lshr_ln129_24_reg_9918 = add_ln129_15_fu_7376_p2.read().range(31, 2);
        lshr_ln129_25_reg_9943 = add_ln129_19_fu_7455_p2.read().range(31, 2);
        lshr_ln129_26_reg_9953 = add_ln129_23_fu_7534_p2.read().range(31, 2);
        lshr_ln129_6_reg_9928 = add_ln129_23_fu_7534_p2.read().range(31, 27);
        or_ln129_23_reg_9902 = or_ln129_23_fu_7475_p3.read();
        trunc_ln129_11_reg_9913 = trunc_ln129_11_fu_7540_p1.read();
        trunc_ln129_12_reg_9923 = trunc_ln129_12_fu_7554_p1.read();
        trunc_ln129_13_reg_9938 = trunc_ln129_13_fu_7579_p1.read();
        trunc_ln129_15_reg_9948 = trunc_ln129_15_fu_7593_p1.read();
    }
    if (esl_seteq<1,1,1>(ap_const_logic_1, ap_CS_fsm_state8.read())) {
        add_ln117_42_reg_8908 = add_ln117_42_fu_1864_p2.read();
        lshr_ln117_10_reg_8903 = add_ln117_39_fu_1792_p2.read().range(31, 27);
        lshr_ln117_30_reg_8929 = add_ln117_39_fu_1792_p2.read().range(31, 2);
        or_ln117_35_reg_8888 = or_ln117_35_fu_1721_p3.read();
        or_ln117_37_reg_8893 = or_ln117_37_fu_1812_p3.read();
        or_ln117_39_reg_8913 = or_ln117_39_fu_1884_p3.read();
        or_ln117_40_reg_8919 = or_ln117_40_fu_1910_p2.read();
        sha_info_data_load_12_reg_8869 = sha_info_data_q0.read();
        sha_info_data_load_13_reg_8878 = sha_info_data_q1.read();
        trunc_ln117_20_reg_8898 = trunc_ln117_20_fu_1820_p1.read();
        trunc_ln117_23_reg_8924 = trunc_ln117_23_fu_1916_p1.read();
    }
    if (esl_seteq<1,1,1>(ap_const_logic_1, ap_CS_fsm_state9.read())) {
        add_ln117_63_reg_9125 = add_ln117_63_fu_2617_p2.read();
        add_ln117_67_reg_9137 = add_ln117_67_fu_2709_p2.read();
        add_ln117_70_reg_9163 = add_ln117_70_fu_2749_p2.read();
        lshr_ln117_17_reg_9158 = add_ln117_67_fu_2709_p2.read().range(31, 27);
        lshr_ln117_35_reg_9148 = add_ln117_59_fu_2525_p2.read().range(31, 2);
        lshr_ln117_36_reg_9173 = add_ln117_63_fu_2617_p2.read().range(31, 2);
        lshr_ln117_37_reg_9183 = add_ln117_67_fu_2709_p2.read().range(31, 2);
        or_ln117_49_reg_9131 = or_ln117_49_fu_2637_p3.read();
        trunc_ln117_33_reg_9143 = trunc_ln117_33_fu_2715_p1.read();
        trunc_ln117_34_reg_9153 = trunc_ln117_34_fu_2729_p1.read();
        trunc_ln117_35_reg_9168 = trunc_ln117_35_fu_2755_p1.read();
        trunc_ln117_37_reg_9178 = trunc_ln117_37_fu_2769_p1.read();
        xor_ln107_11_reg_8955 = xor_ln107_11_fu_1985_p2.read();
        xor_ln107_14_reg_8962 = xor_ln107_14_fu_2000_p2.read();
        xor_ln107_17_reg_8970 = xor_ln107_17_fu_2015_p2.read();
        xor_ln107_20_reg_8978 = xor_ln107_20_fu_2031_p2.read();
        xor_ln107_23_reg_8986 = xor_ln107_23_fu_2047_p2.read();
        xor_ln107_24_reg_8994 = xor_ln107_24_fu_2053_p2.read();
        xor_ln107_26_reg_8999 = xor_ln107_26_fu_2063_p2.read();
        xor_ln107_27_reg_9006 = xor_ln107_27_fu_2069_p2.read();
        xor_ln107_29_reg_9011 = xor_ln107_29_fu_2079_p2.read();
        xor_ln107_2_reg_8934 = xor_ln107_2_fu_1939_p2.read();
        xor_ln107_30_reg_9018 = xor_ln107_30_fu_2085_p2.read();
        xor_ln107_32_reg_9024 = xor_ln107_32_fu_2095_p2.read();
        xor_ln107_33_reg_9031 = xor_ln107_33_fu_2101_p2.read();
        xor_ln107_35_reg_9037 = xor_ln107_35_fu_2111_p2.read();
        xor_ln107_36_reg_9044 = xor_ln107_36_fu_2117_p2.read();
        xor_ln107_38_reg_9049 = xor_ln107_38_fu_2128_p2.read();
        xor_ln107_39_reg_9056 = xor_ln107_39_fu_2134_p2.read();
        xor_ln107_41_reg_9062 = xor_ln107_41_fu_2145_p2.read();
        xor_ln107_42_reg_9069 = xor_ln107_42_fu_2151_p2.read();
        xor_ln107_44_reg_9074 = xor_ln107_44_fu_2163_p2.read();
        xor_ln107_45_reg_9081 = xor_ln107_45_fu_2169_p2.read();
        xor_ln107_47_reg_9086 = xor_ln107_47_fu_2181_p2.read();
        xor_ln107_48_reg_9094 = xor_ln107_48_fu_2187_p2.read();
        xor_ln107_51_reg_9100 = xor_ln107_51_fu_2193_p2.read();
        xor_ln107_57_reg_9106 = xor_ln107_57_fu_2199_p2.read();
        xor_ln107_5_reg_8941 = xor_ln107_5_fu_1955_p2.read();
        xor_ln107_60_reg_9113 = xor_ln107_60_fu_2205_p2.read();
        xor_ln107_69_reg_9119 = xor_ln107_69_fu_2211_p2.read();
        xor_ln107_8_reg_8948 = xor_ln107_8_fu_1970_p2.read();
    }
    if (esl_seteq<1,1,1>(ap_const_logic_1, ap_CS_fsm_state10.read())) {
        add_ln121_11_reg_9470 = add_ln121_11_fu_3888_p2.read();
        add_ln121_15_reg_9481 = add_ln121_15_fu_3967_p2.read();
        add_ln121_18_reg_9506 = add_ln121_18_fu_4006_p2.read();
        lshr_ln121_22_reg_9491 = add_ln121_7_fu_3809_p2.read().range(31, 2);
        lshr_ln121_23_reg_9516 = add_ln121_11_fu_3888_p2.read().range(31, 2);
        lshr_ln121_24_reg_9526 = add_ln121_15_fu_3967_p2.read().range(31, 2);
        lshr_ln121_4_reg_9501 = add_ln121_15_fu_3967_p2.read().range(31, 27);
        or_ln121_21_reg_9475 = or_ln121_21_fu_3908_p3.read();
        trunc_ln121_11_reg_9521 = trunc_ln121_11_fu_4026_p1.read();
        trunc_ln121_7_reg_9486 = trunc_ln121_7_fu_3973_p1.read();
        trunc_ln121_8_reg_9496 = trunc_ln121_8_fu_3987_p1.read();
        trunc_ln121_9_reg_9511 = trunc_ln121_9_fu_4012_p1.read();
        xor_ln107_101_reg_9291 = xor_ln107_101_fu_3026_p2.read();
        xor_ln107_104_reg_9297 = xor_ln107_104_fu_3044_p2.read();
        xor_ln107_107_reg_9303 = xor_ln107_107_fu_3062_p2.read();
        xor_ln107_110_reg_9309 = xor_ln107_110_fu_3080_p2.read();
        xor_ln107_113_reg_9315 = xor_ln107_113_fu_3098_p2.read();
        xor_ln107_116_reg_9321 = xor_ln107_116_fu_3116_p2.read();
        xor_ln107_119_reg_9327 = xor_ln107_119_fu_3134_p2.read();
        xor_ln107_122_reg_9333 = xor_ln107_122_fu_3152_p2.read();
        xor_ln107_125_reg_9340 = xor_ln107_125_fu_3170_p2.read();
        xor_ln107_128_reg_9347 = xor_ln107_128_fu_3188_p2.read();
        xor_ln107_131_reg_9353 = xor_ln107_131_fu_3206_p2.read();
        xor_ln107_134_reg_9360 = xor_ln107_134_fu_3224_p2.read();
        xor_ln107_137_reg_9367 = xor_ln107_137_fu_3242_p2.read();
        xor_ln107_138_reg_9374 = xor_ln107_138_fu_3248_p2.read();
        xor_ln107_140_reg_9379 = xor_ln107_140_fu_3260_p2.read();
        xor_ln107_143_reg_9387 = xor_ln107_143_fu_3278_p2.read();
        xor_ln107_146_reg_9395 = xor_ln107_146_fu_3296_p2.read();
        xor_ln107_149_reg_9402 = xor_ln107_149_fu_3314_p2.read();
        xor_ln107_152_reg_9410 = xor_ln107_152_fu_3332_p2.read();
        xor_ln107_155_reg_9416 = xor_ln107_155_fu_3350_p2.read();
        xor_ln107_158_reg_9423 = xor_ln107_158_fu_3368_p2.read();
        xor_ln107_161_reg_9430 = xor_ln107_161_fu_3386_p2.read();
        xor_ln107_167_reg_9437 = xor_ln107_167_fu_3404_p2.read();
        xor_ln107_170_reg_9444 = xor_ln107_170_fu_3422_p2.read();
        xor_ln107_176_reg_9450 = xor_ln107_176_fu_3440_p2.read();
        xor_ln107_179_reg_9460 = xor_ln107_179_fu_3459_p2.read();
        xor_ln107_50_reg_9188 = xor_ln107_50_fu_2787_p2.read();
        xor_ln107_53_reg_9194 = xor_ln107_53_fu_2796_p2.read();
        xor_ln107_56_reg_9200 = xor_ln107_56_fu_2809_p2.read();
        xor_ln107_59_reg_9206 = xor_ln107_59_fu_2819_p2.read();
        xor_ln107_62_reg_9212 = xor_ln107_62_fu_2828_p2.read();
        xor_ln107_65_reg_9218 = xor_ln107_65_fu_2842_p2.read();
        xor_ln107_68_reg_9224 = xor_ln107_68_fu_2856_p2.read();
        xor_ln107_71_reg_9230 = xor_ln107_71_fu_2866_p2.read();
        xor_ln107_74_reg_9236 = xor_ln107_74_fu_2880_p2.read();
        xor_ln107_77_reg_9242 = xor_ln107_77_fu_2895_p2.read();
        xor_ln107_80_reg_9248 = xor_ln107_80_fu_2911_p2.read();
        xor_ln107_83_reg_9254 = xor_ln107_83_fu_2926_p2.read();
        xor_ln107_86_reg_9260 = xor_ln107_86_fu_2941_p2.read();
        xor_ln107_89_reg_9266 = xor_ln107_89_fu_2957_p2.read();
        xor_ln107_92_reg_9272 = xor_ln107_92_fu_2974_p2.read();
        xor_ln107_95_reg_9279 = xor_ln107_95_fu_2990_p2.read();
        xor_ln107_98_reg_9285 = xor_ln107_98_fu_3008_p2.read();
    }
    if (esl_seteq<1,1,1>(ap_const_logic_1, ap_CS_fsm_state11.read())) {
        add_ln121_39_reg_9559 = add_ln121_39_fu_4488_p2.read();
        add_ln121_43_reg_9570 = add_ln121_43_fu_4567_p2.read();
        add_ln121_46_reg_9595 = add_ln121_46_fu_4606_p2.read();
        lshr_ln121_11_reg_9590 = add_ln121_43_fu_4567_p2.read().range(31, 27);
        lshr_ln121_29_reg_9580 = add_ln121_35_fu_4409_p2.read().range(31, 2);
        lshr_ln121_30_reg_9605 = add_ln121_39_fu_4488_p2.read().range(31, 2);
        lshr_ln121_31_reg_9615 = add_ln121_43_fu_4567_p2.read().range(31, 2);
        or_ln121_28_reg_9564 = or_ln121_28_fu_4508_p3.read();
        trunc_ln121_21_reg_9575 = trunc_ln121_21_fu_4573_p1.read();
        trunc_ln121_22_reg_9585 = trunc_ln121_22_fu_4587_p1.read();
        trunc_ln121_23_reg_9600 = trunc_ln121_23_fu_4612_p1.read();
        trunc_ln121_25_reg_9610 = trunc_ln121_25_fu_4626_p1.read();
        xor_ln107_164_reg_9531 = xor_ln107_164_fu_4048_p2.read();
        xor_ln107_173_reg_9538 = xor_ln107_173_fu_4063_p2.read();
        xor_ln107_182_reg_9544 = xor_ln107_182_fu_4078_p2.read();
    }
    if (esl_seteq<1,1,1>(ap_const_logic_1, ap_CS_fsm_state12.read())) {
        add_ln121_67_reg_9630 = add_ln121_67_fu_5058_p2.read();
        add_ln121_71_reg_9641 = add_ln121_71_fu_5137_p2.read();
        add_ln121_74_reg_9666 = add_ln121_74_fu_5176_p2.read();
        lshr_ln121_18_reg_9661 = add_ln121_71_fu_5137_p2.read().range(31, 27);
        lshr_ln121_36_reg_9651 = add_ln121_63_fu_4979_p2.read().range(31, 2);
        lshr_ln121_37_reg_9676 = add_ln121_67_fu_5058_p2.read().range(31, 2);
        lshr_ln121_38_reg_9686 = add_ln121_71_fu_5137_p2.read().range(31, 2);
        or_ln121_35_reg_9635 = or_ln121_35_fu_5078_p3.read();
        trunc_ln121_35_reg_9646 = trunc_ln121_35_fu_5143_p1.read();
        trunc_ln121_36_reg_9656 = trunc_ln121_36_fu_5157_p1.read();
        trunc_ln121_37_reg_9671 = trunc_ln121_37_fu_5182_p1.read();
        trunc_ln121_39_reg_9681 = trunc_ln121_39_fu_5196_p1.read();
    }
    if (esl_seteq<1,1,1>(ap_const_logic_1, ap_CS_fsm_state13.read())) {
        add_ln125_15_reg_9691 = add_ln125_15_fu_5646_p2.read();
        add_ln125_19_reg_9703 = add_ln125_19_fu_5737_p2.read();
        add_ln125_22_reg_9728 = add_ln125_22_fu_5776_p2.read();
        lshr_ln125_23_reg_9713 = add_ln125_11_fu_5555_p2.read().range(31, 2);
        lshr_ln125_24_reg_9738 = add_ln125_15_fu_5646_p2.read().range(31, 2);
        lshr_ln125_25_reg_9748 = add_ln125_19_fu_5737_p2.read().range(31, 2);
        lshr_ln125_5_reg_9723 = add_ln125_19_fu_5737_p2.read().range(31, 27);
        or_ln125_29_reg_9696 = or_ln125_29_fu_5666_p3.read();
        trunc_ln125_10_reg_9718 = trunc_ln125_10_fu_5757_p1.read();
        trunc_ln125_11_reg_9733 = trunc_ln125_11_fu_5782_p1.read();
        trunc_ln125_13_reg_9743 = trunc_ln125_13_fu_5796_p1.read();
        trunc_ln125_9_reg_9708 = trunc_ln125_9_fu_5743_p1.read();
    }
    if (esl_seteq<1,1,1>(ap_const_logic_1, ap_CS_fsm_state17.read())) {
        add_ln129_54_reg_9993 = add_ln129_54_fu_8133_p2.read();
        lshr_ln129_13_reg_9983 = add_ln129_51_fu_8074_p2.read().range(31, 27);
        lshr_ln129_33_reg_10014 = add_ln129_51_fu_8074_p2.read().range(31, 2);
        or_ln129_30_reg_9968 = or_ln129_30_fu_8015_p3.read();
        or_ln129_31_reg_9973 = or_ln129_31_fu_8094_p3.read();
        or_ln129_32_reg_9998 = or_ln129_32_fu_8153_p3.read();
        trunc_ln129_26_reg_9978 = trunc_ln129_26_fu_8102_p1.read();
        trunc_ln129_29_reg_10009 = trunc_ln129_29_fu_8173_p1.read();
        xor_ln129_27_reg_9988 = xor_ln129_27_fu_8122_p2.read();
        xor_ln129_29_reg_10004 = xor_ln129_29_fu_8167_p2.read();
    }
    if (esl_seteq<1,1,1>(ap_const_logic_1, ap_CS_fsm_state18.read())) {
        add_ln129_75_reg_10019 = add_ln129_75_fu_8537_p2.read();
        add_ln132_1_reg_10024 = add_ln132_1_fu_8621_p2.read();
        add_ln132_4_reg_10029 = add_ln132_4_fu_8632_p2.read();
        add_ln135_reg_10034 = add_ln135_fu_8644_p2.read();
    }
    if (esl_seteq<1,1,1>(ap_const_logic_1, ap_CS_fsm_state19.read())) {
        add_ln133_reg_10039 = add_ln133_fu_8665_p2.read();
    }
    if ((esl_seteq<1,1,1>(ap_const_logic_1, ap_CS_fsm_state2.read()) || esl_seteq<1,1,1>(ap_const_logic_1, ap_CS_fsm_state9.read()))) {
        reg_925 = sha_info_data_q0.read();
        reg_930 = sha_info_data_q1.read();
    }
    if (esl_seteq<1,1,1>(ap_const_logic_1, ap_CS_fsm_state3.read())) {
        sha_info_data_load_2_reg_8669 = sha_info_data_q0.read();
        sha_info_data_load_3_reg_8677 = sha_info_data_q1.read();
    }
    if (esl_seteq<1,1,1>(ap_const_logic_1, ap_CS_fsm_state4.read())) {
        sha_info_data_load_4_reg_8685 = sha_info_data_q0.read();
        sha_info_data_load_5_reg_8693 = sha_info_data_q1.read();
    }
}

void sha_transform::thread_ap_NS_fsm() {
    switch (ap_CS_fsm.read().to_uint64()) {
        case 1 : 
            if ((esl_seteq<1,1,1>(ap_const_logic_1, ap_CS_fsm_state1.read()) && esl_seteq<1,1,1>(ap_start.read(), ap_const_logic_1))) {
                ap_NS_fsm = ap_ST_fsm_state2;
            } else {
                ap_NS_fsm = ap_ST_fsm_state1;
            }
            break;
        case 2 : 
            ap_NS_fsm = ap_ST_fsm_state3;
            break;
        case 4 : 
            ap_NS_fsm = ap_ST_fsm_state4;
            break;
        case 8 : 
            ap_NS_fsm = ap_ST_fsm_state5;
            break;
        case 16 : 
            ap_NS_fsm = ap_ST_fsm_state6;
            break;
        case 32 : 
            ap_NS_fsm = ap_ST_fsm_state7;
            break;
        case 64 : 
            ap_NS_fsm = ap_ST_fsm_state8;
            break;
        case 128 : 
            ap_NS_fsm = ap_ST_fsm_state9;
            break;
        case 256 : 
            ap_NS_fsm = ap_ST_fsm_state10;
            break;
        case 512 : 
            ap_NS_fsm = ap_ST_fsm_state11;
            break;
        case 1024 : 
            ap_NS_fsm = ap_ST_fsm_state12;
            break;
        case 2048 : 
            ap_NS_fsm = ap_ST_fsm_state13;
            break;
        case 4096 : 
            ap_NS_fsm = ap_ST_fsm_state14;
            break;
        case 8192 : 
            ap_NS_fsm = ap_ST_fsm_state15;
            break;
        case 16384 : 
            ap_NS_fsm = ap_ST_fsm_state16;
            break;
        case 32768 : 
            ap_NS_fsm = ap_ST_fsm_state17;
            break;
        case 65536 : 
            ap_NS_fsm = ap_ST_fsm_state18;
            break;
        case 131072 : 
            ap_NS_fsm = ap_ST_fsm_state19;
            break;
        case 262144 : 
            ap_NS_fsm = ap_ST_fsm_state20;
            break;
        case 524288 : 
            ap_NS_fsm = ap_ST_fsm_state21;
            break;
        case 1048576 : 
            ap_NS_fsm = ap_ST_fsm_state22;
            break;
        case 2097152 : 
            ap_NS_fsm = ap_ST_fsm_state23;
            break;
        case 4194304 : 
            ap_NS_fsm = ap_ST_fsm_state24;
            break;
        case 8388608 : 
            ap_NS_fsm = ap_ST_fsm_state25;
            break;
        case 16777216 : 
            ap_NS_fsm = ap_ST_fsm_state26;
            break;
        case 33554432 : 
            ap_NS_fsm = ap_ST_fsm_state27;
            break;
        case 67108864 : 
            ap_NS_fsm = ap_ST_fsm_state28;
            break;
        case 134217728 : 
            ap_NS_fsm = ap_ST_fsm_state29;
            break;
        case 268435456 : 
            ap_NS_fsm = ap_ST_fsm_state30;
            break;
        case 536870912 : 
            ap_NS_fsm = ap_ST_fsm_state31;
            break;
        case 1073741824 : 
            ap_NS_fsm = ap_ST_fsm_state32;
            break;
        case 2147483648 : 
            ap_NS_fsm = ap_ST_fsm_state33;
            break;
        case 4294967296 : 
            ap_NS_fsm = ap_ST_fsm_state34;
            break;
        case 8589934592 : 
            ap_NS_fsm = ap_ST_fsm_state35;
            break;
        case 17179869184 : 
            ap_NS_fsm = ap_ST_fsm_state36;
            break;
        case 34359738368 : 
            ap_NS_fsm = ap_ST_fsm_state37;
            break;
        case 68719476736 : 
            ap_NS_fsm = ap_ST_fsm_state38;
            break;
        case 137438953472 : 
            ap_NS_fsm = ap_ST_fsm_state39;
            break;
        case 274877906944 : 
            ap_NS_fsm = ap_ST_fsm_state40;
            break;
        case 549755813888 : 
            ap_NS_fsm = ap_ST_fsm_state41;
            break;
        case 1099511627776 : 
            ap_NS_fsm = ap_ST_fsm_state42;
            break;
        case 2199023255552 : 
            ap_NS_fsm = ap_ST_fsm_state43;
            break;
        case 4398046511104 : 
            ap_NS_fsm = ap_ST_fsm_state44;
            break;
        case 8796093022208 : 
            ap_NS_fsm = ap_ST_fsm_state45;
            break;
        case 17592186044416 : 
            ap_NS_fsm = ap_ST_fsm_state1;
            break;
        default : 
            ap_NS_fsm =  (sc_lv<45>) ("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX");
            break;
    }
}

}

