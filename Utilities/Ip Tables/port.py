#!/bin/python


class PortConstructor:
    ruleTemplate =  "iptables -t nat -A PREROUTING -i {inter} -p {proto} -m {proto} --dport {locport} -j DNAT --to-destination {destaddr}:{destport}\n"
    ruleTemplate += "iptables -t nat -A POSTROUTING -o {inter} -j SNAT --to-source {locaddr}"

    def construct(self, locaddr, locport, destaddr, destport, inter, proto):
        return self.ruleTemplate.format(locaddr=locaddr, locport=locport, destaddr=destaddr, destport=destport, inter=inter, proto=proto)


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()

    parser.add_argument("-L", "--locaddr", required=True, help="IP to \"listen\" on")
    parser.add_argument("-l", "--locport", required=True, help="The port to \"listen\" on")
    parser.add_argument("-D", "--destaddr", required=True, help="Destination IP")
    parser.add_argument("-d", "--destport", required=True, help="Destination port")
    parser.add_argument("-i", "--inter", help="Interface to \"listen\" on", default="enp8")
    parser.add_argument("-p", "--proto", help="The protocol. (tcp or udp)", default="tcp", choices=["tcp", "udp"])
    args = parser.parse_args()

    print(PortConstructor().construct(args.locaddr, args.locport, args.destaddr, args.destport, args.inter, args.proto))


