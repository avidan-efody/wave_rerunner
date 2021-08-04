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

class post_uvm_env extends uvm_env;
   `uvm_component_utils(post_uvm_env)

   tb_ctl_vif vif;

   apb_agent apb;
   vip_agent vip;
   reg_dut regmodel;

   sym_sb ingress;  // VIP->DUT
   sym_sb egress;   // DUT->VIP
   apb2txrx adapt;

   function new(string name, uvm_component parent = null);
      super.new(name, parent);
   endfunction
      
   function void build_phase(uvm_phase phase);
      if (!uvm_config_db#(tb_ctl_vif)::get(this, "", "vif", vif)) begin
         `uvm_fatal("TB/ENV/NOVIF", "No virtual interface specified for environment instance")
      end

      uvm_config_db#(int)::set(this,  "apb",  "is_active", 0);
      uvm_config_db#(int)::set(this,  "vip",  "is_active", 0);
      
      apb = apb_agent::type_id::create("apb", this);
      vip = vip_agent::type_id::create("vip", this);

      if (regmodel == null) begin
         regmodel = reg_dut::type_id::create("regmodel",,get_full_name());
         regmodel.build();
         regmodel.lock_model();
      end

      ingress = sym_sb::type_id::create("ingress", this);
      egress = sym_sb::type_id::create("egress", this);
      adapt = apb2txrx::type_id::create("adapt", this);

   endfunction

   function void connect_phase(uvm_phase phase);
      if (regmodel.get_parent() == null) begin
         regmodel.default_map.set_auto_predict(1);
      end

      apb.mon.ap.connect(adapt.apb);

      vip.tx_mon.ap.connect(ingress.expected);
      vip.rx_mon.ap.connect(egress.observed);
      adapt.tx_ap.connect(egress.expected);
      adapt.rx_ap.connect(ingress.observed);
   endfunction

   task pre_reset_phase(uvm_phase phase);
      phase.raise_objection(this, "Waiting for reset to be valid");
      wait (vif.rst !== 1'bx);
      phase.drop_objection(this, "Reset is no longer X");
   endtask


   task reset_phase(uvm_phase phase);
      phase.raise_objection(this, "Asserting reset for 10 clock cycles");

      `uvm_info("TB/TRACE", "Resetting DUT...", UVM_NONE);
      
      regmodel.reset();
      vip.reset_and_suspend();
      repeat (10) @(posedge vif.clk);
      vip.resume();

      //m_isr = 0;

      phase.drop_objection(this, "HW reset done");
   endtask
endclass
