#!/bin/python3


class PortConstructor:
    from os import system as sys
    from time import sleep, time
    ruleTemplate =  "iptables -t nat -A PREROUTING -i {inter} -p {proto} --dport {locport} -j DNAT --to-destination {destaddr}:{destport}\n" # Forward
    ruleTemplate += "iptables -t nat -A POSTROUTING -o {inter} -j SNAT --to-source {locaddr}\n" # Back
    ruleTemplate += "iptables -A FORWARD -p {proto} -d {locaddr} --dport {locport} -j ACCEPT" # Allow

    def construct(self, locaddr, locport, destaddr, destport, inter, proto):
        return self.ruleTemplate.format(locaddr=locaddr, locport=locport, destaddr=destaddr, destport=destport, inter=inter, proto=proto)

    def execute(self, locaddr, locport, destaddr, destport, inter, proto):
        command = self.construct(locaddr, locport, destaddr, destport, inter, proto)
        print(str(self.time()) + "".join(" > " + com + "\n" for com in command.split("\n")))
        self.sleep(0.1)
        self.sys(command)


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()

    parser.add_argument("-L", "--locaddr", required=True, help="IP to \"listen\" on")
    parser.add_argument("-l", "--locport", required=True, help="The port to \"listen\" on")
    parser.add_argument("-D", "--destaddr", required=True, help="Destination IP")
    parser.add_argument("-d", "--destport", required=True, help="Destination port")
    parser.add_argument("-i", "--inter", help="Interface to \"listen\" on", default="enp8")
    parser.add_argument("-p", "--proto", help="The protocol. (tcp or udp or both)", default="tcp", choices=["tcp", "udp", "both"])
    parser.add_argument("-e", "--execute", help="Execute the command", action="count")
    args = parser.parse_args()

    if args.proto == "both":
        protos = ["tcp", "udp"]

    else:
        protos = [args.proto]

    for proto in protos:
        if not args.execute:
            print(PortConstructor().construct(args.locaddr, args.locport, args.destaddr, args.destport, args.inter, proto))
        
        else:
            PortConstructor().execute(args.locaddr, args.locport, args.destaddr, args.destport, args.inter, proto)

