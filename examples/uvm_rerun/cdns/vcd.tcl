database -open my_vcd -vcd -into my_vcd.vcd

probe -create -database my_vcd -all -depth all top 

if {!$simvision_attached} {
   run 2000 us;
   exit;
};