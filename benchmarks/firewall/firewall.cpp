//
// Copyright (c) 2016-2019 Haggai Eran, Gabi Malka, Lior Zeno, Maroun Tork
// All rights reserved.
//
// Redistribution and use in source and binary forms, with or without modification,
// are permitted provided that the following conditions are met:
//
//  * Redistributions of source code must retain the above copyright notice, this
// list of conditions and the following disclaimer.
//  * Redistributions in binary form must reproduce the above copyright notice,
// this list of conditions and the following disclaimer in the documentation and/or
// other materials provided with the distribution.
//
// THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS ``AS IS''
// AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
// IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
// DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR
// ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
// (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
// LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON
// ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
// (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
// SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
//

#include "parser.hpp"
#include "firewall.hpp"
#include "cache.hpp"

int firewall_rpc(int addr, gateway_data& data,
    hls::stream<gateway_command>& gateway_commands,
    hls::stream<gateway_response>& gateway_responses)
{
    switch (addr) {
    case FIREWALL_ADD:
        return gateway_add_entry(std::make_pair(data.tag, data.result),
                                 &data.status, gateway_commands,
                                 gateway_responses);
    case FIREWALL_DEL:
        return gateway_delete_entry(data.tag, &data.status, gateway_commands,
                                    gateway_responses);
    default:
        return 1;
    }
}

void gateway(gateway_registers& r,
    hls::stream<gateway_command>& gateway_commands,
    hls::stream<gateway_response>& gateway_responses)
{
    static bool axilite_gateway_done;
DO_PRAGMA_SYN(HLS data_pack variable=r.cmd)
    if (r.cmd.go && !axilite_gateway_done) {
        int res = firewall_rpc(r.cmd.addr, r.data, gateway_commands,
                               gateway_responses);
        if (res != 1) {
            axilite_gateway_done = true;
            r.done = 1;
        }
    } else if (!r.cmd.go && axilite_gateway_done) {
        axilite_gateway_done = false;
        r.done = 0;
    }
}

void map_metadata_to_hash_lookup(metadata_stream& in,
        hls::stream<hash_tag> &out)
{
    if (in.empty() || out.full())
        return;

    metadata m;
    in.read_nb(m);
    out.write_nb(hash_tag(m.ip_source, m.ip_dest, m.udp_source, m.udp_dest));
}

volatile void merge_hash_results(lookup_result_stream& results,
                        metadata_stream& metadata_in, bool_stream &classify_out)
{
    if (results.empty() || metadata_in.empty() || classify_out.full())
        return;
    
    ntl_legacy::maybe<std::pair<uint32_t, ap_uint<1> > > val = results.read();
    metadata m = metadata_in.read();
     
    bool forward = !valid_udp(m) ||
        (val.valid() ? val.value().second : ap_uint<1>(0));
    classify_out.write(forward);
}

void firewall_step(axi_data_stream& in, axi_data_stream& data_out, bool_stream& classify_out, gateway_registers& g)
{
    static axi_data_stream dup_to_parse;
#pragma HLS STREAM variable=dup_to_parse depth=12 dim=1
    static metadata_stream parse_to_dup, dup_metadata_to_hash, dup_metadata_to_invalid;
#pragma HLS STREAM variable=dup_metadata_to_hash depth=12 dim=1
#pragma HLS STREAM variable=parse_to_dup depth=12 dim=1
#pragma HLS stream variable=dup_metadata_to_invalid depth=12

    static hls::stream<gateway_command> gateway_commands;
#pragma HLS STREAM variable=gateway_commands depth=12 dim=1
    static hls::stream<gateway_response> gateway_responses;
#pragma HLS STREAM variable=gateway_responses depth=12 dim=1
    static tag_stream lookups;
#pragma HLS STREAM variable=lookups depth=12 dim=1
    static lookup_result_stream results;
#pragma HLS STREAM variable=results depth=12 dim=1

    gateway(g, gateway_commands, gateway_responses);

    dup(in, dup_to_parse, data_out);
    parser(dup_to_parse, parse_to_dup);
    dup(parse_to_dup, dup_metadata_to_hash, dup_metadata_to_invalid);

    map_metadata_to_hash_lookup(dup_metadata_to_hash, lookups);

    hash_table(lookups, results, gateway_commands, gateway_responses);

    merge_hash_results(results, dup_metadata_to_invalid, classify_out);
}

void firewall_top(hls::stream<ntl_legacy::raw_axi_data>& in,
                  hls::stream<ntl_legacy::raw_axi_data>& data_out,
                  bool_stream& classify_out_stream, gateway_registers& g)
{
    static axi_data_stream in_fifo, out_fifo;
#pragma HLS STREAM variable=in_fifo depth=12 dim=1
#pragma HLS stream variable=out_fifo depth=12

    ntl_legacy::link(in, in_fifo);
    ntl_legacy::link(out_fifo, data_out);
    firewall_step(in_fifo, out_fifo, classify_out_stream, g);
    
}

void firewall_outer_top(hls::stream<ntl_legacy::raw_axi_data> in[NUM],
                  hls::stream<ntl_legacy::raw_axi_data> data_out[NUM],
                  bool_stream classify_out_stream[NUM], gateway_registers g[NUM]){
/*
#pragma HLS interface ap_ctrl_none port=return
#pragma HLS interface axis port=in
#pragma HLS interface axis port=data_out

#pragma HLS interface s_axilite port=g->cmd offset=0x100
#pragma HLS interface s_axilite port=g->data offset=0x118
#pragma HLS interface s_axilite port=g->done offset=0xfc
*/
    outer_top_loop:for (int i = 0; i < NUM; ++i){
//#pragma HLS UNROLL factor=2
//#pragma HLS UNROLL factor=3
//#pragma HLS UNROLL factor=4
//#pragma HLS UNROLL factor=6
//#pragma HLS UNROLL
//#pragma HLS PIPELINE rewind
    	firewall_top(in[i], data_out[i], classify_out_stream[i], g[i]);
    }
}

