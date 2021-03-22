import idaapi
import idc
import idautils


def get_func_boundaries(ea):
	func=idaapi.get_func(ea)
	start = func.start_ea
	end	  =func.end_ea
	return start,end

def get_disassm(addr):
    start,end = get_func_boundaries(addr)
    while start<end:
        mnemonic=idc.GetMnem(start)
        if mnemonic == "ret" or mnemonic == "retn":
            print(hex(start))
        start = ida_bytes.next_head(start+1,end)


faddr = 0x405990
start,end = get_disassm(faddr)