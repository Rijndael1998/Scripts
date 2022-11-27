#!/bin/python


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()

    parser.add_argument("-L", "--locaddr", required=True, help="IP to \"listen\" on")
    parser.add_argument("-l", "--locport", required=True, help="The ascending sequential range of ports to \"listen\" on. Eg: 100-120 forwards ports 100 to 120 inclusive")
    parser.add_argument("-D", "--destaddr", required=True, help="Destination IP")
    parser.add_argument("-d", "--destport", required=True, help="First destination port")
    parser.add_argument("-i", "--inter", help="Interface to \"listen\" on", default="enp8")
    parser.add_argument("-p", "--proto", help="The protocol. (tcp or udp)", default="tcp", choices=["tcp", "udp"])
    args = parser.parse_args()


    port = args.locport.split("-")
    from port import PortConstructor
    pc = PortConstructor()

    i = 0
    dest = int(args.destport)
    for locport in range(int(port[0]), int(port[1])+1):
        print(pc.construct(args.locaddr, locport, args.destaddr, dest + i, args.inter, args.proto))
        i += 1

