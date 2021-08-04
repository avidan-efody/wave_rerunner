// 
// -------------------------------------------------------------
//    Copyright 2011 Synopsys, Inc.
//    All Rights Reserved Worldwide
// 
//    Licensed under the Apache License, Version 2.0 (the
//    "License"); you may not use this file except in
//    compliance with the License.  You may obtain a copy of
//    the License at
// 
//        http://www.apache.org/licenses/LICENSE-2.0
// 
//    Unless required by applicable law or agreed to in
//    writing, software distributed under the License is
//    distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR
//    CONDITIONS OF ANY KIND, either express or implied.  See
//    the License for the specific language governing
//    permissions and limitations under the License.
// -------------------------------------------------------------
//


`include "apb.sv"
`include "vip.sv"

package codec_pkg;
import uvm_pkg::*;
`include "uvm_macros.svh"

import apb_pkg::*;
import vip_pkg::*;

`include "sym_sb.svh"
`include "apb2txrx.svh"
`include "reg_model.svh"
`include "tb_env.svh"
`include "testlib.svh"

`include "post_uvm/post_uvm_env.svh"
`include "post_uvm/post_uvm_test.svh"

endpackage
