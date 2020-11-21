import idaapi
import idautils

jmprel_addr = 0
strtab_addr = 0
symtab_addr = 0

def get_index(plt_sec_entry_addr):
    addr = plt_sec_entry_addr
    assert GetMnem(addr) == "endbr64"
    addr += 4
    assert GetMnem(addr) == "jmp"
    plt_addr = idc.Dword(int(GetOpnd(addr,0)[7:],16))
    #print "plt_addr = " + hex(plt_addr)

    assert GetMnem(plt_addr) == "endbr64"
    push_addr = plt_addr + 4
    assert GetMnem(push_addr) == 'push'
    index = GetOpnd(push_addr,0)
    if "h" in index:
        index = index[:-1]
    return int(index,16)


def getName(idx, jmptab_addr, symtab_addr, strtab_addr):
    symidx = idc.Qword(jmptab_addr+idx*0x18 + 0x8) >> 32
    symtab_entry = symtab_addr + symidx * 0x18
    str_off = idc.Dword(symtab_entry)
    name_str = idc.GetString(str_off +strtab_addr)
    return name_str

def rename_plt_sec(plt_sec_entry_addr,name_str):
    # rename function
    MakeName(plt_sec_entry_addr,name_str)


def get_tables():
    global jmprel_addr
    global symtab_addr
    global strtab_addr
    addr = MinEA()
    addr += 0x40 # program header   
    while 1:
        PHT_type = idc.Dword(addr)
        if(PHT_type == 2):
            break
        addr += 0x38
    # print "addr = " + hex(addr)
    va = addr + 0x10
    dynamic_addr = idc.Qword(va) + MinEA()
    # print "dynamic_addr = " + hex(dynamic_addr)
    idx = 0
    while 1:
        t = idc.Qword(dynamic_addr+idx*0x10)
        if(not t):
            break
        else:
            if t == 0x17:
                jmprel_addr = idc.Qword(dynamic_addr + idx * 0x10 +0x8)
            elif t == 0x6 :
                symtab_addr = idc.Qword(dynamic_addr + idx * 0x10 + 0x8)
            elif t == 0x5:
                strtab_addr = idc.Qword(dynamic_addr + idx * 0x10 + 0x8)
        idx += 1
    #assert jmprel_addr and symtab_addr and strtab_addr

def get_plt_sec_addr():
    for i in idautils.Segments():
        if idc.SegName(i) == ".plt.sec":
            return [idc.SegStart(i),idc.SegEnd(i)]
    return []

def main():
    get_tables()
    print "jmprel_addr = %lx"%(jmprel_addr)
    print "strtab_addr = %lx"%(strtab_addr)
    print "symtab_addr = %lx"%(symtab_addr)

    print getName(0,jmprel_addr,symtab_addr,strtab_addr)
    print getName(1,jmprel_addr,symtab_addr,strtab_addr)
    print getName(2,jmprel_addr,symtab_addr,strtab_addr)

    res = get_plt_sec_addr()

    plt_sec_entry_addr = res[0]
    while(plt_sec_entry_addr < res[1]):
        name_str = getName(get_index(plt_sec_entry_addr),jmprel_addr,symtab_addr,strtab_addr)
        rename_plt_sec(plt_sec_entry_addr,name_str+"_plt_sec")
        plt_sec_entry_addr += 0x10


main()






