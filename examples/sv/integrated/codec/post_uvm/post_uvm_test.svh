class post_uvm_test extends uvm_test;
   `uvm_component_utils(post_uvm_test)

   post_uvm_env env;

   function new(string name, uvm_component parent = null);
      super.new(name, parent);
   endfunction

   function void build_phase(uvm_phase phase);
      super.build_phase(phase);

      env = post_uvm_env::type_id::create("env", this);
   endfunction
/*
   task run_phase(uvm_phase phase);
      phase.raise_objection(this, "XXXXX");
      #(550000);
      phase.drop_objection(this, "XXXXX");
   endtask
*/
endclass