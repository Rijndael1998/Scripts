#!/bin/python3


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()

    parser.add_argument("-L", "--locaddr", required=True, help="IP to \"listen\" on")
    parser.add_argument("-l", "--locport", required=True, help="The ascending sequential range of ports to \"listen\" on. Eg: 100-120 forwards ports 100 to 120 inclusive")
    parser.add_argument("-D", "--destaddr", required=True, help="Destination IP")
    parser.add_argument("-d", "--destport", required=False, help="First destination port", default=None)
    parser.add_argument("-i", "--inter", help="Interface to \"listen\" on", default="enp8")
    parser.add_argument("-p", "--proto", help="The protocol. (tcp or udp or both)", default="tcp", choices=["tcp", "udp", "both"])
    parser.add_argument("-e", "--execute", help="Execute the command", action="count")
    args = parser.parse_args()


    port = args.locport.split("-")
    from port import PortConstructor
    pc = PortConstructor()

    if args.proto == "both":
        protos = ["tcp", "udp"]

    else:
        protos = [args.proto]
    
    for proto in protos:
        i = 0
        dest = int(args.destport) if args.destport is not None else int(port[0])
        for locport in range(int(port[0]), int(port[1])+1):
            if not args.execute:
                print(pc.construct(args.locaddr, locport, args.destaddr, dest + i, args.inter, proto))

            else:
                pc.execute(args.locaddr, locport, args.destaddr, dest + i, args.inter, proto)

            i += 1


